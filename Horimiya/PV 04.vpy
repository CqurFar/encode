from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsutil import get_w
from vsgan import ESRGAN
from mvsfunc import ToYUV
import vapoursynth as vs
import atomchtools as atf
import beatricetools
import havsfunc as haf
import fvsfunc as fvf
import kagefunc
import mvsfunc as mvs
import muvsfunc as mvf
import descale as dsc
import finesharp
import ccd
import MCDenoise 
import cooldegrain
import finedehalo as fd
import insaneAA
import xaa
import vsTAAmbk
import HardAA
import lostfunc
import G41Fun
import lvsfunc
import limit
import vsdehalo
import vsdenoise
import vsmask
import vsgan
import vskernels
import dhh


#Техническое
core.num_threads = 24
core.max_cache_size = 30000

import os
os.environ['CUDA_MODULE_LOADING'] = 'LAZY'
os.environ['CUDA_FORCE_PRELOAD_LIBRARIES'] = '1'
os.environ['CUDA_AUTO_BOOST'] = '1'
os.environ['CUDA_DEVICE_MAX_CONNECTIONS'] = '32'
os.environ['CUDA_CACHE_MAXSIZE'] = '12884901888'


#Сорц
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Horimiya\PV 04.m2ts')
clip16 = core.resize.Lanczos(episode, format=vs.YUV420P16, matrix_s='709')
pf = core.dfttest.DFTTest(clip16, sigma=0.25, tbsize=3, opt=0)
db_ep = core.neo_f3kdb.Deband(pf, y=15, cb=7, cr=7, grainy=0, grainc=0, blur_first=False)


#Нейронка
rgbs_in = core.resize.Lanczos(episode, format=vs.RGBS, matrix_in='1')
ai = core.trt.Model(rgbs_in , engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2xGT-v2-evA-01.engine')

linear = core.resize.Lanczos(ai, format=vs.RGBS).fmtc.bitdepth(bits=16)
sigmoidized = haf.SigmoidInverse(linear, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1920, 1080) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
rgbs_out = core.resize.Lanczos(de_sigmoidized, format=vs.RGBS)

ai_expr = core.std.Expr([rgbs_in, rgbs_out], 'x 0.70 * y 0.30 * +')
dpir  = lvsfunc.dpir(ai_expr, strength=2, mode='denoise', cuda=True, matrix=1)


#Остальная фильтрация
clip16 = core.resize.Lanczos(dpir, format=vs.YUV420P16, matrix_s='709')
pf = core.dfttest.DFTTest(clip16, sigma=1.5, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=2, thsad=40, thsadc=38, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=40, cb=30, cr=30, grainy=0, grainc=0, blur_first=True)


#Зерно и вывод
deh = vsdehalo.fine_dehalo(db, ref=None, rx=2.4, ry=2.4, darkstr=0, brightstr=0.7, thmi=30, thma=100, excl=True, ss=1, edgeproc=0.5)
gr = core.grain.Add(deh, var=0.5, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)

mg = gr.std.Trim(0,739)+db_ep.std.Trim(740,1007)
mg.fmtc.bitdepth(bits=10).set_output()
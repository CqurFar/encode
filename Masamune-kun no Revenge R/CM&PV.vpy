from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsutil import get_w
from vsgan import ESRGAN
from mvsfunc import ToYUV, ToRGB
from havsfunc import FastLineDarkenMOD
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
import vsmlrt
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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Masamune-kun no Revenge R\CM 03.mkv')


#Депир
rgb_in = ToRGB(episode, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_in, model=1, strength=2, overlap=0, tilesize=[1920, 1080], backend=vsmlrt.Backend.TRT())
yuv_out_01 = ToYUV(dpir, matrix=1, css='420', depth=16)


#Нейронка
yuv_episode = ToYUV(yuv_out_01, depth=16)
clip_y = get_y(yuv_episode)
rgb_in = ToRGB(yuv_out_01, matrix=1, depth=32)

ai = core.trt.Model(rgb_in , engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AniScale2S_Compact_i8_60K_new.engine')

linear = ToRGB(ai, matrix=1, depth=16)
sigmoidized = haf.SigmoidInverse(linear, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1920, 1080) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
yuv_out_02 = ToYUV(de_sigmoidized, matrix=1, css='420', depth=16)

line_mask = vsmask.edge.Tritical().edgemask(clip_y, multi=4).std.Maximum().std.Limiter()
mask_ai = core.std.MaskedMerge(yuv_out_01, yuv_out_02, line_mask)
ai_expr = core.std.Expr([yuv_episode, mask_ai], 'x 0.60 * y 0.40 * +')


#Остальная фильтрация
clip16 = core.resize.Lanczos(ai_expr, format=vs.YUV420P16, matrix_s='709')
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=20, cb=15, cr=15, grainy=0, grainc=0, blur_first=False)


#Зерно и вывод
deh = vsdehalo.fine_dehalo(db, rx=2.3, ry=2.3, darkstr=0, brightstr=0.6, thmi=30, thma=100, ss=1, edgeproc=0.5)
gr = core.grain.Add(deh, var=0.5, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)
gr.fmtc.bitdepth(bits=10).set_output()
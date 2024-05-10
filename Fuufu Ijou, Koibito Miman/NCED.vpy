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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Fuufu Ijou, Koibito Miman\NCED.mkv')
episode_ai = core.lsmas.LWLibavSource(source=r'E:\Работа\Fuufu Ijou, Koibito Miman\NCED.mkv').resize.Lanczos(format=vs.RGBS, matrix_in='1')
dsc = episode.resize.Lanczos(width=1696, height=954)


#Нейронка
rgbs = core.resize.Lanczos(dsc, format=vs.RGBS, matrix_in='1')
ai = core.trt.Model(rgbs , engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2xGT-v2-evA-01.engine').resize.Lanczos(width=1920, height=1080)
ai_expr = core.std.Expr([episode_ai, ai], 'x 0.65 * y 0.35 * +')
dpir  = lvsfunc.dpir(ai_expr, strength=1, mode='denoise', cuda=True, matrix=1)


#Остальная фильтрация
clip16 = core.resize.Lanczos(dpir, format=vs.YUV420P16, matrix_s='709')
aa =  fvf.rfs(clip16, HardAA.HardAA(clip16, mask='simple', mthr=0.1), "[0 260]")
pf = core.dfttest.DFTTest(aa, sigma=0.5, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=2, thsad=40, thsadc=38, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=20, cb=10, cr=10, grainy=0, grainc=0, blur_first=False)


#Зерно и вывод
sh = core.cas.CAS(db, sharpness=0.1, opt=0)
gr = core.grain.Add(sh, var=0.5, uvar=0.1, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)
gr.fmtc.bitdepth(bits=10).set_output()
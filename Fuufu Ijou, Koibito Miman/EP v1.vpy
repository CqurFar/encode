from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Fuufu Ijou, Koibito Miman\EP 02.mkv')
desc = insaneAA.revert_upscale(episode, descale_strength=0.3, kernel='lanczos', descale_height=954, bicubic_b=0.33, bicubic_c=0.33) 
rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  

episode_ai = core.lsmas.LWLibavSource(source=r'E:\Работа\Fuufu Ijou, Koibito Miman\EP 02.mkv').resize.Lanczos(format=vs.RGBS, matrix_in='1')
desc_ai = insaneAA.revert_upscale(episode_ai, descale_strength=0.3, kernel='lanczos', descale_height=954, bicubic_b=0.33, bicubic_c=0.33) 
rescale_ai = insaneAA.rescale(desc_ai, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  


#Склейка OP
op_titles = core.std.Trim(episode, 1416, 3572)
ncop = core.lsmas.LWLibavSource(source=r'E:\Работа\Fuufu Ijou, Koibito Miman\NCOP.mkv').std.Trim(24, 2180).fmtc.bitdepth(bits=8)
ncop_fix = core.raws.Source(r'E:\Работа\Fuufu Ijou, Koibito Miman\NCOP.y4m').std.Trim(24, 2180).fmtc.bitdepth(bits=8)
op = atf.ApplyCredits(op_titles, ncop, ncop_fix).resize.Lanczos(format=vs.YUV420P16)


#Склейка ED
ed_titles = core.std.Trim(episode, 32151, 34309)
nced = core.lsmas.LWLibavSource(source=r'E:\Работа\Fuufu Ijou, Koibito Miman\NCED.mkv').std.Trim(24, 2182).fmtc.bitdepth(bits=8)
nced_fix = core.raws.Source(r'E:\Работа\Fuufu Ijou, Koibito Miman\NCED.y4m').std.Trim(24, 2182).fmtc.bitdepth(bits=8)
ed = atf.ApplyCredits(ed_titles, nced, nced_fix).resize.Lanczos(format=vs.YUV420P16)


#Нейронка
rgbs = core.resize.Lanczos(rescale, format=vs.RGBS, matrix_in='1')
ai = core.trt.Model(rgbs , engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2xGT-v2-evA-01.engine').resize.Lanczos(width=1920, height=1080)
ai_expr = core.std.Expr([rescale_ai, ai], 'x 0.65 * y 0.35 * +')
dpir  = lvsfunc.dpir(ai, strength=1, mode='denoise', cuda=True, matrix=1)


#Остальная фильтрация
clip16 = core.resize.Lanczos(dpir, format=vs.YUV420P16, matrix_s='709')
pf = core.dfttest.DFTTest(clip16, sigma=0.5, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=2, thsad=40, thsadc=38, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=20, cb=10, cr=10, grainy=0, grainc=0, blur_first=False)


#Зерно и вывод
sh = core.cas.CAS(db, sharpness=0.1, opt=0)
gr = core.grain.Add(sh, var=0.5, uvar=0.1, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)

mg = gr.std.Trim(0,1415)+op+gr.std.Trim(3573,32150)+ed+gr.std.Trim(34310,34813)
mg.fmtc.bitdepth(bits=10).set_output()
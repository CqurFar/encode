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


#Сорц + деинт + аа
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Fuufu Ijou, Koibito Miman\Bonus\SP\MV.m2ts')
cr = core.std.Crop(episode, top=134, bottom=134)


rgbs = core.resize.Lanczos(cr, format=vs.RGBS, matrix_in='1')
dpir  = lvsfunc.dpir(rgbs, strength=1, mode='denoise', cuda=True, matrix=1)


#Остальная фильтрация
clip16 = core.resize.Lanczos(dpir, format=vs.YUV420P16, matrix_s='709')
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=0)
db = core.neo_f3kdb.Deband(pf, y=30, cb=30, cr=30, grainy=0, grainc=0,  blur_first=False)
sh = core.cas.CAS(db, sharpness=0.3, opt=0)
gr = core.grain.Add(sh, var=0.4, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
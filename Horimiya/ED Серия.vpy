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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Horimiya\EP 01.m2ts')


#Склейка ED
ed_titles = core.std.Trim(episode, 31339, 33495)
nced = core.lsmas.LWLibavSource(r'E:\Работа\Horimiya\NCED.m2ts').std.Trim(24, 2180).fmtc.bitdepth(bits=8)
nced_fix = core.lsmas.LWLibavSource(r'E:\Работа\Horimiya\NCED.y4m').std.Trim(24, 2180).fmtc.bitdepth(bits=8)

credits_ = core.std.ShufflePlanes(ed_titles, 0, GRAY)
nc = core.std.ShufflePlanes(nced, 0, GRAY)
fixed_nc = core.std.ShufflePlanes(nced_fix, 0, GRAY)
averaged = core.std.Expr([credits_, nc, fixed_nc], 'x y - z +')
averaged_01 = core.std.ShufflePlanes([averaged, nced_fix], planes=[0,0,0], colorfamily=vs.YUV)

credits_ = core.std.ShufflePlanes(ed_titles, 1, GRAY)
nc = core.std.ShufflePlanes(nced, 1, GRAY)
fixed_nc = core.std.ShufflePlanes(nced_fix, 1, GRAY)
averaged = core.std.Expr([credits_, nc, fixed_nc], 'x y - z +')
averaged_02 = core.std.ShufflePlanes([averaged, nced_fix], planes=[0,1,2], colorfamily=vs.YUV)

credits_ = core.std.ShufflePlanes(ed_titles, 2, GRAY)
nc = core.std.ShufflePlanes(nced, 2, GRAY)
fixed_nc = core.std.ShufflePlanes(nced_fix, 2, GRAY)
averaged = core.std.Expr([credits_, nc, fixed_nc], 'x y - z +')
averaged_03 = core.std.ShufflePlanes([averaged, nced_fix], planes=[0,1,2], colorfamily=vs.YUV)

averaged_04 = core.std.ShufflePlanes([averaged_01, averaged_02, averaged_03], planes=[0, 0, 0], colorfamily=vs.YUV)

ed = nced_fix.std.Trim(0,0)+averaged_04.std.Trim(1,1938)+averaged_04.std.Trim(1938,1938)+averaged_04.std.Trim(1940,2156)
clip16 = core.resize.Lanczos(ed, format=vs.YUV420P16, matrix_in='1')
pf = core.dfttest.DFTTest(clip16, sigma=1.5, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=3, thsad=400, thsadc=380, blksize=4, overlap=2, pf=pf)
gr = core.grain.Add(den, var=0.5, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
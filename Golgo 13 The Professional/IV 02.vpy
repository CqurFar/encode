from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsutil import get_w
from vsgan import ESRGAN
from mvsfunc import ToYUV, ToRGB
from havsfunc import FastLineDarkenMOD
from vsrgtools import rgtools
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


core.num_threads = 24
core.max_cache_size = 30000

import os
os.environ['CUDA_MODULE_LOADING'] = 'LAZY'
os.environ['CUDA_FORCE_PRELOAD_LIBRARIES'] = '1'
os.environ['CUDA_AUTO_BOOST'] = '1'
os.environ['CUDA_DEVICE_MAX_CONNECTIONS'] = '32'
os.environ['CUDA_CACHE_MAXSIZE'] = '12884901888'


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Golgo 13 The Professional\IV 02.m2ts').fmtc.bitdepth(bits=16)
deint = haf.ChangeFPS(episode, fpsnum=24000, fpsden=1001)


#Фильтрация
pf = core.dfttest.DFTTest(deint, sigma=2, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=2, thsad=50, thsadc=100, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=30, cb=20, cr=20, grainy=0, grainc=0, blur_first=True)

db.fmtc.bitdepth(bits=10).set_output()
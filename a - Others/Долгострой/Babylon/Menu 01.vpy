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
episode = core.lsmas.LWLibavSource(r'E:\Работа\Babylon\Menu 01.m2ts')
episode = ToRGB(episode)
item = core.imwri.Read(r'E:\Работа\Babylon\Скрипты\Маски\Menu 01.png', alpha=True)


#Наложение
overlay = haf.Overlay(episode, item[0], mask=item.std.PropToClip('_Alpha'),mode='grainmerge')
overlay = ToYUV(overlay, matrix=1, css='420', depth=10)


#Фильтрация
pf = core.dfttest.DFTTest(overlay, sigma=1, tbsize=3, opt=3) 
den = cooldegrain.CoolDegrain(pf, tr=1, thsad=20, thsadc=0, blksize=8, overlap=4, pf=pf).std.Trim(0, 2327)

den.set_output()
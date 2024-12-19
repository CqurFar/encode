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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Yoru no Kurage wa Oyogenai\Menu 02.m2ts')
episode = ToRGB(episode)

# 2x_AniScale2_SwinIR_i16_265K, 4x_IllustrationJaNai_V1_ESRGAN_135k дескеил Hamming, постеризация 4 для фона
item = core.imwri.Read(r'E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\Menu 03.png', alpha=True)


#Наложение
overlay = haf.Overlay(episode, item[0], mask=item.std.PropToClip('_Alpha'),mode='normal')
overlay = ToYUV(overlay, matrix=1, css='420', depth=10)


#Депир
rgb_in = ToRGB(overlay, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_in, model=1, strength=1, overlap=0, tilesize=[1920, 1080], backend=vsmlrt.Backend.TRT())
yuv_out = ToYUV(dpir, matrix=1, css='420', depth=16)

overlay.fmtc.bitdepth(bits=10).set_output()
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


#Сорц FR
episode_fr = core.lsmas.LWLibavSource(source=r'E:\Работа\Golgo 13 The Professional\Film FR.m2ts').std.Trim(19, 134588)


#Сорц US
episode_us = core.lsmas.LWLibavSource(source=r'E:\Работа\Golgo 13 The Professional\Film US.m2ts')
episode_us = episode_us.std.Trim(223, 134763)
episode_us = episode_us.std.Trim(0,  7339)+episode_us.std.Trim(7341,  134540)
episode_us = episode_us.std.Trim(0,  55917)+episode_us.std.Trim(55906,  55917)+episode_us.std.Trim(55918,  134539)
episode_us = episode_us.std.Trim(0,  56090)+episode_us.std.Trim(56090,  134551)
episode_us = episode_us.std.Trim(0,  84652)+episode_us.std.Trim(84651,  84652)+episode_us.std.Trim(84653,  134552)
episode_us = episode_us.std.Trim(0,  107547)+episode_us.std.Trim(107549,  134554)
episode_us = episode_us.std.Trim(0,  121193)+episode_us.std.Trim(121195,  134553)
episode_us_fin = episode_us.std.Trim(0,  134552)+episode_us.std.Trim(134537,  134552)+episode_us.std.Trim(134552,  134552)

episode_black_in = core.lsmas.LWLibavSource(source=r'E:\Работа\Golgo 13 The Professional\Film FR.m2ts').std.Trim(0, 18)
episode_black_out = episode_us_fin.std.Trim(134537, 134569)

episode_fin = episode_black_in+episode_us_fin.std.Trim(0, 119)+episode_fr.std.Trim(120, 40905)+episode_us_fin.std.Trim(40906, 40941)+episode_fr.std.Trim(40942, 72202)+episode_us_fin.std.Trim(72203, 72262)+episode_fr.std.Trim(72263, 99712)+episode_us_fin.std.Trim(99713, 99890)+episode_fr.std.Trim(99891, 100877)+episode_us_fin.std.Trim(100878, 101017)+episode_fr.std.Trim(101018, 134536)+episode_black_out


cr = core.std.Crop(episode_fin, top=22, bottom=22)
cr.set_output()
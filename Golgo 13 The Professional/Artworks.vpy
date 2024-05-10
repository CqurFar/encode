from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsutil import get_w
from vsgan import ESRGAN
from mvsfunc import ToYUV, ToRGB
from havsfunc import FastLineDarkenMOD
from vsaa import based_aa, upscaled_sraa, Nnedi3, Eedi3, SangNom
from vsrgtools import rgtools
from vstools import join, depth
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
import limit_v2
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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Golgo 13 The Professional\Characters 01.mkv')


#Депир
rgb_in = ToRGB(episode, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_in, model=1, strength=1, overlap=0, tilesize=[1920, 1080], backend=vsmlrt.Backend.TRT())
yuv_dpir =  ToYUV(dpir, matrix=1, css='420', depth=16)


#Нейронка
ai = core.trt.Model(dpir, use_cuda_graph=True, overlap=0, tilesize=[1920, 1080], engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AstroManPlus_262k_new.engine').fmtc.bitdepth(bits=16)

sigmoidized = haf.SigmoidInverse(ai, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1920, 1080) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5)
yuv_ai = ToYUV(de_sigmoidized, matrix=1, css='420', depth=16)

mask = atf.ApplyImageMask(yuv_ai, yuv_dpir, r'E:\Работа\Golgo 13 The Professional\Скрипты\Маски\Mask Artworks.png')


#Зерно и вывод
gr = core.grain.Add(mask, var=0.2, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)
gr.fmtc.bitdepth(bits=10).set_output()
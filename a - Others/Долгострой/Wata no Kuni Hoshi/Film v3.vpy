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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Wata no Kuni Hoshi\F 01.mkv')


#Деинт
deint_01 = core.vivtc.VFM(episode, order=1, field=2, mode=5, cthresh=-1, mi=0, blockx=4, blocky=4, scthresh=8, micout=True, micmatch=2)
deint_01 = core.vivtc.VFM(deint_01, order=0, field=2, mode=5, cthresh=-1, mi=0, blockx=4, blocky=4, scthresh=8, micout=True, micmatch=2)
deint_01 = haf.Vinverse2(deint_01, sstr=0, amnt=255, chroma=True).fmtc.bitdepth(bits=32)
deint_01 = core.ftf.FixFades(deint_01, mode=0, threshold=0.002, color=[0.0, 0.0, 0.0])
deint_01 = haf.srestore(deint_01, frate=24/1.001, speed=-1, thresh=8).fmtc.bitdepth(bits=16)


#Ресайз
sigmoidized = haf.SigmoidInverse(deint_01, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 640, 480) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5).fmtc.bitdepth(bits=8)
cr = core.std.Crop(de_sigmoidized, left=16, right=4, top=50, bottom=52)
cr_16 = cr.fmtc.bitdepth(bits=16).resize.Lanczos(1772, 1080) 


#Депир + фильтрация c  маской
rgb_in = ToRGB(cr_16, matrix=6, depth=32)
dpir = vsmlrt.DPIR(rgb_in, model=1, strength=15, overlap=0, tilesize=[616, 376], backend=vsmlrt.Backend.TRT()).fmtc.bitdepth(bits=16)

sigmoidized = haf.SigmoidInverse(dpir, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 886, 540) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
yuv_out = ToYUV(de_sigmoidized, matrix=6, css='420', depth=16)


#Дегало + даркмод
deh = mvf.abcxyz(yuv_out, rad=1, ss=1)
deh = vsdehalo.fine_dehalo(yuv_out, rx=2.4, ry=2.4, brightstr=0.7, darkstr=0, thmi=30, thma=100, ss=1, edgeproc=0.5)
deh = G41Fun.MaskedDHA(deh, rx=2.2, ry=2.2, darkstr=0, brightstr=0.5, ss=1)
line_d = FastLineDarkenMOD(deh, strength=40, protection=7)


#Нейронка
rgb_in = ToRGB(yuv_out, matrix=6, depth=32)
ai = core.trt.Model(rgb_in, use_cuda_graph=True, overlap=0, tilesize=[880, 536], engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AstroManPlus_262k_new.engine').fmtc.bitdepth(bits=16)


sigmoidized = haf.SigmoidInverse(ai, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 886, 540) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
yuv_out = ToYUV(de_sigmoidized, matrix=1, css='420', depth=16)


yuv_out.fmtc.bitdepth(bits=10).set_output()
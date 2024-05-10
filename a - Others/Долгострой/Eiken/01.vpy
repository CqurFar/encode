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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Eiken\EP 01.m2ts')


#Деинт
deint_01 = core.vivtc.VFM(episode, order=1, field=2, mode=5, cthresh=-1, mi=0, blockx=4, blocky=4, scthresh=8, micout=True, micmatch=2)
deint_01 = core.vivtc.VFM(deint_01, order=0, field=2, mode=5, cthresh=-1, mi=0, blockx=4, blocky=4, scthresh=8, micout=True, micmatch=2)
deint_01 = haf.Vinverse2(deint_01, sstr=0, amnt=255, chroma=True).fmtc.bitdepth(bits=32)
deint_01 = core.ftf.FixFades(deint_01, mode=0, threshold=0.002, color=[0.0, 0.0, 0.0])
deint_01 = haf.srestore(deint_01, frate=24/1.001, speed=-1, thresh=8).fmtc.bitdepth(bits=16)


#Кроп и ресайз
sigmoidized = haf.SigmoidInverse(deint_01, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1280, 720) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5)
cr = core.std.Crop(de_sigmoidized, left=164, right=164, top=8, bottom=4).fmtc.bitdepth(bits=8)


#Депир с фильтрацией
yuv_episode = ToYUV(cr, depth=16)
clip_y = get_y(yuv_episode)
rgb_in = ToRGB(cr, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_in, model=1, strength=1, overlap=0, tilesize=[848, 624], backend=vsmlrt.Backend.TRT())
yuv_out = ToYUV(dpir, matrix=1, css='420', depth=16)

deh = mvf.abcxyz(yuv_out, rad=1, ss=1)
line_d = FastLineDarkenMOD(deh, strength=30, protection=7)
aa = HardAA.HardAA(line_d, mask='simple', mthr=0.1)


#Нейронка с маской
yuv_episode = ToYUV(aa, depth=16)
clip_y = get_y(yuv_episode)
rgb_in = ToRGB(aa, matrix=1, depth=32)
ai = core.trt.Model(rgb_in, use_cuda_graph=True, overlap=0, tilesize=[848, 624], engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AnimeJaNai_V2_Compact_36k_new.engine').fmtc.bitdepth(bits=16)

sigmoidized = haf.SigmoidInverse(ai, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 952, 708) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
yuv_out = ToYUV(de_sigmoidized, matrix=1, css='420', depth=16)

line_mask = vsmask.edge.Kirsch().edgemask(clip_y, multi=0.3).std.Maximum().std.Limiter()
mask_ai = core.std.MaskedMerge(yuv_episode, yuv_out, line_mask)


#Нейронка
yuv_episode = ToYUV(mask_ai, depth=16)
clip_y = get_y(yuv_episode)
rgb_in = ToRGB(mask_ai, matrix=1, depth=32)
ai = core.trt.Model(rgb_in, use_cuda_graph=True, overlap=0, tilesize=[848, 624], engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_Loyaldk-Keroro_650000_V1.0_new.engine').fmtc.bitdepth(bits=16)

sigmoidized = haf.SigmoidInverse(ai, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1428, 1064) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
yuv_out = ToYUV(de_sigmoidized, matrix=1, css='420', depth=16)


yuv_out.set_output()
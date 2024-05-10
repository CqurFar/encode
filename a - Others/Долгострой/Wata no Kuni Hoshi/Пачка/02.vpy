from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsutil import get_w
from vsgan import ESRGAN
from mvsfunc import ToYUV, ToRGB
from havsfunc import FastLineDarkenMOD
from vsrgtools import contrasharpening
from vsdenoise import MotionMode
from vsmask.util import inpand
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
import vsdeinterlace
import dhh


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


#Нейронка
rgb_in_01 = ToRGB(cr, matrix=6, depth=32)
ai_01 = core.trt.Model(rgb_in_01, use_cuda_graph=True, overlap=0, tilesize=[616, 376], engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\4x_OLDIES_ALTERNATIVE_FINAL_new.engine').fmtc.bitdepth(bits=16)
ai_01 = core.timecube.Cube(ai_01, cube=r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\luts\4x_OLDIES_ALTERNATIVE_FINAL.cube')


sigmoidized = haf.SigmoidInverse(ai_01, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 886, 540) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
yuv_out_01 = ToYUV(de_sigmoidized, matrix=1, css='420', depth=16)


#Нейронка на линии
yuv_episode = ToYUV(yuv_out_01, depth=16)
clip_y = get_y(yuv_episode)
rgb_in_02 = ToRGB(yuv_out_01, matrix=6, depth=32)
ai_02 = core.trt.Model(rgb_in_02, use_cuda_graph=True, overlap=0, tilesize=[616, 376], engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_LD-Anime_Compact_330k_net_g_new.engine').fmtc.bitdepth(bits=16)

sigmoidized = haf.SigmoidInverse(ai_02, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 886, 540) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
yuv_out_02 = ToYUV(de_sigmoidized, matrix=1, css='420', depth=16)

line_mask = vsmask.edge.Tritical().edgemask(clip_y, multi=5).std.Maximum().std.Limiter().std.Minimum(coordinates=[7, 7, 7, 7, 7, 7, 7, 7])
mask_ai = core.std.MaskedMerge(yuv_episode, yuv_out_02, line_mask)


#Депир и греин
rgb_in_03 = ToRGB(mask_ai, matrix=6, depth=32)
dpir = vsmlrt.DPIR(rgb_in_03, model=1, strength=3, overlap=0, tilesize=[616, 376], backend=vsmlrt.Backend.TRT())
yuv_out_03 = ToYUV(dpir, matrix=1, css='420', depth=16)
gr = core.grain.Add(yuv_out_03, var=2, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0).std.Trim(87, 138584)


gr.fmtc.bitdepth(bits=10).set_output()
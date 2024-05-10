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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Eiken\EP 01.m2ts')


#Деинт
deint_01 = core.vivtc.VFM(episode, order=1, field=2, mode=5, cthresh=-1, mi=0, blockx=4, blocky=4, scthresh=8, micout=True, micmatch=2)
deint_01 = core.vivtc.VFM(deint_01, order=0, field=2, mode=5, cthresh=-1, mi=0, blockx=4, blocky=4, scthresh=8, micout=True, micmatch=2)
deint_01 = haf.Vinverse2(deint_01, sstr=0, amnt=255, chroma=True).fmtc.bitdepth(bits=32)
deint_01 = core.ftf.FixFades(deint_01, mode=0, threshold=0.002, color=[0.0, 0.0, 0.0])
deint_01 = haf.srestore(deint_01, frate=24/1.001, speed=-1, thresh=8).fmtc.bitdepth(bits=16)


#Кроп + ресайз
cr = core.std.Crop(deint_01, left=250, right=254, top=12, bottom=8)
sigmoidized = haf.SigmoidInverse(cr, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 962, 720) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5)


#Депир с фильтрацией
rgb_in = ToRGB(de_sigmoidized, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_in, model=1, strength=2, overlap=0, tilesize=[848, 624], backend=vsmlrt.Backend.TRT())
yuv_out = ToYUV(dpir, matrix=1, css='420', depth=16)

pf = core.dfttest.DFTTest(yuv_out, sigma=1, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=20, cb=15, cr=15, grainy=0, grainc=0, blur_first=False)
deh_01 = vsdehalo.fine_dehalo(db, rx=2.4, ry=2.4, darkstr=0, brightstr=0.4, thmi=30, thma=100)
deh_02 = G41Fun.MaskedDHA(deh_01, rx=2.3, ry=2.3, darkstr=0, brightstr=0.3)
aa = HardAA.HardAA(deh_02, mask='simple', mthr=0.1)
line_d = FastLineDarkenMOD(aa, strength=30, protection=7)


#Нейронки помесь
rgb_in = ToRGB(line_d, matrix=1, depth=32)

ai_01 = core.trt.Model(rgb_in, use_cuda_graph=True, overlap=0, tilesize=[960, 720], engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_KemonoScale_v2_new.engine')
color_01 = core.timecube.Cube(ai_01, cube=r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\luts\2x_KemonoScale_v2.cube').fmtc.bitdepth(bits=16)

ai_02 = core.trt.Model(rgb_in, use_cuda_graph=True, overlap=0, tilesize=[960, 720], engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\4x_OLDIES_290000_G_FINAL_interp_03_new.engine')
color_02 = core.timecube.Cube(ai_02, cube=r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\luts\4x_OLDIES_290000_G_FINAL_interp_03.cube').fmtc.bitdepth(bits=16)
sigmoidized = haf.SigmoidInverse(color_02, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1924, 1440) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 

ai_expr = core.std.Expr([color_01, de_sigmoidized], 'x 0.70 * y 0.30 * +').fmtc.bitdepth(bits=16)

sigmoidized = haf.SigmoidInverse(ai_expr, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1416, 1060) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
yuv_out = ToYUV(de_sigmoidized, matrix=1, css='420', depth=16)

deh = vsdehalo.fine_dehalo(yuv_out, rx=2.4, ry=2.4, darkstr=0, brightstr=0.4, thmi=30, thma=100)
gr = core.grain.Add(deh, var=0.8, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)
gr.set_output()
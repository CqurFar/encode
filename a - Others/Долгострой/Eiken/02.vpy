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
deh_00 = mvf.abcxyz(db, rad=1.5, ss=1.5)
deh_01 = vsdehalo.fine_dehalo(deh_00, rx=2.4, ry=2.4, darkstr=0, brightstr=0.4, thmi=30, thma=100)
deh_02 = G41Fun.MaskedDHA(deh_01, rx=2.3, ry=2.3, darkstr=0, brightstr=0.3)
line_d = FastLineDarkenMOD(deh_02, strength=30, protection=7)


#Нейронка с маской
yuv_episode = ToYUV(line_d, depth=16)
clip_y = get_y(yuv_episode)
rgb_in = ToRGB(line_d, matrix=1, depth=32)
ai = core.trt.Model(rgb_in, use_cuda_graph=True, overlap=0, tilesize=[720, 536], engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\1x_GainRESV3_Passive_new.engine')
yuv_out = ToYUV(ai, matrix=1, css='420', depth=16)

line_mask = vsmask.edge.Kirsch().edgemask(clip_y, multi=1).std.Minimum(coordinates=[4, 4, 4, 4, 4, 4, 4, 4])
mask_ai = core.std.MaskedMerge(yuv_episode, yuv_out, line_mask)


#Нейронка с маской
yuv_episode = ToYUV(mask_ai, depth=16)
clip_y = get_y(yuv_episode)
rgb_in = ToRGB(mask_ai, matrix=1, depth=32)
ai = core.trt.Model(rgb_in, use_cuda_graph=True, overlap=0, tilesize=[848, 624], engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_QDCU_new.engine').fmtc.bitdepth(bits=16)
color = core.timecube.Cube(ai, cube=r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\luts\2x_QDCU.cube')

sigmoidized = haf.SigmoidInverse(color, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 962, 720) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
yuv_out = ToYUV(de_sigmoidized, matrix=1, css='420', depth=16)


mask_ai.set_output()
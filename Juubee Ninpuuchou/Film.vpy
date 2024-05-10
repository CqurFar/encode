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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Juubee Ninpuuchou\Film.m2ts')


#Депир с фильтрацией
rgb_in = ToRGB(episode, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_in, model=1, strength=1, overlap=0, tilesize=[1920, 1080], backend=vsmlrt.Backend.TRT())
yuv_out = ToYUV(dpir, matrix=1, css='420', depth=16)

db = core.neo_f3kdb.Deband(yuv_out, y=15, cb=10, cr=10, grainy=0, grainc=0, blur_first=False)
cr = core.std.Crop(db, left=230, right=230)


#Нейронка с маской
yuv_episode = ToYUV(cr, depth=16)
clip_y = get_y(yuv_episode)
rgb_in = ToRGB(cr, matrix=1, depth=32)
ai = core.trt.Model(rgb_in, use_cuda_graph=True, overlap=0, tilesize=[1460, 1080], engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2xGT-v2-evA-01_new.engine').fmtc.bitdepth(bits=16)

sigmoidized = haf.SigmoidInverse(ai, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1460, 1080) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
yuv_out = ToYUV(de_sigmoidized, matrix=1, css='420', depth=16)

line_mask = vsmask.edge.Kirsch().edgemask(clip_y, multi=0.75).std.Maximum(coordinates=[4, 4, 4, 4, 4, 4, 4, 4])
mask_ai = core.std.MaskedMerge(yuv_episode, yuv_out, line_mask)


#Зерно и вывод
deh = vsdehalo.fine_dehalo(mask_ai, rx=2.2, ry=2.2, darkstr=0, brightstr=0.5, thmi=30, thma=100, ss=1, edgeproc=0.5)
gr = core.grain.Add(deh, var=1.3, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=123456789, constant=False, opt=0).std.Trim(0, 131300)
gr.fmtc.bitdepth(bits=10).set_output()
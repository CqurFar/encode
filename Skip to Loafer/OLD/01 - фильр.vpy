from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsutil import get_w
from vsgan import ESRGAN
from mvsfunc import ToYUV
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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Skip to Loafer\EP 01.m2ts')


#Фильтрация
clip16 = core.resize.Lanczos(episode, format=vs.YUV420P16, matrix_s='709')
dpir  = lvsfunc.dpir(clip16, strength=2, mode='denoise', cuda=True, matrix=1)
db = core.neo_f3kdb.Deband(dpir, y=20, cb=10, cr=10, grainy=0, grainc=0, blur_first=False)


#Реверс аа
clip = db

clip_y = get_y(clip)
line_mask = vsmask.edge.Tritical().edgemask(clip_y,multi=2).std.Maximum().std.Limiter()
descaled = vskernels.Lanczos.descale(clip_y, width=get_w(828), height=828)

rgbs_in = core.resize.Lanczos(descaled, format=vs.RGBS, matrix_in='1')
ai = core.trt.Model(rgbs_in , engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\1x_GainresV4_128_828.engine')
gray8_out = core.resize.Lanczos(ai, format=vs.GRAY16,  matrix_s="709")

def eedi3_sr(clip: vs.VideoNode) -> vs.VideoNode:
    eedi3mode = core.eedi3m.EEDI3CL(clip, 1, False, sclip=clip, alpha=0.125, beta=0.25, vthresh0=12, vthresh1=24) 
    return eedi3mode

aiclip = core.nnedi3cl.NNEDI3CL(gray8_out, field=1, dh=True, dw=True, nsize=0, nns=4, qual=2, pscrn=1).resize.Lanczos(src_top=-0.5,src_left=-0.5) 

t1 = core.std.Transpose(aiclip)
t1 = eedi3_sr(t1)
t2 = core.std.Transpose(t1)
t2 = eedi3_sr(t2)
t2 = vskernels.Spline64().scale(t2,clip.width,clip.height)
masked = core.std.MaskedMerge(clip_y, t2, line_mask)
t2 = core.std.ShufflePlanes([masked, clip], planes=[0, 1, 2], colorfamily=vs.YUV)


#Нейронка
rgbs_in = core.resize.Lanczos(t2, format=vs.RGBS, matrix_in='1')
yuv_episode = ToYUV(rgbs_in)
clip_y = get_y(yuv_episode)
ai = core.trt.Model(rgbs_in , engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_Ani4K_Compact_35000.engine')

linear = core.resize.Lanczos(ai, format=vs.RGBS).fmtc.bitdepth(bits=16)
sigmoidized = haf.SigmoidInverse(linear, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1920, 1080) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
rgbs_out = core.resize.Lanczos(de_sigmoidized, format=vs.RGBS)
yuv_ai = ToYUV(rgbs_out)
line_mask = vsmask.edge.Tritical().edgemask(clip_y, multi=2).std.Maximum().std.Limiter()
mask_ai = core.std.MaskedMerge(yuv_episode, yuv_ai, line_mask)

ai_expr = core.std.Expr([yuv_episode, mask_ai], 'x 0.20 * y 0.80 * +')


ai_expr.fmtc.bitdepth(bits=10).set_output()
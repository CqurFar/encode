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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Horimiya\NCOP 01.m2ts')
clip = episode


#Реверс аа
clip_y = get_y(clip)
line_mask = vsmask.edge.Kroon().edgemask(clip_y,multi=2).std.Maximum().std.Limiter()
descaled = vskernels.Lanczos.descale(clip_y, width=get_w(873), height=873)

def eedi3_sr(clip: vs.VideoNode) -> vs.VideoNode:
    eedi3mode = core.eedi3m.EEDI3CL(clip, 1, False, sclip=clip, alpha=0.125, beta=0.25, vthresh0=12, vthresh1=24) 
    return eedi3mode

aiclip = core.nnedi3cl.NNEDI3CL(descaled, field=1, dh=True, dw=True, nsize=0, nns=4, qual=2, pscrn=2).resize.Lanczos(src_top=-0.5,src_left=-0.5) 
t1 = core.std.Transpose(aiclip)
t1 = eedi3_sr(t1)
t2 = core.std.Transpose(t1)
t2 = eedi3_sr(t2)
t2 = vskernels.Spline64().scale(t2,clip.width,clip.height)
masked = core.std.MaskedMerge(clip_y, t2, line_mask)
t2 = core.std.ShufflePlanes([masked, clip], planes=[0, 1, 2], colorfamily=vs.YUV)


#Нейронка
rgbs_in = core.resize.Lanczos(t2, format=vs.RGBS, matrix_in='1')
ai = core.trt.Model(rgbs_in , engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2xGT-v2-evA-01.engine')

linear = core.resize.Lanczos(ai, format=vs.RGBS).fmtc.bitdepth(bits=16)
sigmoidized = haf.SigmoidInverse(linear, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1920, 1080) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
rgbs_out = core.resize.Lanczos(de_sigmoidized, format=vs.RGBS)

ai_expr = core.std.Expr([rgbs_in, rgbs_out], 'x 0.70 * y 0.30 * +')
dpir  = lvsfunc.dpir(ai_expr, strength=1, mode='denoise', cuda=True, matrix=1)
mg = ai_expr.std.Trim(0,230)+dpir.std.Trim(231,257)+ai_expr.std.Trim(258,1232)+dpir.std.Trim(1233,1437)+ai_expr.std.Trim(1438,1765)+dpir.std.Trim(1766,1873)+ai_expr.std.Trim(1874,2000)+dpir.std.Trim(2001,2150)+ai_expr.std.Trim(2151,2206)


#Остальная фильтрация
clip16 = core.resize.Lanczos(mg, format=vs.YUV420P16, matrix_s='709')
pf = core.dfttest.DFTTest(clip16, sigma=0.5, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=1, thsad=28, thsadc=20, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=20, cb=10, cr=10, grainy=0, grainc=0, blur_first=False)

Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=False)
Filtered = core.std.MaskedMerge(db, clip16, Mask)


#Зерно и вывод
sh = core.cas.CAS(Filtered, sharpness=0.3, opt=0)
deh = vsdehalo.fine_dehalo(sh, ref=None, rx=2.4, ry=2.4, darkstr=0, brightstr=0.7, thmi=30, thma=100, excl=True, ss=1, edgeproc=0.5)
gr = core.grain.Add(deh, var=0.5, uvar=0.3, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)
gr.fmtc.bitdepth(bits=10).set_output()
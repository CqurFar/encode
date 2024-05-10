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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Horimiya\EP 03.m2ts')
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


#Склейка OP
op_titles = core.std.Trim(episode, 3357, 5514)
ncop = core.lsmas.LWLibavSource(r'E:\Работа\Horimiya\NCOP 01.m2ts').std.Trim(24, 2181).fmtc.bitdepth(bits=8)
ncop_fix = core.raws.Source(r'E:\Работа\Horimiya\NCOP 01.y4m').std.Trim(24, 2181).fmtc.bitdepth(bits=8)
op = atf.ApplyCredits(op_titles, ncop, ncop_fix).resize.Lanczos(format=vs.YUV420P16)


#Склейка ED
ed_titles = core.std.Trim(episode, 31984, 34141)
nced = core.lsmas.LWLibavSource(r'E:\Работа\Horimiya\NCED.m2ts').std.Trim(24, 2180).fmtc.bitdepth(bits=8)
nced_fix = core.lsmas.LWLibavSource(r'E:\Работа\Horimiya\NCED.y4m').std.Trim(24, 2180).fmtc.bitdepth(bits=8)

credits_ = core.std.ShufflePlanes(ed_titles, 0, GRAY)
nc = core.std.ShufflePlanes(nced, 0, GRAY)
fixed_nc = core.std.ShufflePlanes(nced_fix, 0, GRAY)
averaged = core.std.Expr([credits_, nc, fixed_nc], 'x y - z +')
averaged_01 = core.std.ShufflePlanes([averaged, nced_fix], planes=[0,0,0], colorfamily=vs.YUV)

credits_ = core.std.ShufflePlanes(ed_titles, 1, GRAY)
nc = core.std.ShufflePlanes(nced, 1, GRAY)
fixed_nc = core.std.ShufflePlanes(nced_fix, 1, GRAY)
averaged = core.std.Expr([credits_, nc, fixed_nc], 'x y - z +')
averaged_02 = core.std.ShufflePlanes([averaged, nced_fix], planes=[0,1,2], colorfamily=vs.YUV)

credits_ = core.std.ShufflePlanes(ed_titles, 2, GRAY)
nc = core.std.ShufflePlanes(nced, 2, GRAY)
fixed_nc = core.std.ShufflePlanes(nced_fix, 2, GRAY)
averaged = core.std.Expr([credits_, nc, fixed_nc], 'x y - z +')
averaged_03 = core.std.ShufflePlanes([averaged, nced_fix], planes=[0,1,2], colorfamily=vs.YUV)

averaged_04 = core.std.ShufflePlanes([averaged_01, averaged_02, averaged_03], planes=[0, 0, 0], colorfamily=vs.YUV)

ed = nced_fix.std.Trim(0,0)+averaged_04.std.Trim(1,1938)+averaged_04.std.Trim(1938,1938)+averaged_04.std.Trim(1940,2157)
ed_16 = core.resize.Lanczos(ed, format=vs.YUV420P16, matrix_in='1')
ed_pf = core.dfttest.DFTTest(ed_16, sigma=1.5, tbsize=3, opt=3)
ed_den = cooldegrain.CoolDegrain(ed_pf, tr=3, thsad=400, thsadc=380, blksize=4, overlap=2, pf=ed_pf)
ed_gr = core.grain.Add(ed_den, var=0.5, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)


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


#Остальная фильтрация
clip16 = core.resize.Lanczos(dpir, format=vs.YUV420P16, matrix_s='709')
pf = core.dfttest.DFTTest(clip16, sigma=0.5, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=1, thsad=28, thsadc=20, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=30, cb=15, cr=15, grainy=0, grainc=0, blur_first=True)

Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=False)
Filtered = core.std.MaskedMerge(db, clip16, Mask)


#Зерно и вывод
sh = core.cas.CAS(Filtered, sharpness=0.3, opt=0)
deh = vsdehalo.fine_dehalo(sh, ref=None, rx=2.2, ry=2.2, darkstr=0, brightstr=0.5, thmi=30, thma=100, excl=True, ss=1, edgeproc=0.5)
gr = core.grain.Add(deh, var=0.5, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)

mg = gr.std.Trim(0,3356)+op+gr.std.Trim(5515,31983)+ed_gr+gr.std.Trim(34142,34166)
mg.fmtc.bitdepth(bits=10).set_output()
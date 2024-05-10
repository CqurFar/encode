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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Fuufu Ijou, Koibito Miman\EP 01.mkv')
clip = episode


#Реверс аа
clip_y = get_y(clip)
line_mask = vsmask.edge.Kroon().edgemask(clip_y,multi=2).std.Maximum().std.Limiter()
descaled = vskernels.Lanczos.descale(clip_y, width=get_w(956), height=956)

def eedi3_sr(clip: vs.VideoNode) -> vs.VideoNode:
    eedi3mode = core.eedi3m.EEDI3CL(clip, 1, False, sclip=clip, alpha=0.125, beta=0.25, vthresh0=12, vthresh1=24) 
    return eedi3mode

aiclip = core.nnedi3cl.NNEDI3CL(clip_y, field=1, dh=True, dw=True, nsize=0, nns=4, qual=2, pscrn=2).resize.Bicubic(src_top=-0.5,src_left=-0.5) 
t1 = core.std.Transpose(aiclip)
t1 = eedi3_sr(t1)
t2 = core.std.Transpose(t1)
t2 = eedi3_sr(t2)
t2 = vskernels.Spline64().scale(t2,clip.width,clip.height)
masked = core.std.MaskedMerge(clip_y, t2, line_mask)
t2 = core.std.ShufflePlanes([masked, clip], planes=[0, 1, 2], colorfamily=vs.YUV)


#Склейка ED
ed_titles = core.std.Trim(episode, 32152, 34310)
nced = core.lsmas.LWLibavSource(source=r'E:\Работа\Fuufu Ijou, Koibito Miman\NCED.mkv').std.Trim(24, 2182).fmtc.bitdepth(bits=8)
nced_fix = core.raws.Source(r'E:\Работа\Fuufu Ijou, Koibito Miman\NCED.y4m').std.Trim(24, 2182).fmtc.bitdepth(bits=8)
ed = atf.ApplyCredits(ed_titles, nced, nced_fix).resize.Lanczos(format=vs.YUV420P16)


#Нейронка
rgbs = core.resize.Lanczos(t2, format=vs.RGBS, matrix_in='1')
ai = core.trt.Model(rgbs , engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2xGT-v2-evA-01.engine').resize.Lanczos(width=1920, height=1080)
ai_expr = core.std.Expr([rgbs, ai], 'x 0.60 * y 0.40 * +')
dpir  = lvsfunc.dpir(ai_expr, strength=1, mode='denoise', cuda=True, matrix=1)


#Остальная фильтрация
clip16 = core.resize.Lanczos(dpir, format=vs.YUV420P16, matrix_s='709')
pf = core.dfttest.DFTTest(clip16, sigma=0.5, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=2, thsad=40, thsadc=38, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=20, cb=10, cr=10, grainy=0, grainc=0, blur_first=False)


#Зерно и вывод
gr = core.grain.Add(db, var=0.5, uvar=0.1, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)

mg = gr.std.Trim(0,32151)+ed+gr.std.Trim(34311,34814)
mg.fmtc.bitdepth(bits=10).set_output()
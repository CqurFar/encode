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
# 1963 2085 2149 2163

#Сорц
episode_01 = core.lsmas.LWLibavSource(source=r'E:\Работа\Horimiya\NCED.m2ts')
episode_02 = core.znedi3.nnedi3(episode_01, field=0, dh=False, nsize=0, nns=4, qual=1, etype=0, pscrn=0, opt=0, exp=0)
episode_2085 = ToYUV(core.imwri.Read(r'E:\Работа\Horimiya\Скрипты\Маски\2085.png'),css='420')
episode_2085 = core.std.AssumeFPS(episode_2085, episode_01)
episode_2149 = ToYUV(core.imwri.Read(r'E:\Работа\Horimiya\Скрипты\Маски\2149.png'),css='420')
episode_2149 = core.std.AssumeFPS(episode_2149, episode_01)
episode_2163 = ToYUV(core.imwri.Read(r'E:\Работа\Horimiya\Скрипты\Маски\2163.png'),css='420')
episode_2163 = core.std.AssumeFPS(episode_2163, episode_01)
clip = episode_02.std.Trim(0,35)+episode_01.std.Trim(36,1962)+episode_01.std.Trim(1962,1962)+episode_01.std.Trim(1964,2084)+episode_2085+episode_01.std.Trim(2086,2148)+episode_2149+episode_01.std.Trim(2150,2162)+episode_2163+episode_01.std.Trim(2164,2240)


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
rgbs = core.resize.Lanczos(t2, format=vs.RGBS, matrix_in='1')
yuv_episode = ToYUV(rgbs)
clip_y = get_y(yuv_episode)
ai = core.trt.Model(rgbs, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\1x_GainRESV3_Passive.engine')
yuv_ai = ToYUV(ai)
line_mask = vsmask.edge.Prewitt().edgemask(clip_y, multi=2).std.Maximum().std.Limiter()
mask_ai = core.std.MaskedMerge(yuv_episode, yuv_ai, line_mask)


#Остальная фильтрация
clip16 = core.resize.Lanczos(mask_ai, format=vs.YUV420P16, matrix_s='709')
dpir  = lvsfunc.dpir(clip16, strength=1, mode='denoise', cuda=True, matrix=1)
pf = core.dfttest.DFTTest(dpir, sigma=0.5, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=1, thsad=28, thsadc=20, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=30, cb=15, cr=15, grainy=0, grainc=0, blur_first=True)

Mask = atf.retinex_edgemask(clip16, sigma=0.1, draft=False, opencl=False)
Filtered = core.std.MaskedMerge(db, clip16, Mask)


#Зерно и вывод
deh = vsdehalo.fine_dehalo(Filtered, ref=None, rx=2.4, ry=2.4, darkstr=0, brightstr=0.7, thmi=30, thma=100, excl=True, ss=1, edgeproc=0.5)
gr = core.grain.Add(deh, var=0.5, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)
gr.fmtc.bitdepth(bits=10).set_output()
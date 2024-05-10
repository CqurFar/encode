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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Babylon\NCOP 01.m2ts').fmtc.bitdepth(bits=16)


#Депир
rgb_in = ToRGB(episode, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_in, model=1, strength=3, overlap=0, tilesize=[1920, 1080], backend=vsmlrt.Backend.TRT())
yuv_out = ToYUV(dpir, matrix=1, css='420', depth=16)


#Реверс аа
clip = episode
clip_y = get_y(episode)
mask = vsmask.edge.Tritical().edgemask(clip_y,multi=7).std.Maximum().std.Limiter()
descaled = vskernels.Lanczos.descale(clip_y, width=get_w(720), height=720)

def eedi3_sr(clip: vs.VideoNode) -> vs.VideoNode:
    eedi3mode = core.eedi3m.EEDI3CL(clip, 1, False, sclip=clip, alpha=0.125, beta=0.25, vthresh0=12, vthresh1=24) 
    return eedi3mode

aiclip = core.nnedi3cl.NNEDI3CL(descaled, field=1, dh=True, dw=True, nsize=0, nns=4, qual=2, pscrn=1).resize.Lanczos(src_top=-0.5,src_left=-0.5) 
t1 = core.std.Transpose(aiclip)
t1 = eedi3_sr(t1)
t2 = core.std.Transpose(t1)
t2 = eedi3_sr(t2)
t2 = vskernels.Spline64().scale(t2,clip.width,clip.height)
masked = core.std.MaskedMerge(clip_y, t2, mask)
t2 = core.std.ShufflePlanes([masked, clip], planes=[0, 1, 2], colorfamily=vs.YUV)


#Дегало
deh_01 = vsdehalo.fine_dehalo(t2, rx=2.5, ry=2.5, brightstr=0.5, darkstr=0.5, thmi=30, thma=100, ss=1, edgeproc=0.5)
deh_02 = vsdehalo.fine_dehalo(deh_01, rx=2.4, ry=2.4, brightstr=0.4, darkstr=0.4, thmi=30, thma=100, ss=1, edgeproc=0.5)

dha_01 = G41Fun.MaskedDHA(deh_02, rx=2.3, ry=2.3, brightstr=0.4,  darkstr=0.3)
dha_02 = G41Fun.MaskedDHA(dha_01, rx=2.2, ry=2.2, brightstr=0.3,  darkstr=0.2)

deh_03 = mvf.abcxyz(dha_02, rad=1, ss=1)


#Зерно и вывод
gr = core.grain.Add(deh_03, var=0.3, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)

mg = yuv_out.std.Trim(0, 47)+gr.std.Trim(48, 766)+yuv_out.std.Trim(767, 791)
mg.fmtc.bitdepth(bits=10).set_output()
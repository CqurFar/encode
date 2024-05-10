from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsgan import ESRGAN
from mvsfunc import ToYUV
from vstools import scale_8bit
from vsrgtools import box_blur
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


episode = core.lsmas.LWLibavSource(source=r'E:\Аниме\Глейпнир\Bonus\NC\00006.m2ts')


def alisa(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.0, kernel='bicubic', descale_height=720) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(episode, 1, GRAY)
    v = core.std.ShufflePlanes(episode, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1, useCL=True)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1, useCL=True)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1, useCL=True)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], episode.format.color_family)
    return mixyuv


def alisa240(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.0, kernel='bicubic', descale_height=240) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(episode, 1, GRAY)
    v = core.std.ShufflePlanes(episode, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1, useCL=True)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1, useCL=True)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1, useCL=True)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], episode.format.color_family)
    return mixyuv


pipi = alisa(episode)
hihi = alisa240(episode)

mg = episode.std.Trim(0, 152)+pipi.std.Trim(153, 172)+episode.std.Trim(173, 470)+pipi.std.Trim(471, 1912)+episode.std.Trim(1913, 2066)+pipi.std.Trim(2067, 2117)+hihi.std.Trim(2118, 2123)+pipi.std.Trim(2124, 2127)+episode.std.Trim(2128, 2207)

mg = fvf.rfs(mg, core.neo_f3kdb.Deband(mg, y=80, cb=80, cr=80, grainy=0, grainc=0, dynamic_grain=False, blur_first=True), "[153 321]")
mg = fvf.rfs(mg, core.neo_f3kdb.Deband(mg, y=80, cb=80, cr=80, grainy=0, grainc=0, dynamic_grain=False, blur_first=True), "[445 455]")

clip16 = core.resize.Lanczos(mg, format=vs.YUV420P16, matrix_in="1")
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=30, cb=30, cr=30, grainy=0, grainc=0, blur_first=True)


gr = core.grain.Add(db, var=1, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
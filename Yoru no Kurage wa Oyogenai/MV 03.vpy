from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsaa import based_aa, upscaled_sraa, Nnedi3, Eedi3, SangNom
from havsfunc import FastLineDarkenMOD
from mvsfunc import ToYUV, ToRGB
from vsutil import get_y, get_w
from vstools import join, depth
import atomchtools as atf
import vapoursynth as vs
from vsgan import ESRGAN
import finedehalo as fd
import havsfunc as haf
import muvsfunc as mvf
import fvsfunc as fvf
import mvsfunc as mvs
import descale as dsc
import beatricetools
import cooldegrain
import MCDenoise 
import finesharp
import vsdenoise
import vskernels
import vsdehalo
import insaneAA
import vsTAAmbk
import lostfunc
import lvsfunc
import G41Fun
import HardAA
import vsmask
import vsmlrt
import limit
import vsgan
import dhh
import ccd
import xaa
import os


#Техническое
core.num_threads = 24
core.max_cache_size = 30000

os.environ["CUDA_MODULE_LOADING"] = "LAZY"
os.environ["CUDA_FORCE_PRELOAD_LIBRARIES"] = "1"
os.environ["CUDA_AUTO_BOOST"] = "1"
os.environ["CUDA_DEVICE_MAX_CONNECTIONS"] = "32"
os.environ["CUDA_CACHE_MAXSIZE"] = "12884901888"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"




#Сорц
episode = core.lsmas.LWLibavSource(source=r"E:\Работа\Yoru no Kurage wa Oyogenai\MV 03.mkv")
episode_16 = episode.fmtc.bitdepth(bits=16)


#Дегрэин
pf = core.dfttest.DFTTest(episode_16, sigma=1, tbsize=1, opt=3)
den = cooldegrain.CoolDegrain(episode_16, tr=3, thsad=100, thsadc=100, bits=16, blksize=8, overlap=4, pf=episode_16)

osup = den.mv.Super(pel=4, sharp=2, rfilter=2)
bv1 = osup.mv.Analyse(isb=True, delta=1, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
bv2 = osup.mv.Analyse(isb=True, delta=2, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
bv3 = osup.mv.Analyse(isb=True, delta=3, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
fv1 = osup.mv.Analyse(isb=False, delta=1, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
fv2 = osup.mv.Analyse(isb=False, delta=2, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
fv3 = osup.mv.Analyse(isb=False, delta=3, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
all = core.mv.Degrain3(den, super=osup, mvbw=bv1, mvfw=fv1, mvbw2=bv2, mvfw2=fv2, mvbw3=bv3, mvfw3=fv3, thsad=200, thsadc=200, plane=4)

rgb_dp = ToRGB(all, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_dp, model=1, strength=3, overlap=0, tilesize=[1920, 1080], backend=vsmlrt.Backend.TRT())
yuv_dp = ToYUV(dpir, matrix=1, css="420", depth=16)
db = core.neo_f3kdb.Deband(yuv_dp, y=20, cb=15, cr=15, grainy=0, grainc=0, blur_first=False)
gr = core.grain.Add(db, var=4, uvar=3, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)

mg_01 = episode_16.std.Trim(0, 2160)+gr.std.Trim(2161, 2229)


# Чёрный
black_36 = core.std.BlankClip(color=[0, 0, 0], width=1920, height=1080, length=36, fpsnum=24000, fpsden=1001)
yuv_black_36 = ToYUV(black_36, matrix=1, css="420", depth=16)

black_61 = core.std.BlankClip(color=[0, 0, 0], width=1920, height=1080, length=61, fpsnum=24000, fpsden=1001)
yuv_black_61 = ToYUV(black_61, matrix=1, css="420", depth=16)


# Вывод
mg_02 = yuv_black_36+mg_01.std.Trim(36, 2168)+yuv_black_61
mg_02.fmtc.bitdepth(bits=10).set_output()
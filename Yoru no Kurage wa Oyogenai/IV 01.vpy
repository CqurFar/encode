from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from havsfunc import FastLineDarkenMOD
from mvsfunc import ToYUV, ToRGB
import atomchtools as atf
import vapoursynth as vs
from vsutil import get_y
from vsutil import get_w
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
episode = core.lsmas.LWLibavSource(source=r"E:\Работа\Yoru no Kurage wa Oyogenai\IV 01.m2ts")

#Деинт и дескейл
deint = core.vivtc.VFM(episode, order=0, field=2, mode=5, cthresh=-1, mi=0, blockx=4, blocky=4, scthresh=8, micout=True, micmatch=2)
deint = haf.Vinverse2(deint, sstr=0, amnt=255, chroma=True)
deint = core.vivtc.VDecimate(deint)

episode_16 = deint.fmtc.bitdepth(bits=16)


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
dpir = vsmlrt.DPIR(rgb_dp, model=1, strength=2, overlap=0, tilesize=[1920, 1080], backend=vsmlrt.Backend.TRT())
yuv_dp = ToYUV(dpir, matrix=1, css="420", depth=16)
db = core.neo_f3kdb.Deband(yuv_dp, y=20, cb=15, cr=15, grainy=0, grainc=0, blur_first=False)

clip_y = get_y(all)
mask_dp = vsmask.edge.Kirsch().edgemask(clip_y, multi=7).std.Minimum().std.Limiter().std.BoxBlur(1, 1, 1)
masked_dp = core.std.MaskedMerge(db, episode_16, mask_dp)
sh = core.cas.CAS(masked_dp, sharpness=0.2, opt=0)
gr = core.grain.Add(sh, var=1, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)


# Вывод
mg = episode_16.std.Trim(0, 23)+gr.std.Trim(24, 34643)+episode_16.std.Trim(34644, 34799)
mg.fmtc.bitdepth(bits=10).set_output()
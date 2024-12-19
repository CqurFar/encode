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




# Сорц
episode = core.lsmas.LWLibavSource(source=r"E:\Работа\Yoru no Kurage wa Oyogenai\PV 01.mkv")
episode_16 = episode.fmtc.bitdepth(bits=16)


#Дегрэин
pf = core.dfttest.DFTTest(episode_16, sigma=1, tbsize=1, opt=3)
den = cooldegrain.CoolDegrain(episode_16, tr=3, thsad=100, thsadc=100, bits=16, blksize=8, overlap=4, pf=pf)

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
db = core.neo_f3kdb.Deband(yuv_dp, y=30, cb=20, cr=20, grainy=0, grainc=0, blur_first=True)
rgb_db = ToRGB(db,  matrix=1, depth=32)


# Зерно
gr = core.std.BlankClip(db, width=1280, height=720, format=vs.GRAYS, length=db.num_frames, color=[0])
gr = core.grain.Add(gr, var=0.5, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0).resize.Bilinear(1920, 1080)
rgb_gr = ToRGB(gr, matrix=1, depth=32)
merged_gr = haf.Overlay(rgb_db, rgb_gr, mode="screen")
yuv_gr = ToYUV(merged_gr, matrix=1, css="420", depth=16)

mg = episode_16.std.Trim(0, 23)+yuv_gr.std.Trim(24, 110)+episode_16.std.Trim(111, 163)+yuv_gr.std.Trim(164, 245)+episode_16.std.Trim(246, 281)+yuv_gr.std.Trim(282, 330)+episode_16.std.Trim(331, 373)+yuv_gr.std.Trim(374, 453)+episode_16.std.Trim(454, 498)+yuv_gr.std.Trim(499, 884)+episode_16.std.Trim(885, 1179)


# Нейронка
rgb_text = ToRGB(mg, matrix=1, depth=32)
ai_text = core.trt.Model(rgb_text, use_cuda_graph=True, overlap=0, tilesize=[1920, 1080], engine_path=r"C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AniScale_30000_new.engine").fmtc.bitdepth(bits=16)

sigmoidized = haf.SigmoidInverse(ai_text, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1920, 1080) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5)
yuv_text = ToYUV(de_sigmoidized, matrix=1, css="420", depth=16)


# Маски
def apply_mask(clip_raw, clip_processed, mask_path, frame_range):
    mask_img = core.imwri.Read(mask_path, alpha=False)
    mask_yuv = ToYUV(mask_img, matrix=1, css="420", depth=16)
    mask_clip = core.std.MaskedMerge(clip_raw, clip_processed, mask_yuv)
    return fvf.rfs(clip_raw, mask_clip, frame_range)
    
mask_01 = apply_mask(mg, yuv_text, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\PV 01-01.png", "[111 163]")
mask_02 = apply_mask(mask_01, yuv_text, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\PV 01-02.png", "[246 281]")
mask_03 = apply_mask(mask_02, yuv_text, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\PV 01-03.png", "[331 373]")
mask_04 = apply_mask(mask_03, yuv_text, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\PV 01-04.png", "[454 498]")
mask_05 = apply_mask(mask_04, yuv_text, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\PV 01-05.png", "[989 1155]").std.Trim(24, 1155)


# Чёрный
black = core.std.BlankClip(
    color=[0, 0, 0],
    width=1920,
    height=1080,
    length=24,
    fpsnum=24000,
    fpsden=1001
)
yuv_black = ToYUV(black, matrix=1, css="420", depth=16)


# Вывод
mg = yuv_black+mask_05+yuv_black
mg.fmtc.bitdepth(bits=10).set_output()
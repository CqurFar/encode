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


# Анискейл на все титры + вставка между парт а и парб б 
# депир между парт а и парб б 
# блэк бокс

#Сорц
episode = core.lsmas.LWLibavSource(source=r"E:\Работа\Yoru no Kurage wa Oyogenai\EP 03.mkv")
episode_16 = episode.fmtc.bitdepth(bits=16)


#Дегрэин
def de_gnb(clip, thsad=100, thsadc=100, dpir_strength=1, mask_blur=1, mask_limit=True):

    # DFTTest и CoolDegrain
    pf = core.dfttest.DFTTest(clip, sigma=1, tbsize=1, opt=3)
    den = cooldegrain.CoolDegrain(clip, tr=3, thsad=thsad, thsadc=thsadc, bits=16, blksize=8, overlap=4, pf=pf)
    
    # Векторка
    osup = den.mv.Super(pel=4, sharp=2, rfilter=2)
    bv1 = osup.mv.Analyse(isb=True, delta=1, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
    bv2 = osup.mv.Analyse(isb=True, delta=2, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
    bv3 = osup.mv.Analyse(isb=True, delta=3, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
    fv1 = osup.mv.Analyse(isb=False, delta=1, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
    fv2 = osup.mv.Analyse(isb=False, delta=2, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
    fv3 = osup.mv.Analyse(isb=False, delta=3, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
    all_degrain  = core.mv.Degrain3(den, super=osup, mvbw=bv1, mvfw=fv1, mvbw2=bv2, mvfw2=fv2, mvbw3=bv3, mvfw3=fv3, thsad=thsad, thsadc=thsadc, plane=4)
    
    # DPIR и дебан
    rgb = ToRGB(all_degrain, matrix=1, depth=32)
    dpir = vsmlrt.DPIR(rgb, model=1, strength=dpir_strength, overlap=0, tilesize=[1920, 1080], backend=vsmlrt.Backend.TRT())
    yuv = ToYUV(dpir, matrix=1, css="420", depth=16)
    db = core.neo_f3kdb.Deband(yuv, y=20, cb=15, cr=15, grainy=0, grainc=0, blur_first=False)
    
    # Маска    
    clip_y = get_y(all_degrain)
    mask_dp = vsmask.edge.Kirsch().edgemask(clip_y, multi=7).std.Minimum()

    if mask_limit:
        mask_dp = mask_dp.std.Limiter()
    mask_dp = mask_dp.std.BoxBlur(hradius=mask_blur, vradius=mask_blur, hpasses=mask_blur, vpasses=mask_blur)
    masked_dp = core.std.MaskedMerge(db, clip, mask_dp)
    
    return masked_dp

def ApplyCredits(credits, nc, fixed_nc):
    credits = core.dfttest.DFTTest(credits, sigma=3, tbsize=3, opt=3)
    credits = ToRGB(credits, matrix=1, depth=8)
    nc = core.dfttest.DFTTest(nc, sigma=3, tbsize=3, opt=3)
    nc = ToRGB(nc, matrix=1, depth=8)
    fixed_nc = ToRGB(fixed_nc, matrix=1, depth=8)
    light = core.std.Expr([credits, nc], ["x y -"]).fmtc.bitdepth(bits=32)
    light = core.trt.Model(light, use_cuda_graph=True, overlap=0, tilesize=[1920, 1080], engine_path=r"C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AniScale_30000_new.engine").fmtc.bitdepth(bits=8)
    light = vskernels.Hamming.scale(light, 1920, 1080) 
    dark = haf.Overlay(nc, credits, mode="divide").fmtc.bitdepth(bits=32)
    dark = core.trt.Model(dark, use_cuda_graph=True, overlap=0, tilesize=[1920, 1080], engine_path=r"C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AniScale_30000_new.engine").fmtc.bitdepth(bits=8)
    dark = vskernels.Hamming.scale(dark, 1920, 1080) 
    dark = haf.Overlay(dark, fixed_nc, mode="multiply")
    all = core.std.Expr([light, dark], ["x y +"])
    return all


def DynamicMask(credits, nc, fixed_nc):
    fixed_nc = ToYUV(fixed_nc, matrix=1, css="420", depth=16)
    avr = haf.Overlay(credits, nc, mode="phoenix")
    avr_yuv = ToYUV(avr, matrix=1, css="420", depth=16)
    avr_pf = core.dfttest.DFTTest(avr_yuv, sigma=10, tbsize=3, opt=3)
    mask = atf.retinex_edgemask(avr_pf).std.Maximum().std.Maximum().std.BoxBlur()
    mask = core.std.Binarize(mask,9000,0).std.Maximum().std.BoxBlur()
    rgb_ai = ToRGB(credits, matrix=1, depth=32)
    ai = core.trt.Model(rgb_ai, use_cuda_graph=True, overlap=0, tilesize=[1920, 1080], engine_path=r"C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AniScale_30000_new.engine")
    desc = core.resize.Lanczos(ai, 1920, 1080) 
    yuv_ai = ToYUV(desc, matrix=1, css="420", depth=16)
    masked = core.std.MaskedMerge(fixed_nc, yuv_ai, mask)
    return masked


def DynamicMask_v2(credits, nc, fixed_nc):
    credits = credits.fmtc.bitdepth(bits=32)
    nc = nc.fmtc.bitdepth(bits=32)
    fixed_nc = fixed_nc.fmtc.bitdepth(bits=32)
    averaged = core.std.Expr([credits, nc, fixed_nc], ["x y -"])
    averaged = core.dfttest.DFTTest(averaged, sigma=100, tbsize=1, opt=3)
    averaged = core.std.ShufflePlanes(averaged, 0, GRAY)
    averaged = averaged.std.Binarize(threshold=2/255).std.Maximum().std.Inflate().std.Maximum().std.Inflate().std.Maximum().std.Inflate().std.Maximum().std.Inflate()
    averaged = core.std.Expr([averaged], ["x 0.5 > 1 x ?"]).std.BoxBlur(1, 1, 1)
    rgb_ai = ToRGB(credits, matrix=1, depth=32)
    ai = core.trt.Model(rgb_ai, use_cuda_graph=True, overlap=0, tilesize=[1920, 1080], engine_path=r"C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AniScale_30000_new.engine")
    desc = core.resize.Lanczos(ai, 1920, 1080) 
    yuv_ai = ToYUV(desc, matrix=1, css="420", depth=32)
    masked = core.std.MaskedMerge(fixed_nc, yuv_ai, averaged).fmtc.bitdepth(bits=16)
    return masked



de_gnb = de_gnb(episode_16, thsad=100, thsadc=100, dpir_strength=1, mask_blur=1, mask_limit=True)
de_gnb.fmtc.bitdepth(bits=10).set_output()
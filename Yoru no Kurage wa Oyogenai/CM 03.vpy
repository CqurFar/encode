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
episode = core.lsmas.LWLibavSource(source=r"E:\Работа\Yoru no Kurage wa Oyogenai\CM 03.mkv")
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
dpir = vsmlrt.DPIR(rgb_dp, model=1, strength=2, overlap=0, tilesize=[1920, 1080], backend=vsmlrt.Backend.TRT())
yuv_dp = ToYUV(dpir, matrix=1, css="420", depth=16)
db = core.neo_f3kdb.Deband(yuv_dp, y=20, cb=15, cr=15, grainy=0, grainc=0, blur_first=False)

clip_y = get_y(all)
mask_dp = vsmask.edge.Kirsch().edgemask(clip_y, multi=7).std.Minimum().std.Limiter().std.BoxBlur(1, 1, 1)
masked_dp = core.std.MaskedMerge(db, episode_16, mask_dp)


#Реверс аа
clip = masked_dp
clip_y = get_y(clip)

line_mask = vsmask.edge.Tritical().edgemask(clip_y,multi=7).std.Maximum().std.Limiter()
descaled = vskernels.Lanczos.descale(clip_y, width=get_w(945), height=945)
deh = vsdehalo.fine_dehalo(descaled, rx=2.4, ry=2.4, brightstr=0.7, darkstr=0, thmi=30, thma=100, ss=1, edgeproc=0.5)
depthed = core.std.MergeDiff(deh, core.std.MakeDiff(deh.warp.AWarpSharp2(128, 3, 1, 2, 1), deh.warp.AWarpSharp2(128, 2, 1, 4, 1)))

def eedi3_sr(clip: vs.VideoNode) -> vs.VideoNode:
    eedi3mode = core.eedi3m.EEDI3CL(clip, 1, False, sclip=clip, alpha=0.125, beta=0.25, vthresh0=12, vthresh1=24) 
    return eedi3mode

aiclip = core.nnedi3cl.NNEDI3CL(depthed, field=1, dh=True, dw=True, nsize=0, nns=4, qual=2, pscrn=1).resize.Lanczos(src_top=-0.5,src_left=-0.5) 
t1 = core.std.Transpose(aiclip)
t1 = eedi3_sr(t1)
t2 = core.std.Transpose(t1)
t2 = eedi3_sr(t2)
t2 = vskernels.Spline64().scale(t2,clip.width,clip.height)
masked = core.std.MaskedMerge(clip_y, t2, line_mask)
t2 = core.std.ShufflePlanes([masked, clip], planes=[0, 1, 2], colorfamily=vs.YUV)


# Нейронка
rgb_ai = ToRGB(t2, matrix=1, depth=16)
sigmoidized = haf.SigmoidInverse(rgb_ai, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1680, 945)
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5).fmtc.bitdepth(bits=32)

ai = core.trt.Model(de_sigmoidized, use_cuda_graph=True, overlap=0, tilesize=[1680, 945], engine_path=r"C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AniSD_DC_RealPLKSR_115K_new.engine").fmtc.bitdepth(bits=16)

sigmoidized = haf.SigmoidInverse(ai, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1920, 1080) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5)
yuv_ai = ToYUV(de_sigmoidized, matrix=1, css="420", depth=16)

line_mask = vsmask.edge.Tritical().edgemask(clip_y, multi=3).std.Maximum().std.Limiter()
mask_ai = core.std.MaskedMerge(t2, yuv_ai, line_mask)
colorfix = atf.CopyColors(mask_ai, db)


# Аберрация
rgb_in = ToRGB(colorfix, matrix=1, depth=32)
props = core.std.RemoveFrameProps(rgb_in)

r = props.std.ShufflePlanes(0, vs.GRAY).std.Crop(left=2)
g = props.std.ShufflePlanes(1, vs.GRAY).std.Crop(left=2)
b = props.std.ShufflePlanes(2, vs.GRAY).std.Crop(right=2)

abberation = core.std.ShufflePlanes([r, g, b], [0, 0, 0], vs.RGB)
yuv_out = ToYUV(abberation, matrix=1, css="420", depth=16).resize.Bilinear(1920, 1080)

clip = colorfix
clip_y = get_y(clip)
mask_ab = vsmask.edge.Tritical().edgemask(clip_y, multi=0.75).std.Maximum().std.Limiter() # или Kirsch 0,4 но сильнее
masked_ab = core.std.MaskedMerge(colorfix, yuv_out, mask_ab)
rgb_ab = ToRGB(masked_ab, matrix=1, depth=8)




# Лого 
item = core.imwri.Read(r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\CM Logo.png", alpha=True)

def apply_logo(n, *args):
    if 24 <= n <= 71:
        return haf.Overlay(rgb_ab, item[0], mask=item.std.PropToClip("_Alpha"), mode="normal")
    else:
        return rgb_ab

overlay = core.std.FrameEval(rgb_ab, eval=apply_logo)
overlay = ToYUV(overlay, matrix=1, css="420", depth=16)


# Текст
text = episode
text_16 = episode.fmtc.bitdepth(bits=16)


# Нейронка
rgb_text = ToRGB(text_16, matrix=1, depth=32)
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
    
mask_01 = apply_mask(overlay, yuv_text, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\CM 03-01.png", "[24 109]")
mask_02 = apply_mask(mask_01, yuv_text, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\CM 03-02.png", "[110 193]")
mask_03 = apply_mask(mask_02, yuv_text, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\CM 03-03.png", "[277 347]")
mask_04 = apply_mask(mask_03, yuv_text, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\All.png", "[348 383]")
rgb_mask = ToRGB(mask_04,  matrix=1, depth=32)




# Зерно
gr = core.std.BlankClip(mask_04, width=1280, height=720, format=vs.GRAYS, length=mask_04.num_frames, color=[0])
gr = core.grain.Add(gr, var=0.5, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0).resize.Bilinear(1920, 1080)

rgb_gr = ToRGB(gr, matrix=1, depth=32)
merged_gr = haf.Overlay(rgb_mask, rgb_gr, mode="screen")
yuv_gr = ToYUV(merged_gr, matrix=1, css="420", depth=16).std.Trim(24, 383)


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
mg = yuv_black+yuv_gr+yuv_black
mg.fmtc.bitdepth(bits=10).set_output()
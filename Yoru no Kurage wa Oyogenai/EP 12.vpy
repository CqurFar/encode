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
episode = core.lsmas.LWLibavSource(source=r"E:\Работа\Yoru no Kurage wa Oyogenai\EP 12.mkv")
episode_16 = episode.fmtc.bitdepth(bits=16)


#Дегрэин
pf = core.dfttest.DFTTest(episode_16, sigma=0.5, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=3, thsad=50, thsadc=100, bits=16, blksize=8, overlap=4, pf=pf)

rgb_dp = ToRGB(den, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_dp, model=1, strength=1, overlap=0, tilesize=[1920, 1080], backend=vsmlrt.Backend.TRT())
yuv_dp = ToYUV(dpir, matrix=1, css="420", depth=16)
db = core.neo_f3kdb.Deband(yuv_dp, y=15, cb=10, cr=10, grainy=0, grainc=0, blur_first=False)

clip_y = get_y(den)
mask_dp = vsmask.edge.DoG().edgemask(clip_y, multi=8).std.Maximum().std.Limiter()
masked_dp = core.std.MaskedMerge(db, episode_16, mask_dp)


#Реверс аа
clip = masked_dp
clip_y = get_y(clip)

line_mask = vsmask.edge.Tritical().edgemask(clip_y,multi=8).std.Maximum().std.Limiter()
descaled = vskernels.Hamming.scale(clip_y, width=get_w(945), height=945)
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
t2 = vskernels.Hamming.scale(t2,clip.width,clip.height)
masked = core.std.MaskedMerge(clip_y, t2, line_mask)
t2 = core.std.ShufflePlanes([masked, clip], planes=[0, 1, 2], colorfamily=vs.YUV)


# Нейронка
rgb_ai = ToRGB(t2, matrix=1, depth=16)
sigmoidized = haf.SigmoidInverse(rgb_ai, thr=0.5, cont=6.5) 
scaled_sigmoid = vskernels.Hamming.scale(sigmoidized, 1680, 945)
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5).fmtc.bitdepth(bits=32)

ai_01 = core.trt.Model(de_sigmoidized, use_cuda_graph=True, overlap=0, tilesize=[1680, 945], engine_path=r"C:\Users\Art\AppData\Roaming\.enhancr\models\engine\1x_Loyaldk-SharpKeroro_120000_V1.0_new.engine")
ai_02 = core.trt.Model(de_sigmoidized, use_cuda_graph=True, overlap=0, tilesize=[1680, 945], engine_path=r"C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AniSD_G6i1_SPAN_215K_new.engine").fmtc.bitdepth(bits=16)

descale_01 = haf.SigmoidInverse(ai_02, thr=0.5, cont=6.5) 
descale_01 = vskernels.Hamming.scale(descale_01, 1920, 1080) 
descale_01 = haf.SigmoidDirect(descale_01, thr=0.5, cont=6.5)
yuv_ai = ToYUV(descale_01, matrix=1, css="420", depth=16)

mask_ai = vsmask.edge.Kirsch().edgemask(clip_y, multi=3).std.Maximum().std.Limiter()
masked_ai = core.std.MaskedMerge(t2, yuv_ai, mask_ai)
colorfix = atf.CopyColors(masked_ai, t2)


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
mask_ab = vsmask.edge.Kirsch().edgemask(clip_y, multi=0.3).std.Maximum().std.Limiter()
masked_ab = core.std.MaskedMerge(colorfix, yuv_out, mask_ab)


# Eye Catch and End Card
ecec = episode


# Нейронка
rgb_ecec = ToRGB(ecec, matrix=1, depth=32)
ai_ecec = core.trt.Model(rgb_ecec, use_cuda_graph=True, overlap=0, tilesize=[1920, 1080], engine_path=r"C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AniScale_30000_new.engine").fmtc.bitdepth(bits=16)

descale_02 = haf.SigmoidInverse(ai_ecec, thr=0.5, cont=6.5) 
descale_02 = vskernels.Hamming.scale(descale_02, 1920, 1080) 
descale_02 = haf.SigmoidDirect(descale_02, thr=0.5, cont=6.5)
yuv_ecec = ToYUV(descale_02, matrix=1, css="420", depth=16)


# Маски
def apply_mask(clip_raw, clip_processed, mask_path, frame_range):
    mask_img = core.imwri.Read(mask_path, alpha=False)
    mask_yuv = ToYUV(mask_img, matrix=1, css="420", depth=16)
    mask_clip = core.std.MaskedMerge(clip_raw, clip_processed, mask_yuv)
    return fvf.rfs(clip_raw, mask_clip, frame_range)
    
eye_catch = apply_mask(masked_ab, yuv_ecec, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\Eye Catch.png", "[23088, 23159]")
end_card = apply_mask(eye_catch, yuv_ecec, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\End Card 12.png", "[34046, 34165]")




# Маски OP
mask_op = fvf.rfs(end_card, atf.ApplyImageMask(end_card, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-01.png"), "[202 345]")
mask_op = fvf.rfs(mask_op, atf.ApplyImageMask(mask_op, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-02.png"), "[441 596]")
mask_op = fvf.rfs(mask_op, atf.ApplyImageMask(mask_op, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-03.png"), "[637 774]")
mask_op = fvf.rfs(mask_op, atf.ApplyImageMask(mask_op, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-04.png"), "[789 925]")
mask_op = fvf.rfs(mask_op, atf.ApplyImageMask(mask_op, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-05.png"), "[1133 1263]")
mask_op = fvf.rfs(mask_op, atf.ApplyImageMask(mask_op, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-06.png"), "[1362 1517]")
mask_op = fvf.rfs(mask_op, atf.ApplyImageMask(mask_op, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-07.png"), "[1586 1747]")
mask_op = fvf.rfs(mask_op, atf.ApplyImageMask(mask_op, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-08.png"), "[1821 1939]")
mask_op = fvf.rfs(mask_op, atf.ApplyImageMask(mask_op, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-09.png"), "[2078 2222]")
mask_op = fvf.rfs(mask_op, atf.ApplyImageMask(mask_op, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-10.png"), "[2388 2543]")
mask_op = fvf.rfs(mask_op, atf.ApplyImageMask(mask_op, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-11.png"), "[2608 2711]")
mask_op = fvf.rfs(mask_op, atf.ApplyImageMask(mask_op, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-11.png"), "[2804 2881]")


# Маски ED
mask_ed = fvf.rfs(mask_op, atf.ApplyImageMask(mask_op, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-12.png"), "[32086 32185]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-13.png"), "[32201 32299]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-14.png"), "[32309 32413]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-15.png"), "[32422 32536]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-16.png"), "[32631 32758]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-17.png"), "[32823 32897]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-18.png"), "[32910 33015]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-19.png"), "[33034 33120]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-20.png"), "[33141 33229]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-21.png"), "[33291 33379]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-22.png"), "[33429 33513]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-23.png"), "[33525 33608]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-24.png"), "[33621 33708]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-25.png"), "[33717 33797]")
mask_ed = fvf.rfs(mask_ed, atf.ApplyImageMask(mask_ed, episode_16, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\EP12-26.png"), "[33831 33921]")

rgb_cont = ToRGB(mask_ed, matrix=1, depth=32)


# Зерно
gr = core.std.BlankClip(rgb_cont, width=1280, height=720, format=vs.GRAYS, length=masked_ab.num_frames, color=[0])
gr = core.grain.Add(gr, var=0.5, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0).resize.Bilinear(1920, 1080)
rgb_gr = ToRGB(gr, matrix=1, depth=32)

merged = haf.Overlay(rgb_cont, rgb_gr, mode="screen")
yuv_gr = ToYUV(merged, matrix=1, css="420", depth=16)


# Вывод
yuv_gr.fmtc.bitdepth(bits=10).set_output()
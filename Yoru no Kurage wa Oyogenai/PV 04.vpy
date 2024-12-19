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
episode = core.lsmas.LWLibavSource(source=r"E:\Работа\Yoru no Kurage wa Oyogenai\PV 04.mkv")
episode_16 = episode.fmtc.bitdepth(bits=16)


# Нейронка
rgb_text = ToRGB(episode_16, matrix=1, depth=32)
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
    
mask_01 = apply_mask(episode_16, yuv_text, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\PV 04-01.png", "[59 145]")
mask_02 = apply_mask(mask_01, yuv_text, r"E:\Работа\Yoru no Kurage wa Oyogenai\Скрипты\Маски\PV 04-02.png", "[1446 1535]").std.Trim(24, 1535)


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
mg = yuv_black+mask_02+yuv_black
mg.fmtc.bitdepth(bits=10).set_output()
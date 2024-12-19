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
episode = core.lsmas.LWLibavSource(source=r"E:\Работа\Yoru no Kurage wa Oyogenai\AD 12.mkv").fmtc.bitdepth(bits=16)
deh = vsdehalo.fine_dehalo(episode, rx=2.4, ry=2.4, brightstr=0.7, darkstr=0, thmi=30, thma=100, ss=1, edgeproc=0.5)
clip_y = get_y(deh) 


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


# Нейронка
rgb_ai = ToRGB(deh, matrix=1, depth=32)
ai = core.trt.Model(rgb_ai, use_cuda_graph=True, overlap=0, tilesize=[1920, 1080], engine_path=r"C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AniScale_30000_new.engine").fmtc.bitdepth(bits=16)

sigmoidized = haf.SigmoidInverse(ai, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1920, 1080) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5)
yuv_ai = ToYUV(de_sigmoidized, matrix=1, css="420", depth=16)

line_mask = vsmask.edge.Tritical().edgemask(clip_y, multi=3).std.Maximum().std.Limiter()
mask_ai = core.std.MaskedMerge(deh, yuv_ai, line_mask)


#Депир
rgb_dp = ToRGB(mask_ai, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_dp, model=1, strength=2, overlap=0, tilesize=[1920, 1080], backend=vsmlrt.Backend.TRT())
yuv_dp = ToYUV(dpir, matrix=1, css="420", depth=16)
db = core.neo_f3kdb.Deband(yuv_dp, y=20, cb=15, cr=15, grainy=0, grainc=0, blur_first=False)


# Вывод
gr = core.grain.Add(db, var=2, uvar=0.0, hcorr=0.2, vcorr=0.2, seed=123456789, constant=True, opt=0)
mg = yuv_black+gr.std.Trim(24, 5730)+yuv_black
mg.fmtc.bitdepth(bits=10).set_output()
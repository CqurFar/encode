from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsgan import ESRGAN
import vapoursynth as vs
import atomchtools
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


core.num_threads = 24
core.max_cache_size = 30000

import os
os.environ['CUDA_MODULE_LOADING'] = 'LAZY'
os.environ['CUDA_FORCE_PRELOAD_LIBRARIES'] = '1'
os.environ['CUDA_AUTO_BOOST'] = '1'
os.environ['CUDA_DEVICE_MAX_CONNECTIONS'] = '32'
os.environ['CUDA_CACHE_MAXSIZE'] = '12884901888'


episode = core.lsmas.LWLibavSource(source=r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\luts\200.png').fmtc.bitdepth(bits=32)


esrgan = ESRGAN(episode, device="cuda")
vsgan.networks.esrgan.ESRGAN
esrgan.load(r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\2x_QDCU.PTH')
vsgan.networks.esrgan.ESRGAN
esrgan.apply()
vsgan.networks.esrgan.ESRGAN
ai_01 = esrgan.clip.resize.Bilinear(width=1920, height=1080)

ai_01.set_output()
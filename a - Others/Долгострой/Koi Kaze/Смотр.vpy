from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsutil import get_w
from vsgan import ESRGAN
from mvsfunc import ToYUV
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


#Сорц
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Koi Kaze\EP 01.mkv')


#Деинт
deint_01 = core.vivtc.VFM(episode, order=1, field=2, mode=1, cthresh=8, mi=80, blockx=16, blocky=16, scthresh=8)
deint_01 = core.vivtc.VDecimate(deint_01, cycle=5, dupthresh=1.1, scthresh=10, blockx=4, blocky=4, dryrun=0).fmtc.bitdepth(bits=32)


#Рескеил width=846, height=476
cr = core.std.Crop(deint_01, left=4, right=4, top=2)
linear = core.resize.Bicubic(cr, format=vs.RGBS, transfer_in_s="709", transfer_s="linear", matrix_in_s="709").fmtc.bitdepth(bits=16)
sigmoidized = haf.SigmoidInverse(linear, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Bicubic(sigmoidized, 960, 540) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
scaled_gamma = core.resize.Bicubic(de_sigmoidized, format=cr.format, transfer_s="709", transfer_in_s="linear", matrix_s="709")

scaled_gamma.fmtc.bitdepth(bits=10).set_output()
from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsutil import get_w
from vsgan import ESRGAN
from mvsfunc import ToYUV, ToRGB
from havsfunc import FastLineDarkenMOD
from vsrgtools import rgtools
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
import vsmlrt
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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Golgo 13 The Professional\IV 01.m2ts')


#Деинт
deint_01 = core.vivtc.VFM(episode, order=1, field=2, mode=5, cthresh=-1, mi=0, blockx=4, blocky=4, scthresh=8, micout=True, micmatch=2)
deint_01 = core.vivtc.VFM(deint_01, order=0, field=2, mode=5, cthresh=-1, mi=0, blockx=4, blocky=4, scthresh=8, micout=True, micmatch=2)
deint_01 = haf.Vinverse2(deint_01, sstr=0, amnt=255, chroma=True).fmtc.bitdepth(bits=32)
deint_01 = core.ftf.FixFades(deint_01, mode=0, threshold=0.002, color=[0.0, 0.0, 0.0])
deint_01 = haf.srestore(deint_01, frate=24/1.001, speed=-1, thresh=8).fmtc.bitdepth(bits=16)


#Фильтрация
pf = core.dfttest.DFTTest(deint_01, sigma=3, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=2, thsad=50, thsadc=70, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=30, cb=20, cr=20, grainy=0, grainc=0, blur_first=True)

rgb_in = ToRGB(db, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_in, model=1, strength=5, overlap=0, tilesize=[720, 480], backend=vsmlrt.Backend.TRT())
fil = ToYUV(dpir, matrix=1, css='420', depth=16)

mg = fil.std.Trim(0, 355)+deint_01.std.Trim(356, 2516)+fil.std.Trim(2517, 2772)+deint_01.std.Trim(2773, 3005)+fil.std.Trim(3006, 3263)+deint_01.std.Trim(3264, 3569)+fil.std.Trim(3570, 3874)+deint_01.std.Trim(3875, 4155)+fil.std.Trim(4156, 4452)+deint_01.std.Trim(4453, 5079)+fil.std.Trim(5080, 5374)

sigmoidized = haf.SigmoidInverse(mg, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 640, 480) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
yuv_out = ToYUV(de_sigmoidized, matrix=1, css='420', depth=16)

yuv_out.fmtc.bitdepth(bits=10).set_output()
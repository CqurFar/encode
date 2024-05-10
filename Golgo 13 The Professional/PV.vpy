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


#Сорц
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Golgo 13 The Professional\Trailer.m2ts')


#Деинт
deint_01 = core.vivtc.VFM(episode, order=1, field=2, mode=5, cthresh=-1, mi=0, blockx=4, blocky=4, scthresh=8, micout=True, micmatch=2)
deint_01 = core.vivtc.VFM(deint_01, order=0, field=2, mode=5, cthresh=-1, mi=0, blockx=4, blocky=4, scthresh=8, micout=True, micmatch=2)
deint_01 = haf.Vinverse2(deint_01, sstr=0, amnt=255, chroma=True).fmtc.bitdepth(bits=32)
deint_01 = core.ftf.FixFades(deint_01, mode=0, threshold=0.002, color=[0.0, 0.0, 0.0])
deint_01 = haf.srestore(deint_01, frate=24/1.001, speed=-1, thresh=8).fmtc.bitdepth(bits=16)


#Фильтрация
pf = core.dfttest.DFTTest(deint_01, sigma=1, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=2, thsad=10, thsadc=30, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=25, cb=15, cr=15, grainy=0, grainc=0, blur_first=True)


#Депир
rgb_in = ToRGB(db, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_in, model=1, strength=1, overlap=0, tilesize=[720, 480], backend=vsmlrt.Backend.TRT())
yuv_out = ToYUV(dpir, matrix=1, css='420', depth=16)


#Рескеил
sigmoidized = haf.SigmoidInverse(yuv_out, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, get_w(480), 480) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 


#Зерно и выфвод
deh = vsdehalo.fine_dehalo(de_sigmoidized, rx=2.2, ry=2.2, darkstr=0, brightstr=0.5, thmi=30, thma=100, ss=1, edgeproc=0.5)
gr = core.grain.Add(deh, var=1.2, uvar=0.0, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)
gr.fmtc.bitdepth(bits=10).set_output()
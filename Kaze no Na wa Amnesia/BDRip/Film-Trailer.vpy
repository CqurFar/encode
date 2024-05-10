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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Kaze no Na wa Amnesia\Trailer.m2ts')
episode_16 = core.lsmas.LWLibavSource(source=r'E:\Работа\Kaze no Na wa Amnesia\Trailer.m2ts').fmtc.bitdepth(bits=16)

def KillerSpots(clip: vs.VideoNode, limit: int =10, advanced: bool =True):
  osup = core.mv.Super(clip=clip, pel=4, sharp=2)
  bv1  = core.mv.Analyse(super=osup, isb=True, delta=1, overlap=2, blksize=4, search=3, truemotion=False)
  fv1  = core.mv.Analyse(super=osup, isb=False, delta=1, overlap=2, blksize=4, search=3, truemotion=False)
  bc1  = core.mv.Compensate(clip, osup, bv1)
  fc1  = core.mv.Compensate(clip, osup, fv1)
  clip = core.std.Interleave([fc1, clip, bc1])
  if advanced:
    clip = RemoveDirtMod(clip, limit)
  else:
    clip = core.rgvs.Clense(clip)
  clip = core.std.SelectEvery(clip=clip, cycle=3, offsets=1)
  return clip;
  

kls = KillerSpots(episode, limit=0, advanced=False)
lim = limit.limit_filter(episode, kls, thr=0.5, elast=1, bright_thr=0.5)


#Нейронка
rgbs_in = core.resize.Lanczos(lim, format=vs.RGBS, matrix_in='1')
yuv_episode = ToYUV(rgbs_in)
clip_y = get_y(yuv_episode)
ai = core.trt.Model(rgbs_in , engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_AniScale_30000.engine')
linear = core.resize.Lanczos(ai, format=vs.RGBS).fmtc.bitdepth(bits=16)
sigmoidized = haf.SigmoidInverse(linear, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1920, 1080) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
rgbs_out = core.resize.Lanczos(de_sigmoidized, format=vs.RGBS)
yuv_ai = ToYUV(rgbs_out)
line_mask = vsmask.edge.Prewitt().edgemask(clip_y, multi=1).std.Maximum().std.Limiter()
mask_ai = core.std.MaskedMerge(yuv_episode, yuv_ai, line_mask)


#Фильтрация
clip16 = core.resize.Lanczos(mask_ai, format=vs.YUV420P16, matrix_s='709')
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=2, thsad=40, thsadc=20, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=30, cb=15, cr=15, grainy=0, grainc=0, blur_first=False)


#Зерно и вывод
clip16 = core.resize.Lanczos(db, format=vs.YUV420P16, matrix_s='709')
sh = core.cas.CAS(clip16, sharpness=0.3, opt=0)
deh = vsdehalo.fine_dehalo(sh, ref=None, rx=2.4, ry=2.4, darkstr=0, brightstr=0.7, thmi=30, thma=100, excl=True, ss=1, edgeproc=0.5)
gr = core.grain.Add(deh, var=0.5, uvar=0.2, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)

mg = episode_16.std.Trim(0, 541)+gr.std.Trim(542, 6184)+episode_16.std.Trim(6185, 6210)

cr = core.std.Crop(mg, left=240, right=240)
cr.fmtc.bitdepth(bits=10).set_output()
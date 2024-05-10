from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsutil import get_w
from vsgan import ESRGAN
from mvsfunc import ToYUV, ToRGB
from havsfunc import FastLineDarkenMOD
from vsaa import based_aa, upscaled_sraa, Nnedi3, Eedi3, SangNom
from vsrgtools import rgtools
from vstools import join, depth
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
import limit_v2
import vsdehalo
import vsmlrt
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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Golgo 13 The Professional\Disk Menu.m2ts').fmtc.bitdepth(bits=16)
episode = episode.std.Trim(0, 2800)


#SpotLess moded kls
def SpotLess(clip, chroma=True, rec=False, analyse_args=None, recalculate_args=None):

  isFLOAT = clip.format.sample_type == vs.FLOAT
  isGRAY = clip.format.color_family == vs.GRAY
  chroma = False if isGRAY else chroma
  planes = [0, 1, 2] if chroma else [0]
  A = core.mvsf.Analyse if isFLOAT else core.mv.Analyse
  C = core.mvsf.Compensate if isFLOAT else core.mv.Compensate
  S = core.mvsf.Super if isFLOAT else core.mv.Super
  R = core.mvsf.Recalculate if isFLOAT else core.mv.Recalculate

  sup = S(clip, pel=4, sharp=2, rfilter=2)

  if analyse_args is None:
      analyse_args = dict(blksize=4, overlap=2, search=5)

  if recalculate_args is None:
      recalculate_args = dict(blksize=4, overlap=2, search=5)

  bv1 = A(sup, isb=True,  delta=1, **analyse_args)
  fv1 = A(sup, isb=False, delta=1, **analyse_args)

  if rec:
      bv1 = R(sup, bv1, **recalculate_args)
      fv1 = R(sup, fv1, **recalculate_args)

  bc1 = C(clip, sup, bv1)
  fc1 = C(clip, sup, fv1)
  clip = core.std.Interleave([fc1, clip, bc1])

  clip = rgtools.removegrain(clip, mode=5)
  clip = rgtools.clense(clip)
  clip = core.std.SelectEvery(clip=clip, cycle=3, offsets=1)
  return clip;


sls = SpotLess(episode, chroma=True, rec=True)


#Фильтрация
pf = core.dfttest.DFTTest(sls, sigma=1, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=2, thsad=20, thsadc=50, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=20, cb=15, cr=15, grainy=0, grainc=0, blur_first=True)
fix_edge = core.edgefixer.Continuity(db, left=0, right=0, bottom=3)


#Зерно и вывод
deh = vsdehalo.fine_dehalo(fix_edge, rx=2.2, ry=2.2, darkstr=0, brightstr=0.5, thmi=30, thma=100, ss=1, edgeproc=0.5)
gr = core.grain.Add(deh, var=1.5, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=123456789, constant=False, opt=0)
gr.fmtc.bitdepth(bits=10).set_output()
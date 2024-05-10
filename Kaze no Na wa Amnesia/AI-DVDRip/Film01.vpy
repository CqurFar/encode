from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsdpir import DPIR
import vapoursynth as vs
import atomchtools
import beatricetools
import havsfunc as haf
import fvsfunc
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


core.num_threads = 24
core.max_cache_size = 30000


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Kaze no Na wa Amnesia\Kaze no Na wa Amnesia.mkv').fmtc.bitdepth(bits=8)

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
lim = limit.limit_filter(episode, kls, thr=60, elast=1, bright_thr=1).fmtc.bitdepth(bits=32)
dpir  = lvsfunc.dpir(lim, strength=3, mode='denoise', cuda=True)


mg = dpir


clip16=core.fmtc.bitdepth(mg, bits=16)
dehalo_alph1 = vsdehalo.fine_dehalo(clip16,None,2.3,2.3,0,0.4,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph1,None,2.3,2.3,0,0.4,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph2,None,2.3,2.3,0,0.3,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph2,None,2.3,2.3,0,0.2,thmi=30,thma=100)
deh = G41Fun.MaskedDHA(dehalo_alph2, rx=2.3, ry=2.3, darkstr=0, brightstr=0.5)
deh = G41Fun.MaskedDHA(deh, rx=2.3, ry=2.3, darkstr=0, brightstr=0.4)

deh.fmtc.bitdepth(bits=10).set_output()
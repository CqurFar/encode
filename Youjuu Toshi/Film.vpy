from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import atomchtools as atf
import beatricetools as bea
import havsfunc as haf
import fvsfunc as fvf
import kagefunc as kgf
import mvsfunc as mvf
import muvsfunc as muf
import descale as dsc
import finesharp
import ccd
import MCDenoise 
import cooldegrain
import finedehalo as fd
import insaneAA
import xaa
import vsTAAmbk as taa
import HardAA
import lostfunc as lfc
import G41Fun
import rgvs
import xvs


core.num_threads = 24
core.max_cache_size = 30000


all = core.lsmas.LWLibavSource(source=r'E:\Работа\Youjuu Toshi\Film.m2ts')


def RemoveDirtMod(all, limit=10):
  clensed = core.rgvs.Clense(all)
  alt = core.rgvs.RemoveGrain(all, mode=1)
  clip = core.rdvs.RestoreMotionBlocks(clensed, all, alternative=alt, pthreshold=4, cthreshold=6, gmthreshold=10, dist=3, dmode=2, noise=limit, noisy=12)
  return clip
  
rdm = RemoveDirtMod(all)


def KillerSpots(all, limit=10, advanced=True):
  osup = core.mv.Super(clip=all, pel=2, sharp=2)
  bv1  = core.mv.Analyse(super=osup, isb=True, delta=1, overlap=4)
  fv1  = core.mv.Analyse(super=osup, isb=False, delta=1, overlap=4)
  bc1  = core.mv.Compensate(all, osup, bv1)
  fc1  = core.mv.Compensate(all, osup, fv1)
  clip = core.std.Interleave([fc1, all, bc1])
  if advanced:
    clip = RemoveDirtMod(clip, limit)
  else:
    clip = core.rgvs.Clense(clip)
  clip = core.std.SelectEvery(clip=clip, cycle=3, offsets=1)
  return clip;
  
kls = KillerSpots(all)


mg = kls


clip16 = core.fmtc.bitdepth(mg, bits=16)
den = cooldegrain.CoolDegrain(clip16, tr=3, thsad=40, thsadc=38, bits=16, blksize=8, overlap=4, pf=clip16)
db = core.placebo.Deband(den, threshold=2.5, radius=10, grain=0)

Mask = atf.Tp7DebandMask(db, thr = 1.5, scale = 1, rg = True)
Invert = core.std.Invert(Mask, planes=[0])
Filtered = core.std.MaskedMerge(den, db, Invert, planes=[0], first_plane=True)

sh = core.cas.CAS(Filtered, sharpness=0.7, opt=0)

fd1 = fd.fine_dehalo(sh, None, 2.2, 2.2, 0, 0.5)
fd2 = fd.fine_dehalo(fd1, None, 2.2, 2.2, 0, 0.5)
dha1 = G41Fun.MaskedDHA(fd2, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)
dha2 = G41Fun.MaskedDHA(dha1, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)

gr = core.grain.Add(dha2, var=1.3, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=100, constant=False, opt=0)
cr = core.std.Crop(gr, left=240, right=240)

cr.fmtc.bitdepth(bits=10).set_output()
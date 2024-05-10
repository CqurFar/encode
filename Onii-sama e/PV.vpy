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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Oniisama e\PV 01.m2ts')

osup = episode.mv.Super(pel=2, sharp=2)
bv2 = osup.mv.Analyse(delta=2, overlap=4, isb=True)
bv1 = osup.mv.Analyse(delta=1, overlap=4, isb=True)
fv1 = osup.mv.Analyse(delta=1, overlap=4, isb=False)
fv2 = osup.mv.Analyse(delta=2, overlap=4, isb=False)
all = core.mv.Degrain2(episode, super=osup, mvbw=bv1, mvfw=fv1, mvbw2=bv2, mvfw2=fv2, thsad=200)


def RemoveDirtMod(all, limit=10):
  clensed = core.rgvs.Clense(all)
  alt = core.rgvs.RemoveGrain(all, mode=1)
  clip = core.rdvs.RestoreMotionBlocks(clensed, all, alternative=alt, pthreshold=4, cthreshold=6, gmthreshold=40, dist=3, dmode=2, noise=limit, noisy=12)
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
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3)
fd = fd.fine_dehalo(pf, darkstr=0.1, brightstr=0.8, showmask=0, thmi=50, thma=95, rx=2.5, ry=2.5)
den = cooldegrain.CoolDegrain(fd, tr=3, thsad=60, thsadc=14, bits=16, blksize=8, overlap=4, pf=fd)
db = core.neo_f3kdb.Deband(den, range=20, y=15, cb=10, cr=10, output_depth=16)
sh = core.cas.CAS(db, sharpness=0.5, opt=3)
gr = core.grain.Add(sh, var=1.2, uvar=1.2, seed=20, constant=False, opt=3)

mask = fvf.rfs(gr, atf.ApplyImageMask(gr, clip16, r'E:\Работа\Oniisama e\Скрипты\Маски\PV01-01.png'), "[0 2694]")

mask.fmtc.bitdepth(bits=10).set_output()
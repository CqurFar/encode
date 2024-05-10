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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Oniisama e\EP 01.m2ts')
episode = core.std.Crop(episode, left=236, right=236)


osup = episode.mv.Super(pel=2, sharp=2)
bv2 = osup.mv.Analyse(delta=2, overlap=4, isb=True)
bv1 = osup.mv.Analyse(delta=1, overlap=4, isb=True)
fv1 = osup.mv.Analyse(delta=1, overlap=4, isb=False)
fv2 = osup.mv.Analyse(delta=2, overlap=4, isb=False)
all = core.mv.Degrain2(episode, super=osup, mvbw=bv1, mvfw=fv1, mvbw2=bv2, mvfw2=fv2, thsad=400)


mg = all


clip16 = core.fmtc.bitdepth(mg, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3)
fd = fd.fine_dehalo(pf, darkstr=0.1, brightstr=0.8, showmask=0, thmi=50, thma=95, rx=2.5, ry=2.5)
den = cooldegrain.CoolDegrain(fd, tr=3, thsad=20, thsadc=14, bits=16, blksize=8, overlap=4, pf=fd)
db = core.neo_f3kdb.Deband(den, range=20, y=15, cb=10, cr=10, output_depth=16)
sh = core.cas.CAS(db, sharpness=0.5, opt=0)
gr = core.grain.Add(sh, var=1.2, uvar=1.2, seed=20, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
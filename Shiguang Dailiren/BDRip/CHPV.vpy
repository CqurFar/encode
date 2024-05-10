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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Linck Click\PV\CHPV 01.m2ts')


osup = episode.mv.Super(pel=2, sharp=2)
bv2 = osup.mv.Analyse(delta=2, overlap=4, isb=True)
bv1 = osup.mv.Analyse(delta=1, overlap=4, isb=True)
fv1 = osup.mv.Analyse(delta=1, overlap=4, isb=False)
fv2 = osup.mv.Analyse(delta=2, overlap=4, isb=False)
all = core.mv.Degrain2(episode, super=osup, mvbw=bv1, mvfw=fv1, mvbw2=bv2, mvfw2=fv2, thsad=400)


mg = all


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.5, ry=2.5)
pf = core.dfttest.DFTTest(fd, sigma=1, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=3, thsad=20, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.neo_f3kdb.Deband(den, y=50, cb=45, cr=45, blur_first=True, dynamic_grain=False, opt=3)
gr = core.grain.Add(db, var=0.4, uvar=0.4, seed=100, constant=False, opt=3)

gr.fmtc.bitdepth(bits=10).set_output()
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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Linck Click\NC\OP JPN.m2ts')
episode = core.std.Crop(episode, top=140, bottom=140)


osup = episode.mv.Super(pel=2, sharp=2)
bv2 = osup.mv.Analyse(delta=2, overlap=4, isb=True)
bv1 = osup.mv.Analyse(delta=1, overlap=4, isb=True)
fv1 = osup.mv.Analyse(delta=1, overlap=4, isb=False)
fv2 = osup.mv.Analyse(delta=2, overlap=4, isb=False)
all = core.mv.Degrain2(episode, super=osup, mvbw=bv1, mvfw=fv1, mvbw2=bv2, mvfw2=fv2, thsad=200)


mg = all


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.5, ry=2.5)
pf = core.dfttest.DFTTest(fd, sigma=1, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=3, thsad=20, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.neo_f3kdb.Deband(den, y=30, cb=25, cr=25, blur_first=True, dynamic_grain=False, opt=3)
gr = fvf.rfs(db, core.grain.Add(db, var=1.8, uvar=1.5, seed=200, constant=False, opt=3), "[24 1535]")

gr.fmtc.bitdepth(bits=10).set_output()
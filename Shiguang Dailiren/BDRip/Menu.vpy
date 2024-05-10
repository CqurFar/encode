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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Linck Click\BD Menu\Menu 01.m2ts')


mg = episode


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4)
pf = core.dfttest.DFTTest(fd, sigma=1, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=3, thsad=20, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.neo_f3kdb.Deband(den, range=30, y=25, cb=20, cr=20, blur_first=False, dynamic_grain=False, opt=3)

db.fmtc.bitdepth(bits=10).set_output()
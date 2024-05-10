from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import atomchtools as atf
import beatricetools as bea
import havsfunc as haf
import fvsfunc as fvf
import kagefunc as kgf
import mvsfunc as mvsf
import muvsfunc as muvs
import descale as dsc
import finesharp
import ccd
import MCDenoise 
import cooldegrain
import finedehalo as fd
import insaneAA
import xaa
import Vine
import vsTAAmbk as taa
import HardAA
import lostfunc as lfc
import G41Fun
import rgvs
import xvs


core.num_threads = 24
core.max_cache_size = 30000


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Aku no Hana\BD Menu\Menu 01.mkv')


mg = episode


clip16 = core.fmtc.bitdepth(mg, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1.5, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, range=20, y=20, cb=15, cr=15, output_depth=16, blur_first=True)

db.fmtc.bitdepth(bits=10).set_output()
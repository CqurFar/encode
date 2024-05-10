from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import atomchtools as atf
import beatricetools as bea
import havsfunc as haf
import fvsfunc as fvf
import kagefunc as kg
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

core.num_threads = 24
core.max_cache_size = 30000

episode = core.lsmas.LWLibavSource(source=r'E:\Работа\[BDMV][Osananajimi ga Zettai ni Makenai LoveCome][Vol.01-04]\13.m2ts')
 
mg = episode


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0, brightstr=0.4, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2)
db = core.neo_f3kdb.Deband(fd, y=40, cb=40, cr=40, grainy=30, grainc=30, output_depth=16,  dynamic_grain=True, keep_tv_range=True, blur_first=True)


db.fmtc.bitdepth(bits=10).set_output()
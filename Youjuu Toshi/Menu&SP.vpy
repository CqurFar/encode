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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Youjuu Toshi\Menu 01.m2ts')


mg = episode


clip16 = core.fmtc.bitdepth(mg, bits=16)
db = core.neo_f3kdb.Deband(clip16, range=25, y=20, cb=10, cr=10, output_depth=16, blur_first=False)
den = cooldegrain.CoolDegrain(db, tr=1, thsad=16, thsadc=10, bits=16, blksize=8, overlap=4, pf=db)

den.fmtc.bitdepth(bits=10).set_output()
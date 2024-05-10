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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Sonny Boy\Ep 08.m2ts')


mg = episode

mg = fvf.rfs(mg, HardAA.HardAA(episode, mask='simple', mthr=0.1), "[0 33829]")


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0.2, brightstr=0.8, showmask=0, thmi=50, thma=95, rx=2.5, ry=2.5)
db = core.neo_f3kdb.Deband(fd, range=25, y=20, cb=10, cr=10, grainy=20, grainc=20, output_depth=16, dynamic_grain=True, keep_tv_range=True, blur_first=False)


db.fmtc.bitdepth(bits=10).set_output()




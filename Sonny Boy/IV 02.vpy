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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Sonny Boy\2\IV 02.m2ts')
episode = muf.SmoothGrad(episode, radius=4, elast=4, ref=episode)

mg = episode

clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0.2, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4)
pf = core.dfttest.DFTTest(fd, sigma=3, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=60, cb=60, cr=60, grainy=0, grainc=0, output_depth=16, keep_tv_range=True, blur_first=True)


db.fmtc.bitdepth(bits=10).set_output()
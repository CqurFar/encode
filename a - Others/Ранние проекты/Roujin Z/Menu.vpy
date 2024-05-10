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

episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Roujin Z\BDMV\STREAM\01.m2ts')
 

mg = episode


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
pf = core.dfttest.DFTTest(fd, sigma=1, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=30, cb=30, cr=30, grainy=100, grainc=100, output_depth=16, keep_tv_range=True, blur_first=False)


db.fmtc.bitdepth(bits=10).set_output()
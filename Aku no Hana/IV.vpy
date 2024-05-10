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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Aku no Hana\IV\IV 02.m2ts')
episode = muvs.SmoothGrad(episode, radius=4, elast=4, ref=episode)

episode = haf.QTGMC(episode, Preset='very fast',TFF=True)
episode = haf.srestore(episode, frate=30/1.001, speed=-1, thresh=8)


mg = episode


clip16 = core.fmtc.bitdepth(mg, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=3, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=60, cb=60, cr=60, output_depth=16, blur_first=True)


db.fmtc.bitdepth(bits=10).set_output()
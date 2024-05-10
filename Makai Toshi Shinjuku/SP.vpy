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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Makai Toshi Shinjuku\SP.m2ts')
episode = core.std.Crop(episode, left=4, right=4, top=2, bottom=2)


episode = haf.QTGMC(episode, Preset='placebo',TFF=True)
episode = haf.srestore(episode, frate=24/1.001, speed=-1, thresh=8)


mg = episode


clip16 = core.fmtc.bitdepth(mg, bits=16)
db = core.neo_f3kdb.Deband(clip16, range=25, y=20, cb=10, cr=10, output_depth=16, blur_first=False)
den = cooldegrain.CoolDegrain(db, tr=1, thsad=16, thsadc=10, bits=16, blksize=8, overlap=4, pf=db)

fd1 = fd.fine_dehalo(den, None, 2.2, 2.2, 0, 0.5)
fd2 = fd.fine_dehalo(fd1, None, 2.2, 2.2, 0, 0.5)
dha1 = G41Fun.MaskedDHA(fd2, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)
dha2 = G41Fun.MaskedDHA(dha1, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)

dha2.fmtc.bitdepth(bits=10).set_output()
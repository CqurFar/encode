from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsdpir import DPIR
import vapoursynth as vs
import atomchtools
import beatricetools
import havsfunc as haf
import fvsfunc
import kagefunc
import mvsfunc as mvs
import muvsfunc as mvf
import descale as dsc
import finesharp
import ccd
import MCDenoise 
import cooldegrain
import finedehalo as fd
import insaneAA
import xaa
import vsTAAmbk
import HardAA
import lostfunc
import G41Fun
import lvsfunc
import limit
import vsdehalo


core.num_threads = 24
core.max_cache_size = 30000


episode01 = core.lsmas.LWLibavSource(source=r'E:\Работа\Kaze no Na wa Amnesia\Film 01.mp4')
episode02 = core.lsmas.LWLibavSource(source=r'E:\Работа\Kaze no Na wa Amnesia\Film 02.mp4')


mg = episode01.std.Trim(0, 5548)+episode02+episode01.std.Trim(5789, 114988)


clip16=core.fmtc.bitdepth(mg, bits=16)
clip16.fmtc.bitdepth(bits=10).set_output()
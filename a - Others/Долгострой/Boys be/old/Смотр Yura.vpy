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
import rekt


core.num_threads = 24
core.max_cache_size = 30000


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Boys be\Yurasick\Boys Be ... - 01 [DVDRip 960x720 x264 AC3].mkv').fmtc.bitdepth(bits=8)
episode = core.vivtc.VFM(episode, order=1, field=0)
episode = core.vivtc.VDecimate(episode)



mg = episode


clip16=core.fmtc.bitdepth(mg, bits=16)
clip16.fmtc.bitdepth(bits=10).set_output()
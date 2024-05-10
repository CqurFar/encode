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


core.num_threads = 24
core.max_cache_size = 30000


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Готовое\[Zagzad] Kaze no Na wa Amnesia (AI-DVDRip 1440x1080 HEVC-10bit AC3x2 SRT)\VTS_01_1.mkv')
episode=haf.ChangeFPS(episode, fpsnum=24000, fpsden=1001)

mg = episode

clip16=core.fmtc.bitdepth(mg, bits=16)
clip16.fmtc.bitdepth(bits=10).set_output()
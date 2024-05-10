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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Lovely Complex\EP 01.mkv')
vivtc = core.vivtc.VFM(episode, order=1, field=0)
VFM = core.tivtc.TDecimate(vivtc)
vinv = haf.Vinverse2(VFM)


deint = vinv


cr = core.std.Crop(deint, left=8, right=8)
mg = cr.resize.Bilinear(width=1440, height=1080)


clip16=core.fmtc.bitdepth(mg, bits=16)
clip16.fmtc.bitdepth(bits=10).set_output()
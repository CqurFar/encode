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

episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Night Is Short Walk on Girl 2017 1080p JPN Blu-ray AVC DTS-HD MA 5.1-CrsS\KUROKAMINOOTOME\BDMV\STREAM\Film.m2ts')


mg = episode

clip16=core.fmtc.bitdepth(mg, bits=16)
clip16.fmtc.bitdepth(bits=10).set_output()









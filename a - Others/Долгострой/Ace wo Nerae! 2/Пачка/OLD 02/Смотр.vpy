from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Ace wo Nerae! 2\EP 01.mkv')
episode = core.vivtc.VFM(episode, order=1, field=0)
episode = core.vivtc.VDecimate(episode)
rgbs = core.resize.Lanczos(episode, format=vs.RGBS, matrix_in='1').fmtc.bitdepth(bits=16)
episode01 = core.curve.Curve(rgbs, acv=r'C:\Users\Art\Downloads\01.acv')
episode01 = core.resize.Lanczos(episode01, format=vs.YUV420P8, matrix_s="709")


mg01 = episode01
mg02 = lvsfunc.dpir(mg01, strength=20, mode='denoise', cuda=True, matrix=1)
mg = core.matchhist.MatchHistogram(clip1=episode01, clip2=episode, clip3=mg02, raw=False, show=False, debug=False, smoothing_window=1)


clip16=core.fmtc.bitdepth(mg, bits=16)
clip16.fmtc.bitdepth(bits=10).set_output()
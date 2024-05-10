from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import vapoursynth as vs
import vsgan
from vsgan import ESRGAN
import atomchtools
import beatricetools
import havsfunc as haf
import fvsfunc as fvf
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
core.max_cache_size = 32000


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Ace wo Nerae! 2\EP 01.mkv')

deint_01 = core.vivtc.VFM(episode, order=1, field=0)
deint_01 = core.vivtc.VDecimate(deint_01)

fd1 = fd.fine_dehalo(deint_01, None, 2.2, 2.2, 0, 0.5)
fd2 = fd.fine_dehalo(fd1, None, 2.2, 2.2, 0, 0.5)
dha1 = G41Fun.MaskedDHA(fd2, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)
dha2 = G41Fun.MaskedDHA(dha1, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4).fmtc.bitdepth(bits=32)
dpir  = lvsfunc.dpir(dha2, strength=5, mode='denoise', cuda=True, matrix=1)


cr = core.std.Crop(dpir, left=8, right=8)
rgbs = core.resize.Lanczos(cr, width=792, height=540, format=vs.RGBS, matrix_in='1')


color = core.resize.Lanczos(cr, width=1584, height=1080, format=vs.YUV420P8, matrix_s="709")

ai_01 = core.trt.Model(rgbs, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\4x_OLDIES_290000_G_FINAL_interp_03.engine')


mg = ai_01


clip16 = core.resize.Lanczos(mg, width=1584, height=1080, format=vs.YUV420P8, matrix_s="709")
tn = core.matchhist.MatchHistogram(clip16, clip16, color, raw=False, show=False, debug=False, smoothing_window=1)
gr = core.grain.Add(tn,  var=2, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=1234, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
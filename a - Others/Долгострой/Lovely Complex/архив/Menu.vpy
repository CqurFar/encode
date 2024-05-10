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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Lovely Complex\Menu\Menu 01.mkv')

deint = core.vivtc.VFM(episode, order=1, field=0)
deint = core.vivtc.VDecimate(deint)
deint = haf.QTGMC(deint, Preset='placebo',TFF=True)
deint = haf.srestore(deint, frate=24/1.001, speed=-1, thresh=8)

fd1 = fd.fine_dehalo(deint, None, 2.2, 2.2, 0, 0.5)
fd2 = fd.fine_dehalo(fd1, None, 2.2, 2.2, 0, 0.5)
dha1 = G41Fun.MaskedDHA(fd2, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)
dha2 = G41Fun.MaskedDHA(dha1, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)

pf = core.dfttest.DFTTest(dha2, sigma=1, tbsize=3, opt=0)
db = core.placebo.Deband(pf, threshold=1, radius=10, dither = True, grain = 0)

rgbs = core.resize.Lanczos(db, width=810, height=540, format=vs.RGBS, matrix_in='1')


ai_01 = core.trt.Model(rgbs, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_LD-Anime_Skr_v1.0.engine')


clip16 = core.resize.Lanczos(ai_01, format=vs.YUV420P16, matrix_s="709")
sh = core.cas.CAS(clip16, sharpness=0.8, opt=0)
gr = core.grain.Add(sh,  var=1, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=123456789, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
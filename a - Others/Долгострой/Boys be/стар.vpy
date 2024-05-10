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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Boys be\EP 01.mkv')

deint_01 = core.vivtc.VFM(episode, order=1, field=0)
deint_01 = core.vivtc.VDecimate(deint_01)


fd1 = fd.fine_dehalo(deint_01, None, 2.2, 2.2, 0, 0.5)
fd2 = fd.fine_dehalo(fd1, None, 2.2, 2.2, 0, 0.5)
dha1 = G41Fun.MaskedDHA(fd2, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)
dha2 = G41Fun.MaskedDHA(dha1, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)

aa = HardAA.HardAA(dha2, mask='simple', mthr=0.1)
gr = core.grain.Add(aa,  var=2, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=1234, constant=False, opt=0)
cr = core.std.Crop(gr, left=8, right=8)
rgbs = core.resize.Lanczos(cr, width=792, height=540, format=vs.RGBS, matrix_in='1')

ai_01 = core.trt.Model(rgbs, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_LD-Anime_Skr_v1.0.engine')
ai_02 = core.trt.Model(ai_01, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\1x_ThePi7on-Solidd_Deborutify_UltraLite_260k_G.engine')
ai_03 = core.trt.Model(rgbs, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_SHARP_ANIME_V2.engine')
ai_04 = core.trt.Model(rgbs, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2X_DigitalFilmV5_Lite.engine')
ai_expr = core.std.Expr([ai_01, ai_02], 'x 0.70 * y 0.30 * +')


mg = ai_expr


clip16 = core.resize.Lanczos(mg, format=vs.YUV420P16, matrix_s="709")
gr = core.grain.Add(clip16,  var=2, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=1234, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
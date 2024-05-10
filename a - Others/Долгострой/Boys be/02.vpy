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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Boys be\EP 02.mkv')

deint_01 = core.vivtc.VFM(episode, order=1, field=0)
deint_01 = core.vivtc.VDecimate(deint_01)

deint_02 = haf.QTGMC(deint_01, Preset='placebo',TFF=True)
deint_02 = haf.srestore(deint_02, frate=24/1.001, speed=-1, thresh=8)


deint_all = deint_01.std.Trim(0, 16016)+deint_02.std.Trim(16017, 16304)+deint_01.std.Trim(16305, 33568)


fd1 = fd.fine_dehalo(deint_all, None, 2.2, 2.2, 0, 0.5)
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


mg = ai_04.std.Trim(0, 2158)+ai_expr.std.Trim(2159, 4442)+ai_03.std.Trim(4443, 4589)+ai_expr.std.Trim(4590, 6439)+ai_03.std.Trim(6440, 6571)+ai_expr.std.Trim(6572, 11681)+ai_03.std.Trim(11682, 11845)+ai_expr.std.Trim(11846,11924)+ai_03.std.Trim(11925, 11983)+ai_expr.std.Trim(11984,12706)+ai_03.std.Trim(12707, 12776)+ai_expr.std.Trim(12777, 13475)+ai_03.std.Trim(13476, 13547)+ai_expr.std.Trim(13548, 16016)+ai_04.std.Trim(16017, 16304)+ai_expr.std.Trim(16305, 17593)+ai_03.std.Trim(17594, 17712)+ai_expr.std.Trim(17713, 18327)+ai_03.std.Trim(18328, 18394)+ai_expr.std.Trim(18395, 20340)+ai_03.std.Trim(20341, 20440)+ai_expr.std.Trim(20441, 21129)+ai_03.std.Trim(21130, 21295)+ai_expr.std.Trim(21296, 22661)+ai_03.std.Trim(22662, 22757)+ai_expr.std.Trim(22758, 26675)+ai_03.std.Trim(26676, 26763)+ai_expr.std.Trim(26764, 27275)+ai_03.std.Trim(27276, 27383)+ai_expr.std.Trim(27384, 30185)+ai_03.std.Trim(30186, 30266)+ai_expr.std.Trim(30267, 30499)+ai_03.std.Trim(30500, 30690)+ai_04.std.Trim(30691, 32790)+ai_expr.std.Trim(32791, 33568)


clip16 = core.resize.Lanczos(mg, format=vs.YUV420P16, matrix_s="709")
gr = core.grain.Add(clip16,  var=2, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=1234, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Lovely Complex\EP 01.mkv')

deint = core.vivtc.VFM(episode, order=1, field=0)
deint = core.vivtc.VDecimate(deint)

dehalo_alph1 = vsdehalo.fine_dehalo(deint,None,2.3,2.3,0,0.4,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph1,None,2.3,2.3,0,0.4,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph2,None,2.3,2.3,0,0.3,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph2,None,2.3,2.3,0,0.2,thmi=30,thma=100)
deh = G41Fun.MaskedDHA(dehalo_alph2, rx=2.3, ry=2.3, darkstr=0, brightstr=0.5)
deh = G41Fun.MaskedDHA(deh, rx=2.3, ry=2.3, darkstr=0, brightstr=0.4)

pf = core.dfttest.DFTTest(deh, sigma=1, tbsize=3, opt=0)
db = core.placebo.Deband(pf, threshold=1, radius=10, dither = True, grain = 0)

cr = core.std.Crop(db, left=8, right=8)
rgbs = core.resize.Lanczos(cr, width=720, height=540, format=vs.RGBS, matrix_in='1')

ai_01 = core.trt.Model(rgbs, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\1x_GainRESV3_Passive.engine')
ai_expr_01 = core.std.Expr([rgbs, ai_01], 'x 0.80 * y 0.20 * +')

ai_02 = core.trt.Model(ai_expr_01, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_KemonoScale_v2.engine')
ai_03 = core.trt.Model(ai_02, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\1x_ThePi7on-Solidd_Deborutify_UltraLite_260k_G.engine')
ai_expr_02 = core.std.Expr([ai_02, ai_03], 'x 0.80 * y 0.20 * +')


clip16 = core.resize.Lanczos(ai_expr_02, format=vs.YUV420P16, matrix_s="709")
sh = core.cas.CAS(clip16, sharpness=0.8, opt=0)
gr = core.grain.Add(sh,  var=1, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=123456789, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
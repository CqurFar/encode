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
import vsdenoise
import vsmask
from vsutil import get_y
import vskernels


core.num_threads = 24
core.max_cache_size = 32000


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Lovely Complex\EP 02.mkv')

vivtc = core.vivtc.VFM(episode, order=1, field=0)
tivtc = core.tivtc.TFM(vivtc, order=-1, field=-1, mode=1, slow=2, mChroma=True)

VFM = core.tivtc.TDecimate(vivtc)
TFM = core.tivtc.TDecimate(tivtc)


deint = TFM.std.Trim(0, 1030)+VFM.std.Trim(1031, 1165)+TFM.std.Trim(1166, 34069)


src_y = get_y(deint)
masky = vsmask.edge.DoG().edgemask(src_y,0,multi=1).std.Inflate()
mask_out = vsmask.util.expand(masky,4,4)
mask = core.std.Expr([masky,mask_out],'y x -')
deh = vsdehalo.HQDeringmod(deint,vsdenoise.Prefilter.MINBLUR2,mask,darkthr=40)
dehalo_alph1 = vsdehalo.fine_dehalo(deh,None,2.3,2.3,0,0.4,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph1,None,2.3,2.3,0,0.4,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph2,None,2.3,2.3,0,0.3,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph2,None,2.3,2.3,0,0.2,thmi=30,thma=100)
deh = G41Fun.MaskedDHA(dehalo_alph2, rx=2.3, ry=2.3, darkstr=0, brightstr=0.5)
deh = G41Fun.MaskedDHA(deh, rx=2.3, ry=2.3, darkstr=0, brightstr=0.4)


pf = core.dfttest.DFTTest(deh, sigma=1, tbsize=3, opt=0)
db = core.placebo.Deband(pf, threshold=2, radius=12, dither = True, grain = 0)

cr = core.std.Crop(db, left=8, right=8)
rgbs = core.resize.Lanczos(cr, width=1440, height=1080, format=vs.RGBS, matrix_in='1')


esrgan = ESRGAN(rgbs, device="cuda")
vsgan.networks.esrgan.ESRGAN
esrgan.load(r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\1x_BleedOut_Compact_300k_net_g.pth')
vsgan.networks.esrgan.ESRGAN
esrgan.apply()
vsgan.networks.esrgan.ESRGAN
ai_01 = esrgan.clip

ai_02 = core.trt.Model(rgbs, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_KemonoScale_v2.engine').resize.Lanczos(width=1440, height=1080)
ai_expr = core.std.Expr([ai_02, ai_01], 'x 0.70 * y 0.30 * +')


clip16 = core.resize.Lanczos(ai_expr, format=vs.YUV420P16, width=1440, height=1080, matrix_s="709")


def hard720(clip16):
    gray = core.std.ShufflePlanes(clip16, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=1.2, kernel='Lanczos', descale_height=540) 
    rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=1, dx=1440, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(rescale, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(clip16, 1, GRAY)
    v = core.std.ShufflePlanes(clip16, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1, useCL=True)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1, useCL=True)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1, useCL=True)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], clip16.format.color_family)
    return mixyuv

aa = hard720(clip16)


sh = core.cas.CAS(aa, sharpness=0.8, opt=0)
gr = core.grain.Add(sh,  var=1, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=123456789, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
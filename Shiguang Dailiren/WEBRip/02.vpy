from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import atomchtools as atf
import beatricetools as bea
import havsfunc as haf
import fvsfunc as fvf
import kagefunc as kg
import mvsfunc as mvf
import muvsfunc as muf
import descale as dsc
import ccd
import MCDenoise 
import cooldegrain
import finedehalo as fd
import insaneAA
import xaa
import vsTAAmbk as taa
import HardAA




episode = core.lsmas.LWLibavSource(source=r'E:\Работа\[Erai-raws] Shiguang Dailiren\[Erai-raws] Shiguang Dailiren - 02.mkv')
episode = core.std.Crop(episode, top=140, bottom=140)
episode = haf.ChangeFPS(episode, fpsnum=24000, fpsden=1001)


mg = episode.std.Trim(789, 32138)


def hard420(mg):
    gray = core.std.ShufflePlanes(mg, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.5, kernel='bicubic', descale_height=420) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=800, nsize=6)  
    aa = insaneAA.insaneAA(mg, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(mg, 1, GRAY)
    v = core.std.ShufflePlanes(mg, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1, useCL=True)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1, useCL=True)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1, useCL=True)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], mg.format.color_family)
    return mixyuv
    
def hard(mg):
    gray = core.std.ShufflePlanes(mg, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.35, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33)
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=800, nsize=6)  
    aa = insaneAA.insaneAA(mg, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(mg, 1, GRAY)
    v = core.std.ShufflePlanes(mg, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1, useCL=True)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1, useCL=True)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1, useCL=True)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], mg.format.color_family)
    return mixyuv
    
def insuin(mg):
    gray = core.std.ShufflePlanes(mg, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.45, kernel='bicubic', descale_height=680, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=800, nsize=6)  
    aa = insaneAA.insaneAA(mg, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, mg, mg], [0,1,2], mg.format.color_family)
    return mixyuv 

titi = hard420(mg)

pipi = hard(mg)

iti = insuin(mg)


mg2 = iti.std.Trim(0, 1075)+titi.std.Trim(1076, 1137)+iti.std.Trim(1138, 1248)+mg.std.Trim(1249, 2756)+iti.std.Trim(2757, 4722)+titi.std.Trim(4723, 4805)+iti.std.Trim(4806, 9272)+pipi.std.Trim(9273, 9574)+iti.std.Trim(9575, 9665)+pipi.std.Trim(9666, 10410)+iti.std.Trim(10411, 10855)+pipi.std.Trim(10856, 11151)+iti.std.Trim(11152, 11228)+pipi.std.Trim(11229, 11453)+iti.std.Trim(11454, 12015)+pipi.std.Trim(12016, 12093)+iti.std.Trim(12094, 31345)+mg.std.Trim(31346, 31349)


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
pf = core.dfttest.DFTTest(fd, sigma=3, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=60, cb=60, cr=60, grainy=90, grainc=90, output_depth=16, keep_tv_range=True, blur_first=True)


db.fmtc.bitdepth(bits=10).set_output()
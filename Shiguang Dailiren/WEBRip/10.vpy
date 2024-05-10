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




episode = core.lsmas.LWLibavSource(source=r'E:\Работа\[Erai-raws] Shiguang Dailiren\[Erai-raws] Shiguang Dailiren - 10.mkv')
episode = core.std.Crop(episode, top=140, bottom=140)
episode = haf.ChangeFPS(episode, fpsnum=24000, fpsden=1001) 


mg = episode.std.Trim(789, 31256)


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


mg2 = mg.std.Trim(0, 348)+iti.std.Trim(349, 977)+mg.std.Trim(978, 1031)+iti.std.Trim(1032, 1491)+mg.std.Trim(1492, 1711)+iti.std.Trim(1712, 1933)+mg.std.Trim(1934, 2169)+iti.std.Trim(2170, 2385)+mg.std.Trim(2386, 4031)+iti.std.Trim(4032, 5465)+iti.std.Trim(5466, 5532)+iti.std.Trim(5533, 5972)+mg.std.Trim(5973, 6047)+iti.std.Trim(6048, 7828)+mg.std.Trim(7829, 8017)+iti.std.Trim(8018, 9762)+mg.std.Trim(9763, 9903)+iti.std.Trim(9904, 10562)+mg.std.Trim(10563, 10700)+iti.std.Trim(10701, 11160)+mg.std.Trim(11161, 11316)+iti.std.Trim(11317, 12754)+mg.std.Trim(12755, 12919)+iti.std.Trim(12920, 13180)+mg.std.Trim(13181, 13295)+iti.std.Trim(13296, 15106)+mg.std.Trim(15107, 15785)+iti.std.Trim(15786, 16739)+mg.std.Trim(16740, 17116)+iti.std.Trim(17117, 19218)+mg.std.Trim(19219, 19392)+iti.std.Trim(19393, 19824)+mg.std.Trim(19825, 20112)+iti.std.Trim(20113, 21533)+mg.std.Trim(21534, 21773)+iti.std.Trim(21774, 22202)+mg.std.Trim(22203, 22615)+iti.std.Trim(22616, 23708)+mg.std.Trim(23709, 23840)+iti.std.Trim(23841, 24080)+mg.std.Trim(24081, 24586)+iti.std.Trim(24587, 24862)+mg.std.Trim(24863, 25119)+iti.std.Trim(25120, 25427)+mg.std.Trim(25428, 25502)+iti.std.Trim(25503, 30467)


clip16 = core.fmtc.bitdepth(mg2, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
pf = core.dfttest.DFTTest(fd, sigma=3, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=60, cb=60, cr=60, grainy=90, grainc=90, output_depth=16, keep_tv_range=True, blur_first=True)


db.fmtc.bitdepth(bits=10).set_output()
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




episode = core.lsmas.LWLibavSource(source=r'E:\Работа\[Erai-raws] Shiguang Dailiren\[Erai-raws] Shiguang Dailiren - 11.mkv')
episode = core.std.Crop(episode, top=140, bottom=140)
episode = haf.ChangeFPS(episode, fpsnum=24000, fpsden=1001) 


mg = episode.std.Trim(789, 42835)


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


mg2 = mg.std.Trim(0, 104)+iti.std.Trim(105, 800)+mg.std.Trim(801, 854)+iti.std.Trim(855, 2447)+mg.std.Trim(2448, 2550)+iti.std.Trim(2551, 3652)+mg.std.Trim(3653, 5163)+iti.std.Trim(5164, 5863)+mg.std.Trim(5864, 5887)+iti.std.Trim(5888, 8690)+iti.std.Trim(8691, 8837)+iti.std.Trim(8838, 9773)+mg.std.Trim(9774, 10415)+iti.std.Trim(10416, 10677)+mg.std.Trim(10678, 10856)+iti.std.Trim(10857, 10943)+mg.std.Trim(10944, 11598)+iti.std.Trim(11599, 11737)+mg.std.Trim(11738, 12027)+iti.std.Trim(12028, 12388)+mg.std.Trim(12389, 12480)+iti.std.Trim(12481, 12671)+mg.std.Trim(12672, 13440)+iti.std.Trim(13441, 16096)+mg.std.Trim(16097, 16171)+iti.std.Trim(16172, 16809)+mg.std.Trim(16810, 16980)+iti.std.Trim(16981, 18669)+mg.std.Trim(18670, 18873)+iti.std.Trim(18874, 19460)+mg.std.Trim(19461, 19553)+iti.std.Trim(19554, 22970)+mg.std.Trim(22971, 23091)+iti.std.Trim(23092, 24783)+mg.std.Trim(24784, 25020)+iti.std.Trim(25021, 27089)+mg.std.Trim(27090, 27883)+iti.std.Trim(27884, 28535)+mg.std.Trim(28536, 28733)+iti.std.Trim(28734, 35070)+mg.std.Trim(35071, 35180)+iti.std.Trim(35181, 38203)+mg.std.Trim(38204, 38300)+iti.std.Trim(38301, 42046)


clip16 = core.fmtc.bitdepth(mg2, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
pf = core.dfttest.DFTTest(fd, sigma=3, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=60, cb=60, cr=60, grainy=90, grainc=90, output_depth=16, keep_tv_range=True, blur_first=True)


db.fmtc.bitdepth(bits=10).set_output()
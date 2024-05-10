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




episode = core.lsmas.LWLibavSource(source=r'E:\Работа\[Erai-raws] Shiguang Dailiren\[Erai-raws] Shiguang Dailiren - 08.mkv')
episode = core.std.Crop(episode, top=140, bottom=140)
episode = haf.ChangeFPS(episode, fpsnum=24000, fpsden=1001)


mg = episode.std.Trim(789, 32656)


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


mg2 = iti.std.Trim(0, 1348)+mg.std.Trim(1349, 1459)+iti.std.Trim(1460, 1868)+mg.std.Trim(1869, 1905)+iti.std.Trim(1906, 2219)+mg.std.Trim(2220, 2348)+iti.std.Trim(2349, 2782)+mg.std.Trim(2783, 4324)+mg.std.Trim(4325, 4535)+iti.std.Trim(4536, 4795)+mg.std.Trim(4796, 4941)+iti.std.Trim(4942, 7010)+mg.std.Trim(7011, 7352)+iti.std.Trim(7353, 9072)+mg.std.Trim(9073, 9665)+iti.std.Trim(9666, 9888)+mg.std.Trim(9889, 10125)+iti.std.Trim(10126, 10328)+mg.std.Trim(10329, 10682)+iti.std.Trim(10683, 11034)+mg.std.Trim(11035, 11725)+iti.std.Trim(11726, 13037)+mg.std.Trim(13038, 13291)+iti.std.Trim(13292, 14363)+mg.std.Trim(14364, 14468)+iti.std.Trim(14469, 14987)+mg.std.Trim(14988, 15080)+iti.std.Trim(15081, 15752)+mg.std.Trim(15753, 15909)+iti.std.Trim(15910, 16194)+mg.std.Trim(16195, 16256)+iti.std.Trim(16257, 16795)+mg.std.Trim(16796, 16954)+iti.std.Trim(16955, 18133)+mg.std.Trim(18134, 19159)+iti.std.Trim(19160, 19512)+mg.std.Trim(19513, 19635)+iti.std.Trim(19636, 19845)+mg.std.Trim(19846, 19968)+iti.std.Trim(19969, 20949)+mg.std.Trim(20950, 21054)+iti.std.Trim(21055, 21419)+mg.std.Trim(21420, 21785)+iti.std.Trim(21786, 22000)+mg.std.Trim(22001, 22428)+iti.std.Trim(22429, 23538)+mg.std.Trim(23539, 24626)+iti.std.Trim(24627, 25072)+mg.std.Trim(25073, 25635)+iti.std.Trim(25636, 27194)+mg.std.Trim(27195, 27352)+iti.std.Trim(27353, 28023)+mg.std.Trim(28024, 28214)+iti.std.Trim(28215, 29638)+mg.std.Trim(29639, 29731)+iti.std.Trim(29732, 31867)


clip16 = core.fmtc.bitdepth(mg2, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
pf = core.dfttest.DFTTest(fd, sigma=3, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=60, cb=60, cr=60, grainy=90, grainc=90, output_depth=16, keep_tv_range=True, blur_first=True)


db.fmtc.bitdepth(bits=10).set_output()
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




episode = core.lsmas.LWLibavSource(source=r'E:\Работа\[Erai-raws] Shiguang Dailiren\[Erai-raws] Shiguang Dailiren - 05.mkv')
episode = core.std.Crop(episode, top=140, bottom=140)
episode = haf.ChangeFPS(episode, fpsnum=24000, fpsden=1001) 


mg = episode.std.Trim(789, 35277)


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


mg2 = iti.std.Trim(0, 1596)+mg.std.Trim(1597, 1671)+iti.std.Trim(1672, 2379)+mg.std.Trim(2380, 2445)+iti.std.Trim(2446, 3029)+mg.std.Trim(3030, 3119)+iti.std.Trim(3120, 4059)+mg.std.Trim(4060, 5537)+iti.std.Trim(5538, 9628)+mg.std.Trim(9629, 9898)+iti.std.Trim(9899, 10509)+mg.std.Trim(10510, 10632)+iti.std.Trim(10633, 11778)+mg.std.Trim(11779, 11941)+iti.std.Trim(11942, 12980)+pipi.std.Trim(12981, 13056)+iti.std.Trim(13057, 13549)+titi.std.Trim(13550, 13612)+mg.std.Trim(13613, 13690)+iti.std.Trim(13691, 13762)+pipi.std.Trim(13763, 13846)+mg.std.Trim(13847, 13886)+iti.std.Trim(13887, 15747)+mg.std.Trim(15748, 15813)+iti.std.Trim(15814, 16197)+mg.std.Trim(16198, 16262)+iti.std.Trim(16263, 17155)+mg.std.Trim(17156, 17282)+iti.std.Trim(17283, 21679)+mg.std.Trim(21680, 21861)+iti.std.Trim(21862, 23196)+titi.std.Trim(23197, 23298)+iti.std.Trim(23299, 26164)+mg.std.Trim(26165, 26379)+iti.std.Trim(26380, 26661)+mg.std.Trim(26662, 26808)+iti.std.Trim(26809, 34488)


clip16 = core.fmtc.bitdepth(mg2, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
pf = core.dfttest.DFTTest(fd, sigma=3, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=60, cb=60, cr=60, grainy=90, grainc=90, output_depth=16, keep_tv_range=True, blur_first=True)


db.fmtc.bitdepth(bits=10).set_output()
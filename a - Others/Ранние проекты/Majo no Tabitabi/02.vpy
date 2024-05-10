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



episode=core.lsmas.LWLibavSource(source=r'E:\Работа\Eleina\[BDMV][210127] Blu-ray BOX\MAJO_NO_TABITABI_1\BDMV\STREAM\00004.m2ts')

episode=core.neo_f3kdb.Deband(episode, y=60, cb=60, cr=60, grainy=30, grainc=30, output_depth=16, keep_tv_range=True, blur_first=True)

def alisa(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.3, kernel='bicubic', descale_height=720) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(episode, 1, GRAY)
    v = core.std.ShufflePlanes(episode, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1, useCL=True)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1, useCL=True)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1, useCL=True)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], episode.format.color_family)
    return mixyuv
    
def alisa240(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.4, kernel='bicubic', descale_height=240) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(episode, 1, GRAY)
    v = core.std.ShufflePlanes(episode, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1, useCL=True)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1, useCL=True)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1, useCL=True)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], episode.format.color_family)
    return mixyuv
    
def inn(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.3, kernel='bicubic', descale_height=720) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2, useMtEdge=True)   
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6) 
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv


pipi = alisa(episode) #pipi = HardAA.HardAA(episode, mask='simple', mthr=0.1, useCL=True) tutu = core.std.Expr([iti, pipi], 'x 0.70 * y 0.30 * +')

hihi = alisa240(episode)

iti = inn(episode)

op = iti.std.Trim(888, 1094)+pipi.std.Trim(1095, 1192)+iti.std.Trim(1193, 1290)+pipi.std.Trim(1291, 1359)+iti.std.Trim(1360, 3044)
ed = episode.std.Trim(31912, 32973)+pipi.std.Trim(32974, 33254)+episode.std.Trim(33255, 34069)

mg = iti.std.Trim(0, 887)+op+iti.std.Trim(3045, 3519)+pipi.std.Trim(3520, 3756)+iti.std.Trim(3757, 4888)+pipi.std.Trim(4889, 4985)+iti.std.Trim(4986, 5028)+pipi.std.Trim(5029, 5081)+iti.std.Trim(5082, 5326)+pipi.std.Trim(5327, 5388)+iti.std.Trim(5389, 9706)+pipi.std.Trim(9707, 9844)+iti.std.Trim(9845, 11730)+pipi.std.Trim(11731, 11762)+iti.std.Trim(11763, 21334)+pipi.std.Trim(21335, 21418)+iti.std.Trim(21419, 27621)+pipi.std.Trim(27622, 27816)+iti.std.Trim(27817, 31911)+ed+episode.std.Trim(34070, 34093)


mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Eleina\[BDMV][210127] Blu-ray BOX\MAJO_NO_TABITABI_1\BDMV\STREAM\Скрипты\Маски\S01E01-01.png'), "[32986 33105]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Eleina\[BDMV][210127] Blu-ray BOX\MAJO_NO_TABITABI_1\BDMV\STREAM\Скрипты\Маски\S01E01-02.png'), "[33118 33237]")


clip16=core.fmtc.bitdepth(mg, bits=16)
clip16.fmtc.bitdepth(bits=10).set_output()






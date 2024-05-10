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



episode=core.lsmas.LWLibavSource(source=r'E:\Работа\Eleina\[BDMV][210127] Blu-ray BOX\MAJO_NO_TABITABI_1\BDMV\STREAM\00003.m2ts')

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

#mg = episode.std.Trim(0, 230)+pipi.std.Trim(231, 328)+episode.std.Trim(329, 426)+pipi.std.Trim(427, 495)+iti.std.Trim(496, 621)+episode.std.Trim(622, 1938)+iti.std.Trim(1939, 1986)+episode.std.Trim(1987, 2207)
mg = iti.std.Trim(0, 2445)+pipi.std.Trim(2446, 2600)+iti.std.Trim(2601, 34429)+episode.std.Trim(34430, 34573)


#mg = fvf.rfs(mg, core.neo_f3kdb.Deband(episode, y=120, cb=120, cr=120, grainy=10, grainc=10,dynamic_grain=False, blur_first=True), "[33951 33980]")#Дабан Next
#mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Eleina\[BDMV][210127] 魔女の旅々 Blu-ray BOX 上巻\MAJO_NO_TABITABI_1\BDMV\STREAM\Скрипты\Маски\Menu-01.png'), "[408 5183]")


clip16=core.fmtc.bitdepth(mg, bits=16)
clip16.fmtc.bitdepth(bits=10).set_output()






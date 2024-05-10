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



episode=core.lsmas.LWLibavSource(source=r'E:\Работа\Eleina\[BDMV][210127] Blu-ray BOX\MAJO_NO_TABITABI_2\BDMV\STREAM\00006.m2ts')

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
    desc = insaneAA.revert_upscale(gray, descale_strength=0.4, kernel='bicubic', descale_height=480) 
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
    
def inn(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.3, kernel='bicubic', descale_height=720) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2, useMtEdge=True)   
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6) 
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv


pipi = alisa(episode) #pipi = HardAA.HardAA(episode, mask='simple', mthr=0.1, useCL=True) tutu = core.std.Expr([iti, pipi], 'x 0.70 * y 0.30 * +')

hihi = alisa240(episode)

iti = inn(episode)

op = iti.std.Trim(1750, 1956)+pipi.std.Trim(1957, 2054)+iti.std.Trim(2055, 2152)+pipi.std.Trim(2153, 2221)+iti.std.Trim(2222, 3908)
#ed = episode.std.Trim(31913, 32974)+pipi.std.Trim(32975, 33255)+episode.std.Trim(33256, 34070)

mg = iti.std.Trim(0, 1749)+op+iti.std.Trim(3909, 9758)+pipi.std.Trim(9759, 9817)+iti.std.Trim(9818, 14855)+hihi.std.Trim(14856, 14859)+iti.std.Trim(14860, 18310)+pipi.std.Trim(18311, 18733)+iti.std.Trim(18734, 18805)+pipi.std.Trim(18806, 19231)+iti.std.Trim(19232, 19338)+pipi.std.Trim(19339, 19482)+iti.std.Trim(19483, 20023)+pipi.std.Trim(20024, 20882)+iti.std.Trim(20883, 21673)+pipi.std.Trim(21674, 21726)+iti.std.Trim(21727, 22134)+pipi.std.Trim(22135, 22227)+iti.std.Trim(22228, 28387)+pipi.std.Trim(28388, 28465)+iti.std.Trim(28466, 34574)

#mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Eleina\[BDMV][210127] Blu-ray BOX\MAJO_NO_TABITABI_2\BDMV\STREAM\Скрипты\Маски\S01E01-01.png'), "[32987 33106]")
#mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Eleina\[BDMV][210127] Blu-ray BOX\MAJO_NO_TABITABI_2\BDMV\STREAM\Скрипты\Маски\S01E01-02.png'), "[33119 33238]")


clip16=core.fmtc.bitdepth(mg, bits=16)
clip16.fmtc.bitdepth(bits=10).set_output()






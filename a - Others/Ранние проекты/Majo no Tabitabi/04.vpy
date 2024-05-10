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



episode=core.lsmas.LWLibavSource(source=r'E:\Работа\Eleina\[BDMV][210127] Blu-ray BOX\MAJO_NO_TABITABI_1\BDMV\STREAM\00011.m2ts')

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

op = iti.std.Trim(984, 1190)+pipi.std.Trim(1191, 1288)+iti.std.Trim(1289, 1386)+pipi.std.Trim(1387, 1455)+iti.std.Trim(1456, 3140)
ed = episode.std.Trim(32393, 33454)+pipi.std.Trim(33455, 33735)+episode.std.Trim(33736, 34550) 

mg = iti.std.Trim(0, 983)+op+iti.std.Trim(3141, 5745)+pipi.std.Trim(5746, 6239)+iti.std.Trim(6240, 7712)+pipi.std.Trim(7713, 7952)+iti.std.Trim(7953, 9051)+pipi.std.Trim(9052, 9693)+iti.std.Trim(9694, 10573)+pipi.std.Trim(10574, 10789)+iti.std.Trim(10790, 10885)+pipi.std.Trim(10886, 10965)+iti.std.Trim(10966, 15807)+pipi.std.Trim(15808, 15890)+iti.std.Trim(15891, 17245)+pipi.std.Trim(17246, 17813)+iti.std.Trim(17814, 32392)+ed+episode.std.Trim(34551, 34574)

mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Eleina\[BDMV][210127] Blu-ray BOX\MAJO_NO_TABITABI_1\BDMV\STREAM\Скрипты\Маски\S01E01-01.png'), "[33467 33586]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Eleina\[BDMV][210127] Blu-ray BOX\MAJO_NO_TABITABI_1\BDMV\STREAM\Скрипты\Маски\S01E01-02.png'), "[33599 33718]")


clip16=core.fmtc.bitdepth(mg, bits=16)
clip16.fmtc.bitdepth(bits=10).set_output()






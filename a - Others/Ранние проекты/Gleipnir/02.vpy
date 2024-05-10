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

episode = core.lsmas.LWLibavSource(source=r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\00014.m2ts')

episode = muf.SmoothGrad(episode, radius=3, elast=3, ref=episode)
episode = core.neo_f3kdb.Deband(episode, y=30, cb=30, cr=30, grainy=20, grainc=20, dynamic_grain=False, blur_first=True)

def alisa(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.4, kernel='bicubic', descale_height=720) 
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
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.3, showmask=0, thmi=500, thma=95, rx=5.4, ry=5.4, useMtEdge=True)    
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6) 
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv


pipi = alisa(episode) #pipi = HardAA.HardAA(episode, mask='simple', mthr=0.1, useCL=True) tutu = core.std.Expr([iti, pipi], 'x 0.70 * y 0.30 * +')

hihi = alisa240(episode)

iti = inn(episode)

mg = iti.std.Trim(0, 1680)+iti.std.Trim(1681, 1806)+pipi.std.Trim(1807, 1839)+iti.std.Trim(1840, 1960)+episode.std.Trim(1961, 2119)+iti.std.Trim(2120, 2196)+pipi.std.Trim(2197, 2230)+iti.std.Trim(2231, 2697)+pipi.std.Trim(2698, 2896)+iti.std.Trim(2897, 3454)+pipi.std.Trim(3455, 3532)+iti.std.Trim(3533, 3771)+hihi.std.Trim(3772, 3779)+iti.std.Trim(3780, 3836)+iti.std.Trim(3837, 16006)+pipi.std.Trim(16007, 16084)+iti.std.Trim(16085, 18994)+pipi.std.Trim(18995, 19186)+iti.std.Trim(19187, 19450)+pipi.std.Trim(19451, 19555)+iti.std.Trim(19556, 31792)+episode.std.Trim(31793, 34094)

mg = fvf.rfs(mg, core.neo_f3kdb.Deband(pipi, y=80, cb=80, cr=80, grainy=20, grainc=20,dynamic_grain=False, blur_first=True), "[1807 1839]")# Дебан OP
mg = fvf.rfs(mg, core.neo_f3kdb.Deband(iti, y=60, cb=60, cr=60, grainy=20, grainc=20,dynamic_grain=False, blur_first=True), "[2483 2553]")# Дебан OP
mg = fvf.rfs(mg, core.neo_f3kdb.Deband(iti, y=80, cb=80, cr=80, grainy=20, grainc=20,dynamic_grain=False, blur_first=True), "[3650 3700]")# Дебан OP

#mg = fvf.rfs(mg, core.neo_f3kdb.Deband(iti, y=100, cb=100, cr=100, grainy=40, grainc=40,dynamic_grain=False, blur_first=True), "[18540 18806]")

mg = fvf.rfs(mg, core.neo_f3kdb.Deband(episode, y=80, cb=80, cr=80, grainy=40, grainc=40,dynamic_grain=False, blur_first=True), "[31793 31883]")#Дабан ED
mg = fvf.rfs(mg, core.neo_f3kdb.Deband(episode, y=120, cb=120, cr=120, grainy=10, grainc=10,dynamic_grain=False, blur_first=True), "[33951 33980]")#Дабан Next

#OP маски
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\01.png'), "[1687 1757]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\02.png'), "[2122 2194]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\03.png'), "[2197 2266]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\04.png'), "[2269 2347]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\05.png'), "[2407 2481]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\06.png'), "[2484 2553]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\07.png'), "[2554 2622]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\08.png'), "[2625 2696]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\09.png'), "[2699 2761]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\10.png'), "[2765 2828]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\11.png'), "[2831 2895]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\12.png'), "[2981 3044]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\13.png'), "[3133 3197]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\14.png'), "[3260 3324]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\15.png'), "[3352 3423]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\16.png'), "[3574 3700]") 
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\OP\17.png'), "[3775 3836]") 

op = mg.std.Trim(1681, 3836)



episode2 = core.lsmas.LWLibavSource(source=r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\00015.m2ts')

episode2 = muf.SmoothGrad(episode2, radius=3, elast=3, ref=episode2)
episode2 = core.neo_f3kdb.Deband(episode2, y=40, cb=40, cr=40, grainy=20, grainc=20, dynamic_grain=False, blur_first=True)

pipi2 = alisa(episode2) #pipi = HardAA.HardAA(episode, mask='simple', mthr=0.1, useCL=True) tutu = core.std.Expr([iti, pipi], 'x 0.70 * y 0.30 * +')
hihi2 = alisa240(episode2)
iti2 = inn(episode2)

mg2 = iti2.std.Trim(0, 26)+op+iti2.std.Trim(2182, 4525)+pipi2.std.Trim(4526, 4599)+iti2.std.Trim(4600, 10425)+pipi2.std.Trim(10426, 10532)+iti2.std.Trim(10533, 13285)+pipi2.std.Trim(13286, 13404)+iti2.std.Trim(13405, 30079)+pipi2.std.Trim(30080, 30397)+iti2.std.Trim(30398, 31077)+pipi2.std.Trim(31078, 31329)+iti2.std.Trim(31330, 31647)+pipi2.std.Trim(31648, 31695)+iti2.std.Trim(31696, 31791)+episode2.std.Trim(31792, 34091)

mg2 = fvf.rfs(mg2, core.neo_f3kdb.Deband(iti2, y=110, cb=110, cr=110, grainy=40, grainc=40,dynamic_grain=False, blur_first=True), "[13473 13560]")
mg2 = fvf.rfs(mg2, core.neo_f3kdb.Deband(iti2, y=110, cb=110, cr=110, grainy=40, grainc=40,dynamic_grain=False, blur_first=True), "[19810 19935]")

mg = fvf.rfs(mg2, core.neo_f3kdb.Deband(episode2, y=80, cb=80, cr=80, grainy=40, grainc=40,dynamic_grain=False, blur_first=True), "[31792 31882]")#Дабан ED
mg = fvf.rfs(mg2, core.neo_f3kdb.Deband(episode2, y=120, cb=120, cr=120, grainy=10, grainc=10,dynamic_grain=False, blur_first=True), "[33950 33980]")#Дабан Next

mg2 = fvf.rfs(mg2, atf.ApplyImageMask(mg2, episode2, r'E:\Раздачи\[BDMV] Gleipnir\Gleipnir_D1\BDMV\STREAM\Маски\Серии\02_01.png'), "[31036 31077]") 

clip16 = core.fmtc.bitdepth(mg2, bits=16)
clip16.fmtc.bitdepth(bits=10).set_output()#15925


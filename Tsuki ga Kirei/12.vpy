from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import atomchtools as atf
import beatricetools as bea
import havsfunc as haf
import fvsfunc as fvf
import kagefunc as kg
import mvsfunc as mvf
import muvsfunc as muf
import descale as dsc
import finesharp
import ccd
import MCDenoise 
import cooldegrain
import finedehalo as fd
import insaneAA
import xaa
import vsTAAmbk as taa
import HardAA


core.num_threads = 24
core.max_cache_size = 30000


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Ep 12.m2ts')


def hard360(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.6, kernel='bicubic', descale_height=360, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.3, brightstr=0.2, showmask=0, thmi=50, thma=95, rx=2, ry=2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(episode, 1, GRAY)
    v = core.std.ShufflePlanes(episode, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1, useCL=True)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1, useCL=True)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1, useCL=True)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], episode.format.color_family)
    return mixyuv
    
    
def hard720(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.8, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.3, brightstr=0.2, showmask=0, thmi=50, thma=95, rx=2, ry=2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(episode, 1, GRAY)
    v = core.std.ShufflePlanes(episode, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1, useCL=True)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1, useCL=True)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1, useCL=True)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], episode.format.color_family)
    return mixyuv
    

def insuin(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.4, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.3, brightstr=0.2, showmask=0, thmi=50, thma=95, rx=2, ry=2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv

    
titi = hard360(episode)

ed = hard720(episode)

iti = insuin(episode)


mg = iti.std.Trim(0, 11282)+episode.std.Trim(11283, 11337)+iti.std.Trim(11338, 14037)+titi.std.Trim(14038, 14109)+iti.std.Trim(14110, 28565)+titi.std.Trim(28566, 28649)+iti.std.Trim(28650, 29480)+titi.std.Trim(29481, 29516)+iti.std.Trim(29517, 29713)+titi.std.Trim(29714, 29761)+iti.std.Trim(29762, 30805)+titi.std.Trim(30806, 30901)+iti.std.Trim(30902, 32820)+episode.std.Trim(32821, 34670)+iti.std.Trim(34671, 35051)


#Алясинг
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[315 401]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[4626 4709]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[5320 5461]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[9801 9992]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[10041 10132]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[10196 10250]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[14038 14109]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[14254 14337]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[21453 21560]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[28108 28167]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[28566 28649]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[29042 29116]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[29481 29516]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[29564 29659]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[29714 29761]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[30806 30901]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[32918 34670]")


#Маски на опенинг
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.01.png'), "[32 110]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.02.png'), "[111 175]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.03.png'), "[176 243]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.04.png'), "[244 314]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.05.png'), "[339 401]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.06.png'), "[447 542]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.07.png'), "[543 638]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.08.png'), "[639 731]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.09.png'), "[732 815]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.10.png'), "[819 902]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.11.png'), "[906 989]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.12.png'), "[993 1077]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.13.png'), "[1078 1149]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.14.png'), "[1153 1224]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.15.png'), "[1228 1299]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.16.png'), "[1312 1419]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.17.png'), "[1444 1551]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.18.png'), "[1576 1677]")


#Маски на эндинг
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-12.01.png'), "[28108 28167]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-12.02.png'), "[28276 28347]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-12.03.png'), "[28348 28413]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-12.04.png'), "[28889 28993]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-12.05.png'), "[29564 29659]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-12.06.png'), "[32446 32543]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-12.07.png'), "[32544 32639]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-12.08.png'), "[32666 32776]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-12.09.png'), "[34968 35027]")


clip16 = core.fmtc.bitdepth(mg, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1.2, tbsize=3, opt=3)
fd = fd.fine_dehalo(pf, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4)
db = core.neo_f3kdb.Deband(fd, range=25, y=20, cb=10, cr=10, grainy=80, grainc=40, output_depth=16, dynamic_grain=True, keep_tv_range=True, blur_first=True)


db.fmtc.bitdepth(bits=10).set_output()
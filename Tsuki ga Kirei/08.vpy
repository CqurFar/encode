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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Ep 08.m2ts')


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


mg = iti.std.Trim(0, 1936)+titi.std.Trim(1937, 1984)+iti.std.Trim(1985, 2315)+titi.std.Trim(2316, 2397)+iti.std.Trim(2398, 14182)+ed.std.Trim(14183, 14251)+iti.std.Trim(14252, 15624)+titi.std.Trim(15625, 15659)+iti.std.Trim(15660, 28674)+episode.std.Trim(28675, 28796)+ed.std.Trim(28797, 30952)+episode.std.Trim(30953, 31024)+iti.std.Trim(31025, 31799)+episode.std.Trim(31800, 31871)+iti.std.Trim(31872, 32235)+episode.std.Trim(32236, 32307)+iti.std.Trim(32308, 32614)+episode.std.Trim(32615, 32686)+iti.std.Trim(32687, 33160)+episode.std.Trim(33161, 33232)+iti.std.Trim(33233, 33687)+episode.std.Trim(33688, 33759)+iti.std.Trim(33760, 34103)+episode.std.Trim(34104, 34175)+iti.std.Trim(34176, 35051)


#Алясинг
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[1829 1984]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[2316 2397]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[3380 3399]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[4098 4159]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[4356 4554]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[9326 9403]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[14183 14251]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[14945 14992]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[15625 15659]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[17140 17223]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[19428 19724]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[19893 19964]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[20445 20630]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[22506 22577]")


#Маски на опенинг
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-01.png'), "[2403 2481]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-02.png'), "[2482 2562]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-03.png'), "[3011 3084]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-04.png'), "[3085 3173]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-05.png'), "[3174 3272]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-06.png'), "[3273 3336]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-07.png'), "[3337 3422]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-08.png'), "[3423 3543]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-09.png'), "[3677 3827]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-10.png'), "[3996 4097]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-11.png'), "[4098 4159]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.png'), "[4160 4236]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-13.png'), "[4237 4355]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-14.png'), "[4419 4515]")


#Маски на эндинг
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-01.png'), "[28797 29764]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-02.png'), "[29765 30365]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-01.png'), "[30366 30952]")


clip16 = core.fmtc.bitdepth(mg, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1.2, tbsize=3, opt=3)
fd = fd.fine_dehalo(pf, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4)
db = core.neo_f3kdb.Deband(fd, range=25, y=20, cb=10, cr=10, grainy=80, grainc=40, output_depth=16, dynamic_grain=True, keep_tv_range=True, blur_first=True)


db.fmtc.bitdepth(bits=10).set_output()
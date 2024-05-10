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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Ep 10.m2ts')


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


mg = iti.std.Trim(0, 32200)+ed.std.Trim(32201, 34478)+episode.std.Trim(34479, 34550)+iti.std.Trim(34551, 35052)


#Алясинг
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[127 290]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[2876 2895]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[3594 3655]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[3852 4052]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[10256 10327]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[13678 13809]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[15028 15212]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[18463 18534]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[20566 20709]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[21059 21141]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[21205 21321]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[23084 23239]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[25567 25631]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[25679 25744]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[26030 26057]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[26322 26392]")


#Маски на опенинг
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-01.png'), "[1899 1977]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-02.png'), "[1978 2058]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-03.png'), "[2507 2580]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-04.png'), "[2581 2669]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-05.png'), "[2670 2768]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-06.png'), "[2769 2832]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-07.png'), "[2833 2918]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-08.png'), "[2919 3039]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-09.png'), "[3173 3323]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-10.png'), "[3492 3593]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-11.png'), "[3594 3655]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-12.png'), "[3656 3732]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-13.png'), "[3733 3851]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\OP-14.png'), "[3915 4011]")


#Маски на эндинг
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-01.png'), "[32201 33290]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-02.png'), "[33291 33891]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 2\BDMV\STREAM\Скрипты\Маски\ED-01.png'), "[33892 34478]")


clip16 = core.fmtc.bitdepth(mg, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1.2, tbsize=3, opt=3)
fd = fd.fine_dehalo(pf, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4)
db = core.neo_f3kdb.Deband(fd, range=25, y=20, cb=10, cr=10, grainy=80, grainc=40, output_depth=16, dynamic_grain=True, keep_tv_range=True, blur_first=True)


db.fmtc.bitdepth(bits=10).set_output()
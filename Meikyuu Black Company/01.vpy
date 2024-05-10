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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Meikyuu Black Company\Episode 01.m2ts')
    

def insuin(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.5, kernel='bicubic', descale_height=810, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.3, brightstr=0.4, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv


iti = insuin(episode)


mg = iti.std.Trim(0, 3128)+episode.std.Trim(3129, 3260)+iti.std.Trim(3261, 31888)+episode.std.Trim(31889, 34071)


mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[450 629]")


#Маски
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-01.png'), "[12 138]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-02.png'), "[206 318]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-03.png'), "[454 561]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-04.png'), "[711 829]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-05.png'), "[837 955]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-06.png'), "[963 1067]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-07.png'), "[1304 1404]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-08.png'), "[1566 1665]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-09.png'), "[1729 1848]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-10.png'), "[1894 2021]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-11.png'), "[2285 2393]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-12.png'), "[2401 2500]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-13.png'), "[2508 2607]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-14.png'), "[2687 2805]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-15.png'), "[2949 3030]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 01-16.png'), "[3265 3384]")


clip16 = core.fmtc.bitdepth(mg, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1.5, tbsize=3, opt=3)
fd = fd.fine_dehalo(pf, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4)
db = core.neo_f3kdb.Deband(fd, range=30, y=30, cb=20, cr=20, grainy=70, grainc=40, output_depth=16, dynamic_grain=True, keep_tv_range=True, blur_first=True)
den = cooldegrain.CoolDegrain(db, tr=1, thsad=16, thsadc=10, bits=16, blksize=8, overlap=4, pf=db)


den.fmtc.bitdepth(bits=10).set_output()
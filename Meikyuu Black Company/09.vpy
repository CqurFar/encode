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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Meikyuu Black Company\Episode 09.m2ts')


#Склейка ED
ed_titles = core.std.Trim(episode, 31890, 34047)
nced = core.lsmas.LWLibavSource(source=r'E:\Работа\Meikyuu Black Company\NCED 02.m2ts').std.Trim(24, 2181)
nced_aa = core.raws.Source(r'E:\Работа\Meikyuu Black Company\NCED 02.y4m').std.Trim(24, 2181)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)


def insuin(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.5, kernel='bicubic', descale_height=810, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.3, brightstr=0.4, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv


iti = insuin(episode)


mg = iti.std.Trim(0, 526)+episode.std.Trim(527, 1056)+iti.std.Trim(1057, 31889)+ed+episode.std.Trim(34048, 34071)


mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[11280 11380]")


#Маски
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 09-01.png'), "[4 110]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 09-02.png'), "[118 223]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 09-03.png'), "[231 338]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 09-04.png'), "[1141 1248]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 09-05.png'), "[1347 1462]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 09-06.png'), "[1548 1634]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 09-07.png'), "[1792 1911]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 09-08.png'), "[2036 2152]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 09-09.png'), "[2161 2247]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 09-10.png'), "[2327 2446]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 09-11.png'), "[2607 2685]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 09-12.png'), "[2690 2788]")


clip16 = core.fmtc.bitdepth(mg, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1.5, tbsize=3, opt=3)
fd = fd.fine_dehalo(pf, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4)
db = core.neo_f3kdb.Deband(fd, range=30, y=30, cb=20, cr=20, grainy=70, grainc=40, output_depth=16, dynamic_grain=True, keep_tv_range=True, blur_first=True)
den = cooldegrain.CoolDegrain(db, tr=1, thsad=16, thsadc=10, bits=16, blksize=8, overlap=4, pf=db)

 
den.fmtc.bitdepth(bits=10).set_output()
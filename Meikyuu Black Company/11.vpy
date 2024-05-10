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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Meikyuu Black Company\Episode 11.m2ts')


def insuin(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.5, kernel='bicubic', descale_height=810, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.3, brightstr=0.4, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv


iti = insuin(episode)


mg = iti.std.Trim(0, 16349)+episode.std.Trim(16350, 17069)+iti.std.Trim(17070, 32644)+episode.std.Trim(32645, 34071)


mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[8227 8363]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[12285 12482]")


#Маски
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-01.png'), "[12 128]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-02.png'), "[137 253]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-03.png'), "[262 366]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-04.png'), "[375 494]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-05.png'), "[758 850]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-06.png'), "[859 946]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-07.png'), "[959 1046]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-08.png'), "[1055 1135]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-09.png'), "[1144 1246]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-10.png'), "[1259 1362]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-11.png'), "[1493 1604]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-12.png'), "[1613 1699]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-13.png'), "[1712 1799]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-14.png'), "[1808 1883]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-15.png'), "[1892 1977]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-16.png'), "[2458 2552]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-17.png'), "[7918 7994]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-18.png'), "[14816 14881]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Meikyuu Black Company\Скрипты\Маски\EP 11-19.png'), "[21053 21631]")


clip16 = core.fmtc.bitdepth(mg, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1.5, tbsize=3, opt=3)
fd = fd.fine_dehalo(pf, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4)
db = core.neo_f3kdb.Deband(fd, range=30, y=30, cb=20, cr=20, grainy=70, grainc=40, output_depth=16, dynamic_grain=True, keep_tv_range=True, blur_first=True)
den = cooldegrain.CoolDegrain(db, tr=1, thsad=16, thsadc=10, bits=16, blksize=8, overlap=4, pf=db)

 
den.fmtc.bitdepth(bits=10).set_output()
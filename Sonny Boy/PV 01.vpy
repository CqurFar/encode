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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Sonny Boy\2\00006.m2ts')

    
def hard(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=1070, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.3, brightstr=0.2, showmask=0, thmi=50, thma=95, rx=2, ry=2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(episode, 1, GRAY)
    v = core.std.ShufflePlanes(episode, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], episode.format.color_family)
    return mixyuv
    

pipi = hard(episode)


mg = episode.std.Trim(0, 23)+pipi.std.Trim(24, 174)+episode.std.Trim(175, 186)+pipi.std.Trim(187, 310)+episode.std.Trim(311, 327)+pipi.std.Trim(328, 370)+episode.std.Trim(371, 388)+pipi.std.Trim(389, 434)+episode.std.Trim(435, 452)+pipi.std.Trim(453, 481)+episode.std.Trim(482, 496)+pipi.std.Trim(497, 541)+episode.std.Trim(542, 556)+pipi.std.Trim(557, 590)+episode.std.Trim(591, 619)+pipi.std.Trim(620, 853)+episode.std.Trim(854, 907)


mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Sonny Boy\Скрипты\Маски\PV01-01.png'), "[187 248]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Sonny Boy\Скрипты\Маски\PV01-02.png'), "[683 742]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Sonny Boy\Скрипты\Маски\PV01-03.png'), "[743 806]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Sonny Boy\Скрипты\Маски\PV01-04.png'), "[807 882]")


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0.2, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4)
db = core.neo_f3kdb.Deband(fd, range=25, y=20, cb=10, cr=10, grainy=20, grainc=20, output_depth=16, dynamic_grain=True, keep_tv_range=True, blur_first=False)


db.fmtc.bitdepth(bits=10).set_output()




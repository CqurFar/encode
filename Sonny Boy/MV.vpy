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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Sonny Boy\2\MV.m2ts')
episode = core.std.Crop(episode, top=140, bottom=140)

    
def hard(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=790, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.3, brightstr=0.2, showmask=0, thmi=50, thma=95, rx=2, ry=2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=800, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(episode, 1, GRAY)
    v = core.std.ShufflePlanes(episode, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], episode.format.color_family)
    return mixyuv
    

pipi = hard(episode)


mg = episode.std.Trim(0, 375)+pipi.std.Trim(376, 850)+episode.std.Trim(851, 913)+pipi.std.Trim(914, 1037)+episode.std.Trim(1038, 1067)+pipi.std.Trim(1068, 1252)+episode.std.Trim(1253, 1282)+pipi.std.Trim(1283, 1314)+episode.std.Trim(1315, 1328)+pipi.std.Trim(1329, 1363)+episode.std.Trim(1364, 1377)+pipi.std.Trim(1378, 1390)+episode.std.Trim(1391, 1468)+pipi.std.Trim(1469, 1485)+episode.std.Trim(1486, 1531)+pipi.std.Trim(1532, 1546)+episode.std.Trim(1547, 1561)+pipi.std.Trim(1562, 1577)+episode.std.Trim(1578, 1608)+pipi.std.Trim(1609, 1964)+episode.std.Trim(1965, 1994)+pipi.std.Trim(1995, 2397)+episode.std.Trim(2398, 2777)+pipi.std.Trim(2778, 2815)+episode.std.Trim(2816, 3218)+pipi.std.Trim(3219, 3250)+episode.std.Trim(3251, 3496)+pipi.std.Trim(3497, 3835)+episode.std.Trim(3836, 3867)+pipi.std.Trim(3868, 3937)+episode.std.Trim(3938, 4143)+pipi.std.Trim(4144, 4176)+episode.std.Trim(4177, 4206)+pipi.std.Trim(4207, 4453)+episode.std.Trim(4454, 4690)+pipi.std.Trim(4691, 4929)+episode.std.Trim(4930, 5386)


mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Sonny Boy\Скрипты\Маски\MV-01.png'), "[505 601]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Sonny Boy\Скрипты\Маски\MV-02.png'), "[1222 1282]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Sonny Boy\Скрипты\Маски\MV-03.png'), "[3899 3929]")


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0.2, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4)
db = core.neo_f3kdb.Deband(fd, range=25, y=20, cb=10, cr=10, grainy=20, grainc=20, output_depth=16, dynamic_grain=True, keep_tv_range=True, blur_first=False)


db.fmtc.bitdepth(bits=10).set_output()




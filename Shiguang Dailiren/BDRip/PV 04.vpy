from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import atomchtools as atf
import beatricetools as bea
import havsfunc as haf
import fvsfunc as fvf
import kagefunc as kgf
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
import lostfunc as lfc
import G41Fun
import rgvs
import xvs

core.num_threads = 24
core.max_cache_size = 30000


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Linck Click\PV\PV 04.m2ts')


def insuin(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.45, kernel='bicubic', descale_height=960, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.1, brightstr=0.4, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv

iti = insuin(episode)


mg = iti.std.Trim(0, 1159)+episode.std.Trim(1160, 1185)+iti.std.Trim(1186, 1256)+episode.std.Trim(1257, 1274)+iti.std.Trim(1275, 1351)+episode.std.Trim(1352, 1366)+iti.std.Trim(1367, 1447)+episode.std.Trim(1448, 1461)+iti.std.Trim(1462, 1543)+episode.std.Trim(1544, 1558)+iti.std.Trim(1559, 1638)+episode.std.Trim(1639, 1657)+iti.std.Trim(1658, 1734)+episode.std.Trim(1735, 1753)+iti.std.Trim(1754, 2245)+episode.std.Trim(2246, 2587)


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.5, ry=2.5)
pf = core.dfttest.DFTTest(fd, sigma=1, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=3, thsad=20, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.neo_f3kdb.Deband(den, range=30, y=30, cb=25, cr=25, blur_first=True, dynamic_grain=False, opt=3)
gr = core.grain.Add(db, var=0.3, uvar=0.3, seed=100, constant=False, opt=3)

mask = fvf.rfs(gr, atf.ApplyImageMask(gr, clip16, r'E:\Работа\Linck Click\Скрипты\Маски\PV02-01.png'), "[0 2443]")

mask.fmtc.bitdepth(bits=10).set_output()
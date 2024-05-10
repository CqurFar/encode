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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Linck Click\PV\PV 02.m2ts')


def insuin(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.45, kernel='bicubic', descale_height=960, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.1, brightstr=0.4, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv

iti = insuin(episode)


mg = episode.std.Trim(0, 57)+iti.std.Trim(58, 94)+episode.std.Trim(95, 128)+iti.std.Trim(129, 166)+episode.std.Trim(167, 200)+iti.std.Trim(201, 415)+episode.std.Trim(416, 450)+iti.std.Trim(451, 476)+episode.std.Trim(477, 507)+iti.std.Trim(508, 531)+episode.std.Trim(532, 563)+iti.std.Trim(564, 1263)+episode.std.Trim(1264, 1321)+iti.std.Trim(1322, 2208)+episode.std.Trim(2209, 2639)


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.5, ry=2.5)
pf = core.dfttest.DFTTest(fd, sigma=1, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=3, thsad=20, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.neo_f3kdb.Deband(den, range=30, y=30, cb=25, cr=25, blur_first=True, dynamic_grain=False, opt=3)
gr = core.grain.Add(db, var=0.3, uvar=0.3, seed=100, constant=False, opt=3)

mask = fvf.rfs(gr, atf.ApplyImageMask(gr, clip16, r'E:\Работа\Linck Click\Скрипты\Маски\PV02-01.png'), "[0 2639]")

mask.fmtc.bitdepth(bits=10).set_output()
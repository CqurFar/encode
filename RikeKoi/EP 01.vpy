from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import atomchtools as atf
import beatricetools as bea
import havsfunc as haf
import fvsfunc as fvf
import kagefunc as kgf
import mvsfunc as mvsf
import muvsfunc as muvs
import descale as dsc
import finesharp
import ccd
import MCDenoise 
import cooldegrain
import finedehalo as fd
import insaneAA
import xaa
import Vine
import vsTAAmbk as taa
import HardAA
import lostfunc as lfc
import G41Fun
import rgvs
import xvs


core.num_threads = 24
core.max_cache_size = 30000


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Rikei ga Koi ni Ochita no de Shoumei shitemita\EP 01.m2ts')
aa = HardAA.HardAA(episode, mask='simple', mthr=0.1)

#Склейка OP
op_titles = core.std.Trim(episode, 3981, 6137)
ncop = core.lsmas.LWLibavSource(source=r'E:\Работа\Rikei ga Koi ni Ochita no de Shoumei shitemita\NCOP.m2ts').std.Trim(0, 2156)
ncop_aa = core.raws.Source(r'E:\Работа\Rikei ga Koi ni Ochita no de Shoumei shitemita\NCOP.y4m').std.Trim(0, 2156)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)


#Склейка ED
ed_titles = core.std.Trim(episode, 31169, 33325)
nced = core.lsmas.LWLibavSource(source=r'E:\Работа\Rikei ga Koi ni Ochita no de Shoumei shitemita\NCED.m2ts').std.Trim(0, 2156)
nced_aa = core.raws.Source(r'E:\Работа\Rikei ga Koi ni Ochita no de Shoumei shitemita\NCED.y4m').std.Trim(0, 2156)
ed = atf.ApplyCredits(ed_titles, nced, nced_aa)


def hard(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.8, kernel='Spline36', descale_height=720) 
    graydh = fd.fine_dehalo(desc, darkstr=0.1, brightstr=0.4, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2)
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


mg = aa.std.Trim(0, 3518)+pipi.std.Trim(3519, 3703)+aa.std.Trim(3704, 3778)+pipi.std.Trim(3779, 3872)+aa.std.Trim(3873, 3980)+op+aa.std.Trim(6138, 10812)+pipi.std.Trim(10813, 10956)+aa.std.Trim(10957, 17279)+pipi.std.Trim(17280, 17483)+aa.std.Trim(17484, 23201)+pipi.std.Trim(23202, 23375)+aa.std.Trim(23376, 24566)+pipi.std.Trim(24567, 24686)+aa.std.Trim(24687, 31168)+ed+aa.std.Trim(33326, 33721)+pipi.std.Trim(33722, 33925)+episode.std.Trim(33926, 34071)


#Маски
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\Rikei ga Koi ni Ochita no de Shoumei shitemita\Скрипты\Маски\EP01-01.png'), "[10929 10956]")


clip16 = core.fmtc.bitdepth(mg, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1.5, tbsize=3, opt=0)
dg = cooldegrain.CoolDegrain(pf, tr=3, thsad=100, thsadc=10, bits=16, blksize=8, overlap=4, pf=pf)
db = core.placebo.Deband(dg, threshold=0.8, radius=10)
sh = core.cas.CAS(db, sharpness=0.3, opt=0)
dh = G41Fun.MaskedDHA(sh, rx=2.4, ry=2.4, darkstr=0.2, brightstr=0.8, lowsens=50, highsens=50, maskpull=48, maskpush=192, ss=1, showmask=False)

dh.fmtc.bitdepth(bits=10).set_output()
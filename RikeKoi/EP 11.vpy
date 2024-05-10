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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Rikei ga Koi ni Ochita no de Shoumei shitemita\EP 11.m2ts')
aa = HardAA.HardAA(episode, mask='simple', mthr=0.1)


#Склейка OP
op_titles = core.std.Trim(episode, 0, 2156)
ncop = core.lsmas.LWLibavSource(source=r'E:\Работа\Rikei ga Koi ni Ochita no de Shoumei shitemita\NCOP.m2ts').std.Trim(0, 2156)
ncop_aa = core.raws.Source(r'E:\Работа\Rikei ga Koi ni Ochita no de Shoumei shitemita\NCOP.y4m').std.Trim(0, 2156)
op = atf.ApplyCredits(op_titles, ncop, ncop_aa)


#Склейка ED
ed_titles = core.std.Trim(episode, 31768, 33924)
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


mg = op+aa.std.Trim(2157, 3244)+pipi.std.Trim(3245, 3768)+aa.std.Trim(3769, 5679)+pipi.std.Trim(5680, 6087)+aa.std.Trim(6088, 6180)+pipi.std.Trim(6181, 6372)+aa.std.Trim(6373, 6549)+pipi.std.Trim(6550, 6726)+aa.std.Trim(6727, 7398)+pipi.std.Trim(7399, 7758)+aa.std.Trim(7759, 16623)+pipi.std.Trim(16624, 16716)+aa.std.Trim(16717, 16980)+pipi.std.Trim(16981, 17112)+aa.std.Trim(17113, 23036)+pipi.std.Trim(23037, 23126)+aa.std.Trim(23127, 26711)+pipi.std.Trim(26712, 26945)+aa.std.Trim(26946, 30842)+pipi.std.Trim(30843, 31070)+aa.std.Trim(31071, 31605)+pipi.std.Trim(31606, 31767)+ed+episode.std.Trim(33925, 34071)


clip16 = core.fmtc.bitdepth(mg, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1.5, tbsize=3, opt=0)
dg = cooldegrain.CoolDegrain(pf, tr=3, thsad=100, thsadc=10, bits=16, blksize=8, overlap=4, pf=pf)
db = core.placebo.Deband(dg, threshold=0.8, radius=10)
sh = core.cas.CAS(db, sharpness=0.3, opt=0)
dh = G41Fun.MaskedDHA(sh, rx=2.4, ry=2.4, darkstr=0.2, brightstr=0.8, lowsens=50, highsens=50, maskpull=48, maskpush=192, ss=1, showmask=False)

dh.fmtc.bitdepth(bits=10).set_output()
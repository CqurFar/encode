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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Linck Click\EP 05.m2ts')
episode = core.std.Crop(episode, top=140, bottom=140)


osup = episode.mv.Super(pel=2, sharp=2)
bv2 = osup.mv.Analyse(delta=2, overlap=4, isb=True)
bv1 = osup.mv.Analyse(delta=1, overlap=4, isb=True)
fv1 = osup.mv.Analyse(delta=1, overlap=4, isb=False)
fv2 = osup.mv.Analyse(delta=2, overlap=4, isb=False)
all = core.mv.Degrain2(episode, super=osup, mvbw=bv1, mvfw=fv1, mvbw2=bv2, mvfw2=fv2, thsad=200)


def hard420(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.5, kernel='bicubic', descale_height=420) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=800, nsize=6)  
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
    desc = insaneAA.revert_upscale(gray, descale_strength=0.45, kernel='bicubic', descale_height=680, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.1, brightstr=0.4, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=800, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv

iti = insuin(episode)

titi = hard420(episode)


mg = iti.std.Trim(0, 3909)+all.std.Trim(3910, 5572)+iti.std.Trim(5573, 23208)+titi.std.Trim(23209, 23311)+iti.std.Trim(23312, 34500)+episode.std.Trim(34501, 36326)

mg = fvf.rfs(mg, HardAA.HardAA(episode, mask='simple', mthr=0.1), "[5164 5178]")
mg = fvf.rfs(mg, HardAA.HardAA(episode, mask='simple', mthr=0.1), "[3418 3477]")
mg = fvf.rfs(mg, HardAA.HardAA(episode, mask='simple', mthr=0.1), "[12994 13068]")
mg = fvf.rfs(mg, HardAA.HardAA(episode, mask='simple', mthr=0.1), "[13776 13859]")


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd1 = fd.fine_dehalo(clip16, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4)
pf = core.dfttest.DFTTest(fd1, sigma=1, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=3, thsad=20, thsadc=14, bits=16, blksize=8, overlap=4, pf=pf)
db = core.neo_f3kdb.Deband(den, y=40, cb=35, cr=35, blur_first=True, dynamic_grain=False, opt=3)
sh = core.cas.CAS(db, sharpness=0.15, opt=0)
fd2 = fd.fine_dehalo(sh, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4)
gr = core.grain.Add(fd2, var=0.4, uvar=0.4, seed=120, constant=False, opt=3)

gr.fmtc.bitdepth(bits=10).set_output()
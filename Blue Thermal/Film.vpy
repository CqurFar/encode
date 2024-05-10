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
import dhh


core.num_threads = 24
core.max_cache_size = 30000


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Blue Thermal\Film.m2ts')


def insuin(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.3, kernel='lanczos', descale_height=810, bicubic_b=0.33, bicubic_c=0.33) 
    rescale = insaneAA.rescale(desc, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv 

iti = insuin(episode)


mg = episode.std.Trim(0, 576)+iti.std.Trim(577, 143231)+episode.std.Trim(143232, 149303)

mg = fvf.rfs(mg, HardAA.HardAA(episode, mask='simple', mthr=0.1), "[105799 105906]")
mg = fvf.rfs(mg, HardAA.HardAA(episode, mask='simple', mthr=0.1), "[140483 140590]")

clip16 = core.fmtc.bitdepth(mg, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=0.5, tbsize=3, opt=0)
db = core.placebo.Deband(pf, threshold=2.5, radius=10, dither = True, grain = 7)

fd1 = fd.fine_dehalo(db, None, 2.2, 2.2, 0, 0.5)
fd2 = fd.fine_dehalo(fd1, None, 2.2, 2.2, 0, 0.5)
dha1 = G41Fun.MaskedDHA(fd2, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)
dha2 = G41Fun.MaskedDHA(dha1, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)

Mask = atf.Tp7DebandMask(db, thr = 2.5, scale = 1, rg = True)
Invert = core.std.Invert(Mask, planes=[0])
Filtered = core.std.MaskedMerge(dha2, db, Invert, planes=[0], first_plane=True)
Filtered.fmtc.bitdepth(bits=10).set_output()
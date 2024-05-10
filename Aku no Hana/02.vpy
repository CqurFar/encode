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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Aku no Hana\EP 02.m2ts')


def insuin(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.6, kernel='Spline36', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.1, brightstr=0.4, showmask=0, thmi=50, thma=95, rx=2.2, ry=2.2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv

iti = insuin(episode)


mg = iti.std.Trim(0, 4197)+episode.std.Trim(4198, 5520)+iti.std.Trim(5521, 5782)+episode.std.Trim(5783, 6352)+iti.std.Trim(6353, 31389)+episode.std.Trim(31390, 33564)+iti.std.Trim(33565, 34087)


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0.2, brightstr=0.8, showmask=0, thmi=80, thma=120, thlimi=50, thlima=100, rx=2.5, ry=2.5, excl=True)
db = core.placebo.Deband(fd, threshold=0.8, radius=10)
gr = core.grain.Add(db, var=0.1, uvar=0.1, seed=100, constant=False, opt=3)

gr.fmtc.bitdepth(bits=10).set_output()
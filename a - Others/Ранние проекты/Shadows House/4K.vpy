from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import atomchtools as atf
import beatricetools as bea
import havsfunc as haf
import fvsfunc as fvf
import kagefunc as kg
import mvsfunc as mvf
import muvsfunc as muf
import descale as dsc
import ccd
import MCDenoise 
import cooldegrain
import finedehalo as fd
import insaneAA
import xaa
import vsTAAmbk as taa
import HardAA




episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Shadows House\Vol 04\BDMV\STREAM\00005.m2ts')
episode = core.resize.Bicubic(episode, width=3840, height=2160)

    
def hard(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=873, bicubic_b=0.33, bicubic_c=0.33)
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.9, showmask=0, thmi=50, thma=95, rx=2.6, ry=2.6)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=3840, dy=2160, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(episode, 1, GRAY)
    v = core.std.ShufflePlanes(episode, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1, useCL=True)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1, useCL=True)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1, useCL=True)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], episode.format.color_family)
    return mixyuv 


pipi = hard(episode)


mg = pipi


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=3.4, ry=3.4, useMtEdge=True)
pf = core.dfttest.DFTTest(fd, sigma=3, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(fd, tr=1, thsad=70, thsadc=70, bits=16, blksize=8, overlap=4, pf=pf)
db = core.neo_f3kdb.Deband(den, y=40, cb=40, cr=40, grainy=100, grainc=100, seed=100, output_depth=16, keep_tv_range=True, blur_first=True,  dynamic_grain=True)



db.fmtc.bitdepth(bits=10).set_output()




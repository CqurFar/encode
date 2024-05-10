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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\As the moon, so beautiful\Disc 1\BDMV\STREAM\Ep 03.m2ts')


def hard360(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.6, kernel='bicubic', descale_height=360, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.3, brightstr=0.2, showmask=0, thmi=50, thma=95, rx=2, ry=2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(episode, 1, GRAY)
    v = core.std.ShufflePlanes(episode, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1, useCL=True)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1, useCL=True)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1, useCL=True)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], episode.format.color_family)
    return mixyuv
    
    
def hard720(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.8, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.3, brightstr=0.2, showmask=0, thmi=50, thma=95, rx=2, ry=2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
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
    desc = insaneAA.revert_upscale(gray, descale_strength=0.4, kernel='bicubic', descale_height=720, bicubic_b=0.33, bicubic_c=0.33) 
    graydh = fd.fine_dehalo(desc, darkstr=0.3, brightstr=0.2, showmask=0, thmi=50, thma=95, rx=2, ry=2)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1920, dy=1080, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv

    
titi = hard360(episode)

ed = hard720(episode)

iti = insuin(episode)


mg = iti.std.Trim(0, 18547)+titi.std.Trim(18548, 18637)+iti.std.Trim(18638, 32752)+episode.std.Trim(32753, 32872)+ed.std.Trim(32873, 35052)


#Алясинг
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[7286 7381]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[7862 7939]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[8036 8587]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[8792 8987]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[9036 9105]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[9154 9222]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[9398 9607]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[9680 9733]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[10222 10383]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[12682 13143]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[17171 17242]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[17645 17698]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[17897 17956]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[18041 18282]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[18548 18637]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[20609 21040]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[26276 26311]")
mg = fvf.rfs(mg, HardAA.HardAA(mg, mask='simple', mthr=0.1), "[26499 26575]")


#Маски на эндинг
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 1\BDMV\STREAM\Скрипты\Маски\ED-01.png'), "[32873 33841]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 1\BDMV\STREAM\Скрипты\Маски\ED-02.png'), "[33842 34520]")
mg = fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\As the moon, so beautiful\Disc 1\BDMV\STREAM\Скрипты\Маски\ED-01.png'), "[34521 35052]")


clip16 = core.fmtc.bitdepth(mg, bits=16)
pf = core.dfttest.DFTTest(clip16, sigma=1.2, tbsize=3, opt=3)
fd = fd.fine_dehalo(pf, darkstr=0.1, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4)
db = core.neo_f3kdb.Deband(fd, range=25, y=20, cb=10, cr=10, grainy=80, grainc=40, output_depth=16, dynamic_grain=True, keep_tv_range=True, blur_first=True)


db.fmtc.bitdepth(bits=10).set_output()
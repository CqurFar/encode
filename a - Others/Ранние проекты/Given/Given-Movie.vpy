import vapoursynth as vs
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
import cooldegrain as cold
import finedehalo as fd
import insaneAA
core = vs.get_core()
episode=core.ffms2.Source(source=r'E:\Работа\映画 ギヴン\BDROM\BDMV\STREAM\00001.m2ts')
episode=core.resize.Spline64(episode, format=vs.YUV420P10, matrix_in_s='709')
#episode=haf.ChangeFPS(episode, fpsnum=24000, fpsden=1001)
episode=muf.SmoothGrad(episode, radius=4, elast=4, ref=episode)
#episode=core.neo_f3kdb.Deband(episode, range=31, y=24, cb=10, cr=10, grainy=40, grainc=40, output_depth=16, keep_tv_range=True, dynamic_grain=True)
episode=core.neo_f3kdb.Deband(episode, y=40, cb=40, cr=40, grainy=40, grainc=40,dynamic_grain=False, blur_first=True)

def inn(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.2, kernel='bilinear', descale_height=720) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.3, showmask=0, thmi=500, thma=95, rx=5.4, ry=5.4, useMtEdge=True)    
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=2, dx=1920, dy=1080, nsize=6) 
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    mixyuv = core.std.ShufflePlanes([aa, episode, episode], [0,1,2], episode.format.color_family)
    return mixyuv
     
    
iti=inn(episode)

mg=iti.std.Trim(0, 76780)+episode.std.Trim(76781, 83645)+iti.std.Trim(83646, 85170)+episode.std.Trim(85171, 85287)
#mg=fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\映画 ギヴン\BDROM\BDMV\STREAM\Маски\03.png'), "[222 296]")
#mg=fvf.rfs(mg, atf.ApplyImageMask(mg, episode, r'E:\Работа\映画 ギヴン\BDROM\BDMV\STREAM\Маски\04.png'), "[565 623]")
clip16=core.fmtc.bitdepth(mg, bits=16)
clip16.fmtc.bitdepth(bits=10).set_output()

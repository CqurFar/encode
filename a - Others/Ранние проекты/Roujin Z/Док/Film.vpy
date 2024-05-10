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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Roujin Z\BDMV\STREAM\00010.m2ts')

def rotate_clockwise(clip: VideoNode) -> VideoNode:
    return clip.std.Transpose().std.FlipHorizontal()

def rotate_counterclockwise(clip: VideoNode) -> VideoNode:
    return clip.std.Transpose().std.FlipVertical()

def lumaAA(episode, pscrn=1, dev=-1):
    ux = episode.width * 4
    uy = episode.height * 4
    luma = core.std.ShufflePlanes(episode, 0, GRAY)
    graydh = fd.fine_dehalo(luma, darkstr=0, brightstr=1, showmask=0, rx=1.5, ry=1.5, useMtEdge=True)
    upscale = core.nnedi3cl.NNEDI3CL(graydh, field=1, dh=True, dw=True, nsize=6, nns=4, pscrn=pscrn, device=dev)
    upscale = fd.fine_dehalo(upscale, darkstr=0, brightstr=1, showmask=0, rx=2, ry=2, useMtEdge=True)
    rotated = rotate_clockwise(upscale)
    interpolated = rotated.eedi3m.EEDI3CL(field=1, dh=True, alpha=0.4,beta=0.25,gamma=20.0,nrad=2,mdis=20, hp=False,ucubic=True,cost3=True,vcheck=2,vthresh0=32,vthresh1=64,vthresh2=4, sclip=rotated.nnedi3.nnedi3(field=1, dh=True,    
    nsize=0, nns=4, pscrn=1, qual=2), device=dev)
    interpolated = rotate_counterclockwise(interpolated)
    interpolated = interpolated.eedi3m.EEDI3CL(field=1, dh=True, alpha=0.4,beta=0.25,gamma=20.0,nrad=2,mdis=20, hp=False,ucubic=True,cost3=True,vcheck=2,vthresh0=32,vthresh1=64,vthresh2=4, sclip=interpolated.nnedi3.nnedi3(field=1, 
    dh=True, nsize=0, nns=4, pscrn=1, qual=2), device=dev)
    graydh2 = fd.fine_dehalo(interpolated, darkstr=0, brightstr=1, showmask=0, rx=2.3, ry=2.3, useMtEdge=True)
    downscale = core.resize.Spline36(graydh2, episode.width, episode.height, src_left=-1.5, src_top=-1.5, src_width=ux, src_height=uy, filter_param_a=0.33, filter_param_b=0.33)
    downscale = core.std.ShufflePlanes([downscale,episode], [0,1,2], YUV) 
    downscale = finesharp.sharpen(downscale, mode=-3, sstr=0.1)
    mixyuv = fd.fine_dehalo(downscale, darkstr=0, brightstr=0.7, showmask=0, rx=2, ry=2, useMtEdge=True)
    return  mixyuv 
    
    
lulu = lumaAA(episode)
 

mg = episode


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
pf = core.dfttest.DFTTest(fd, sigma=2, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=30, cb=30, cr=30, grainy=20, grainc=20, output_depth=16, keep_tv_range=True, blur_first=False, dynamic_grain=True)


db.fmtc.bitdepth(bits=10).set_output()
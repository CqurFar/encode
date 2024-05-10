from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS, FLOAT
from vsutil import get_y
from vsutil import get_w
from vsgan import ESRGAN
from mvsfunc import ToYUV, ToRGB
from havsfunc import FastLineDarkenMOD
from vsaa import based_aa, upscaled_sraa, Nnedi3, Eedi3, SangNom
from vsrgtools import rgtools
from vstools import join, depth
import vapoursynth as vs
import atomchtools as atf
import beatricetools
import havsfunc as haf
import fvsfunc as fvf
import kagefunc
import mvsfunc as mvs
import muvsfunc as mvf
import descale as dsc
import finesharp
import ccd
import MCDenoise 
import cooldegrain
import finedehalo as fd
import insaneAA
import xaa
import vsTAAmbk
import HardAA
import lostfunc
import G41Fun
import lvsfunc
import limit_v2
import vsdehalo
import vsmlrt
import vsdenoise
import vsmask
import vsgan
import vskernels
import dhh


#Техническое
core.num_threads = 24
core.max_cache_size = 30000

import os
os.environ['CUDA_MODULE_LOADING'] = 'LAZY'
os.environ['CUDA_FORCE_PRELOAD_LIBRARIES'] = '1'
os.environ['CUDA_AUTO_BOOST'] = '1'
os.environ['CUDA_DEVICE_MAX_CONNECTIONS'] = '32'
os.environ['CUDA_CACHE_MAXSIZE'] = '12884901888'


#Сорц FR
episode_fr = core.lsmas.LWLibavSource(source=r'E:\Работа\Golgo 13 The Professional\Film FR.m2ts').std.Trim(19, 134588)


#aа на древное cgi
def sangnom_AA(clip: vs.VideoNode) -> vs.VideoNode:
    clip_y = get_y(clip)
    line_mask = vsmask.edge.Tritical().edgemask(clip_y, multi=7).std.Maximum().std.Limiter().std.BoxBlur(1, 1, 1)
    descale = vskernels.Lanczos.descale(clip_y, width=get_w(720), height=720)
    rescale = upscaled_sraa(descale, ssfunc=Nnedi3(opencl=False), aafunc=SangNom(), width=1920, height=1080, rfactor=2)
    aa = based_aa(rescale, supersampler=False)
    rescaled = core.std.MaskedMerge(clip_y, aa, line_mask)
    rescaled = join(rescaled, clip)
    return rescaled

aa = sangnom_AA(episode_fr)
episode_fr = episode_fr.std.Trim(0, 3673)+aa.std.Trim(3674, 4184)+episode_fr.std.Trim(4185, 6917)+aa.std.Trim(6918, 7112)+episode_fr.std.Trim(7113, 111744)+aa.std.Trim(111745, 112173)+episode_fr.std.Trim(112174, 112357)+aa.std.Trim(112358, 112778)+episode_fr.std.Trim(112779, 112801)+aa.std.Trim(112802, 113000)+episode_fr.std.Trim(113001, 113047)+aa.std.Trim(113048, 113143)+episode_fr.std.Trim(113144, 113187)+aa.std.Trim(113188, 113259)+episode_fr.std.Trim(113260, 113318)+aa.std.Trim(113319, 113474)+episode_fr.std.Trim(113475, 134569)  


#Сорц US тайминг под FR
episode_us = core.lsmas.LWLibavSource(source=r'E:\Работа\Golgo 13 The Professional\Film US.m2ts')
episode_us = episode_us.std.Trim(223, 134763)
episode_us = episode_us.std.Trim(0,  7339)+episode_us.std.Trim(7341,  134540)
episode_us = episode_us.std.Trim(0,  55917)+episode_us.std.Trim(55906,  55917)+episode_us.std.Trim(55918,  134539)
episode_us = episode_us.std.Trim(0,  56090)+episode_us.std.Trim(56090,  134551)
episode_us = episode_us.std.Trim(0,  84652)+episode_us.std.Trim(84651,  84652)+episode_us.std.Trim(84653,  134552)
episode_us = episode_us.std.Trim(0,  107547)+episode_us.std.Trim(107549,  134554)
episode_us = episode_us.std.Trim(0,  121193)+episode_us.std.Trim(121195,  134553)
episode_us_fin = episode_us.std.Trim(0,  134552)+episode_us.std.Trim(134537,  134552)+episode_us.std.Trim(134552,  134552)


#Красный инт
red_us = episode_us_fin.std.Trim(14941, 14941)
rgb_in = ToRGB(red_us, matrix=1, depth=32)
cube = core.timecube.Cube(rgb_in, cube=r'E:\Работа\Golgo 13 The Professional\Скрипты\Cube\red.cube')
yuv_out = ToYUV(cube, matrix=1, css='420', depth=8)

int = yuv_out+episode_us_fin.std.Trim(14942, 14989)


#Склейка + белые линии по краям
episode_black_in = core.lsmas.LWLibavSource(source=r'E:\Работа\Golgo 13 The Professional\Film FR.m2ts').std.Trim(0, 11)+core.lsmas.LWLibavSource(source=r'E:\Работа\Golgo 13 The Professional\Film US.m2ts').std.Trim(0, 6)
episode_black_out = episode_us_fin.std.Trim(134537, 134569)

episode_fin = episode_black_in+episode_us_fin.std.Trim(0, 119)+episode_fr.std.Trim(120, 14940)+int+episode_fr.std.Trim(14990, 40905)+episode_us_fin.std.Trim(40906, 40941)+episode_fr.std.Trim(40942, 72202)+episode_us_fin.std.Trim(72203, 72262)+episode_fr.std.Trim(72263, 99712)+episode_us_fin.std.Trim(99713, 99890)+episode_fr.std.Trim(99891, 100877)+episode_us_fin.std.Trim(100878, 101017)+episode_fr.std.Trim(101018, 134536)+episode_black_out

cr = core.std.Crop(episode_fin, top=22, bottom=22)
fix_edge = core.edgefixer.Continuity(cr, left=4, right=8, top=2, bottom=2).fmtc.bitdepth(bits=16)


#KillerSpots
def KillerSpots(clip: vs.VideoNode):
  osup = core.mv.Super(clip, pel=4, sharp=2, rfilter=2)
  bv1 = core.mv.Analyse(osup, isb=True, delta=1, overlap=2, blksize=4, search=5, chroma=True, truemotion=False, searchparam=16, pnew=50, dct=4)
  fv1 = core.mv.Analyse(osup, isb=False, delta=1, overlap=2, blksize=4, search=7, chroma=True, truemotion=False, searchparam=16, pnew=50, dct=4)
  
  bv1_re = core.mv.Recalculate(osup, bv1, overlap=2, blksize=4, search=5, chroma=True, truemotion=False)
  fv1_re = core.mv.Recalculate(osup, fv1, overlap=2, blksize=4, search=6, chroma=True, truemotion=False)
  
  bc1  = core.mv.Compensate(clip, osup, bv1_re)
  fc1  = core.mv.Compensate(clip, osup, fv1_re)
  
  
  clip = core.std.Interleave([fc1, clip, bc1])
  clip = rgtools.removegrain(clip, mode=5)
  clip = rgtools.clense(clip)
  clip = core.std.SelectEvery(clip=clip, cycle=3, offsets=1)
  return clip;
  
kls = KillerSpots(fix_edge)


#Фильтрация
pf = core.dfttest.DFTTest(kls, sigma=1, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=2, thsad=20, thsadc=50, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=20, cb=15, cr=15, grainy=0, grainc=0, blur_first=True)

mask_db = atf.Tp7DebandMask(db, thr=0.8, scale=0.5, rg=True).std.BoxBlur(1, 1, 1)
invert = core.std.Invert(mask_db, planes=[0])
masked_db = core.std.MaskedMerge(kls, db, invert, planes=[0], first_plane=True)

rgb_in = ToRGB(masked_db, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_in, model=1, strength=1, overlap=0, tilesize=[1920, 1032], backend=vsmlrt.Backend.TRT())
yuv_out = ToYUV(dpir, matrix=1, css='420', depth=16)


#Векторка
osup = yuv_out.mv.Super(pel=4, sharp=2, rfilter=2)
bv1 = osup.mv.Analyse(isb=True, delta=1, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
bv2 = osup.mv.Analyse(isb=True, delta=2, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
bv3 = osup.mv.Analyse(isb=True, delta=3, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
fv1 = osup.mv.Analyse(isb=False, delta=1, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
fv2 = osup.mv.Analyse(isb=False, delta=2, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
fv3 = osup.mv.Analyse(isb=False, delta=3, overlap=2, blksize=4, search=4, chroma=True, truemotion=False)
all = core.mv.Degrain3(yuv_out, super=osup, mvbw=bv1, mvfw=fv1, mvbw2=bv2, mvfw2=fv2, mvbw3=bv3, mvfw3=fv3, thsad=200, thsadc=150, plane=4)


#Нейронка + цвета
yuv_episode = ToYUV(all, depth=16)
clip_y = get_y(yuv_episode)
rgb_in = ToRGB(all, matrix=1, depth=32)
ai = core.trt.Model(rgb_in, use_cuda_graph=True, overlap=0, tilesize=[1920, 1032], engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_DBZScanLite_252k_new.engine').fmtc.bitdepth(bits=16)

sigmoidized = haf.SigmoidInverse(ai, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 1920, 1036) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
yuv_out = ToYUV(de_sigmoidized, matrix=1, css='420', depth=16)

ai_expr = core.std.Expr([all, yuv_out], 'x 0.60 * y 0.40 * +')
colorfix = atf.CopyColors(ai_expr, all)


#Зерно и вывод
deh = vsdehalo.fine_dehalo(colorfix, rx=2.2, ry=2.2, darkstr=0, brightstr=0.5, thmi=30, thma=100, ss=1, edgeproc=0.5)
gr = core.grain.Add(deh, var=1, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=123456789, constant=False, opt=0)


#Черный
rgb_in = ToRGB(gr, matrix=1, depth=32)
cube = core.timecube.Cube(rgb_in, cube=r'E:\Работа\Golgo 13 The Professional\Скрипты\Cube\black-05.cube')
yuv_out = ToYUV(cube, matrix=1, css='420', depth=10)

yuv_out.fmtc.bitdepth(bits=10).set_output()
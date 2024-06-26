from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsgan import ESRGAN
from mvsfunc import ToYUV
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
import limit
import vsdehalo
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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Yofukashi no Uta\Song 01.m2ts')

#Начальное дегало с маской
dehalo_alph1 = vsdehalo.fine_dehalo(episode,None,2.3,2.3,0,0.4,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph1,None,2.3,2.3,0,0.4,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph2,None,2.3,2.3,0,0.3,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph2,None,2.3,2.3,0,0.2,thmi=30,thma=100)
deh = G41Fun.MaskedDHA(dehalo_alph2, rx=2.3, ry=2.3, darkstr=0, brightstr=0.5)
deh = G41Fun.MaskedDHA(deh, rx=2.3, ry=2.3, darkstr=0, brightstr=0.4)
Mask_01 =  dhh.mask(deh, radius=1.2, thr=None, thr2=100, mode=1, smooth=False, dha=False) 
Filtered = core.std.MaskedMerge(episode, deh, Mask_01, planes=0)


#Нейронка и маска только на линии
rgbs = core.resize.Lanczos(Filtered, format=vs.RGBS, matrix_in='1')
yuv_episode = ToYUV(rgbs)
clip_y = get_y(yuv_episode)
ai = core.trt.Model(rgbs , engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\1x_GainRESV3_Passive.engine')
yuv_ai = ToYUV(ai)
line_mask = vsmask.edge.Prewitt().edgemask(clip_y, multi=2).std.Maximum().std.Limiter()
mask_ai = core.std.MaskedMerge(yuv_episode, yuv_ai, line_mask)


#Дегало с маской после нейронки
clip16 = core.resize.Lanczos(mask_ai, format=vs.YUV420P16, matrix_s="709")
fd1 = fd.fine_dehalo(clip16, None, 2.2, 2.2, 0, 0.5)
fd2 = fd.fine_dehalo(fd1, None, 2.2, 2.2, 0, 0.5)
dha1 = G41Fun.MaskedDHA(fd2, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)
dha2 = G41Fun.MaskedDHA(dha1, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)
Mask_02 =  dhh.mask(dha2, radius=0.5, thr=None, thr2=100, mode=1, smooth=False, dha=False) 
Filtered = core.std.MaskedMerge(clip16, dha2, Mask_02, planes=0)


#Остальная фильтрация
pf = core.dfttest.DFTTest(Filtered, sigma=1, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=3, thsad=40, thsadc=38, blksize=8, overlap=4, pf=pf)
db = core.neo_f3kdb.Deband(den, y=30, cb=20, cr=20, grainy=0, grainc=0, blur_first=True)
Mask_03 = atf.Tp7DebandMask(db, thr=4, scale=1, rg = True)
Invert = core.std.Invert(Mask_03, planes=[0])
Filtered = core.std.MaskedMerge(Filtered, db, Invert, planes=0)


#Зерно и вывод
gr = core.grain.Add(Filtered, var=0.3, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=123456789, constant=False, opt=0)
gr.fmtc.bitdepth(bits=10).set_output()
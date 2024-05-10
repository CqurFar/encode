from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsutil import get_w
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


#Сорц
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Koi Kaze\EP 01.mkv')


#Деинт
deint_01 = core.vivtc.VFM(episode, order=1, field=2, mode=1, cthresh=8, mi=80, blockx=16, blocky=16, scthresh=8)
deint_01 = core.vivtc.VDecimate(deint_01, cycle=5, dupthresh=1.1, scthresh=10, blockx=4, blocky=4, dryrun=0).fmtc.bitdepth(bits=32)
deint_01 = core.ftf.FixFades(deint_01, mode=0, threshold=0.002, color=[0.0, 0.0, 0.0]).fmtc.bitdepth(bits=8)

deint_02 = haf.QTGMC(episode, Preset='placebo',TFF=True)
deint_02 = haf.srestore(deint_02, frate=24/1.001, speed=-1, thresh=8)

deint_fin = deint_02.std.Trim(0,33806)


#Рескеил width=846, height=476
cr = core.std.Crop(deint_02, left=4, right=4, top=2)
linear = core.resize.Bicubic(cr, format=vs.RGBS, transfer_in_s="709", transfer_s="linear", matrix_in_s="709").fmtc.bitdepth(bits=16)
sigmoidized = haf.SigmoidInverse(linear, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Bicubic(sigmoidized, 960, 540) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
scaled_gamma = core.resize.Bicubic(de_sigmoidized, format=cr.format, transfer_s="709", transfer_in_s="linear", matrix_s="709")
clip32 = scaled_gamma.fmtc.bitdepth(bits=32)
dpir  = lvsfunc.dpir(clip32, strength=3, mode='denoise', cuda=True, matrix=1)


#Нейронка
rgbs = core.resize.Lanczos(dpir, format=vs.RGBS, matrix_in='1')
yuv_episode = ToYUV(rgbs)
clip_y = get_y(yuv_episode)
ai_01 = core.trt.Model(rgbs , engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\1x_HurrDeblur_SubCompact_nf24-nc8_244k_net_g.engine')
yuv_ai = ToYUV(ai_01)
line_mask = vsmask.edge.Sobel().edgemask(clip_y, multi=0.5).std.Maximum().std.Limiter()
mask_ai = core.std.MaskedMerge(yuv_episode, yuv_ai, line_mask)

rgbs = core.resize.Lanczos(mask_ai, format=vs.RGBS, matrix_in='1')
ai_01 = core.trt.Model(rgbs, use_cuda_graph=True, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_KemonoScale_v2_mod.engine')
ai_02 = core.timecube.Cube(ai_01, cube=r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\luts\2x_KemonoScale_v2-200.cube')


#Фильтрация
clip16 = core.resize.Lanczos(ai_02, format=vs.YUV420P16, matrix_s='709')
pf = core.dfttest.DFTTest(clip16, sigma=0.5, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=2, thsad=40, thsadc=38, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=20, cb=10, cr=10, grainy=0, grainc=0, blur_first=False)
sh = core.cas.CAS(db, sharpness=0.7, opt=0)
gr = core.grain.Add(sh, var=2.5, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=123456789, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
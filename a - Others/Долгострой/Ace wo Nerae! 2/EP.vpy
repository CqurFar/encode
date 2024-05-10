from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsgan import ESRGAN
from mvsfunc import ToYUV
from vstools import scale_8bit
from vsrgtools import box_blur
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


core.num_threads = 24
core.max_cache_size = 30000

import os
os.environ['CUDA_MODULE_LOADING'] = 'LAZY'
os.environ['CUDA_FORCE_PRELOAD_LIBRARIES'] = '1'
os.environ['CUDA_AUTO_BOOST'] = '1'
os.environ['CUDA_DEVICE_MAX_CONNECTIONS'] = '32'
os.environ['CUDA_CACHE_MAXSIZE'] = '12884901888'


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Ace wo Nerae! 2\EP 07.mkv')
episode = core.vivtc.VFM(episode, order=1, field=0)
episode = core.vivtc.VDecimate(episode)


fd1 = fd.fine_dehalo(episode, None, 2.2, 2.2, 0, 0.5)
fd2 = fd.fine_dehalo(fd1, None, 2.2, 2.2, 0, 0.5)
dha1 = G41Fun.MaskedDHA(fd2, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)
dha2 = G41Fun.MaskedDHA(dha1, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)


cr = core.std.Crop(dha2, left=8, right=8).fmtc.bitdepth(bits=16)

pf = core.dfttest.DFTTest(cr, sigma=1, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=3, thsad=40, thsadc=38, blksize=8, overlap=4, pf=pf)
dpir  = lvsfunc.dpir(den, strength=2, mode='denoise', cuda=True, matrix=1)
db = core.neo_f3kdb.Deband(dpir, y=30, cb=20, cr=20, grainy=0, grainc=0, blur_first=False)
Mask = atf.retinex_edgemask(cr, sigma=0.1, draft=False, opencl=False)
Filtered = core.std.MaskedMerge(db, cr, Mask)


rgbs_01 = core.resize.Lanczos(Filtered, format=vs.RGBS, matrix_in='1')
ai_01 = core.trt.Model(rgbs_01, use_cuda_graph=True, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_KemonoScale_v2_mod.engine').resize.Lanczos(width=1440, height=1080)


rgbs = core.resize.Lanczos(ai_01, format=vs.RGBS, matrix_in='1')
yuv_episode = ToYUV(rgbs)
clip_y = get_y(yuv_episode)
ai = core.trt.Model(rgbs , engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\4x_OLDIES_290000_G_FINAL_interp_03_1440x1080.engine').resize.Lanczos(width=1440, height=1080)
ai = core.timecube.Cube(ai, cube=r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\luts\4x_OLDIES_290000_G_FINAL_interp_03_mod_02.cube')
yuv_ai = ToYUV(ai)
line_mask = vsmask.edge.Prewitt().edgemask(clip_y, multi=5).std.Maximum().std.Limiter()
mask_ai = core.std.MaskedMerge(yuv_episode, yuv_ai, line_mask)


clip16 = core.resize.Lanczos(mask_ai, format=vs.YUV420P16, width=1440, height=1080, matrix_s="709")
sh = core.cas.CAS(clip16, sharpness=0.25, opt=0)
gr = core.grain.Add(sh, var=3.5, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=123456789, constant=False, opt=0)


clip16.fmtc.bitdepth(bits=10).set_output()
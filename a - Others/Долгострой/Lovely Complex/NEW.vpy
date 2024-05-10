from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsutil import get_w
from vsgan import ESRGAN
from mvsfunc import ToYUV, ToRGB
from havsfunc import FastLineDarkenMOD
from vskernels import Catrom, Spline36
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


#Сорц
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Lovely Complex\EP 01.mkv')


#Деинт
vivtc = core.vivtc.VFM(episode, order=1, field=0)
VFM = core.tivtc.TDecimate(vivtc).fmtc.bitdepth(bits=32)
FixFade = core.ftf.FixFades(VFM, mode=0, threshold=0.002, color=[0.0, 0.0, 0.0]).fmtc.bitdepth(bits=8)
Vinver = haf.Vinverse2(FixFade)


#Рескеил 720x540
cr = core.std.Crop(Vinver, left=8, right=8)
linear = ToRGB(cr, matrix=1, depth=16)
sigmoidized = haf.SigmoidInverse(linear, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Lanczos(sigmoidized, 720, 540) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 


#Депир
rgb_in = ToRGB(de_sigmoidized, matrix=1, depth=32)
dpir = vsmlrt.DPIR(rgb_in, model=1, strength=2, overlap=0, tilesize=[720, 536], backend=vsmlrt.Backend.TRT())
yuv_out = ToYUV(dpir, matrix=1, css='420', depth=16)


#Фильтрация
line_d = FastLineDarkenMOD(yuv_out, strength=1, protection=7)
pf = core.dfttest.DFTTest(line_d, sigma=1.5, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=30, cb=20, cr=20, grainy=0, grainc=0, blur_first=True)


#Дегало
clip_y = get_y(db)
masky = vsmask.edge.DoG().edgemask(clip_y,0,multi=1).std.Inflate()
mask_out = vsmask.util.expand(masky,4,4)
mask = core.std.Expr([masky,mask_out],'y x -')
deh = vsdehalo.HQDeringmod(db,vsdenoise.Prefilter.MINBLUR2,mask,darkthr=40)
deh = vsdehalo.fine_dehalo(deh,None,2.2,2.2,0,0.5,thmi=10,thma=100)


yuv_episode = ToYUV(deh, depth=16)
clip_y = get_y(yuv_episode)
rgb_in = ToRGB(deh, matrix=1, depth=32)

ai = core.trt.Model(rgb_in, use_cuda_graph=True, overlap=0, tilesize=[720, 536], engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\1x_HurrDeblur_SubCompact_nf24-nc8_244k_net_g_new.engine')
yuv_out = ToYUV(ai, matrix=1, css='420', depth=16)
line_mask = vsmask.edge.Tritical().edgemask(clip_y, multi=5).std.Maximum().std.Limiter()
mask_ai = core.std.MaskedMerge(yuv_episode, yuv_out, line_mask)
ai_expr = core.std.Expr([yuv_episode, mask_ai], 'x 0.70 * y 0.30 * +')


rgb_in = ToRGB(ai_expr, matrix=1, depth=32)
ai = core.trt.Model(rgb_in, use_cuda_graph=True, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_KemonoScale_v2_new.engine')
ai = core.timecube.Cube(ai, cube=r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\luts\2x_KemonoScale_v2.cube')
ai = core.trt.Model(ai, use_cuda_graph=True, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2xIronLove_11729_g_new.engine')

linear = ToRGB(ai, matrix=1, depth=16)
sigmoidized = haf.SigmoidInverse(linear, thr=0.5, cont=6.5) 
scaled_sigmoid = Catrom.descale(sigmoidized, 720, 540) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
yuv_out = ToYUV(de_sigmoidized, matrix=1, css='420', depth=16)

yuv_out.fmtc.bitdepth(bits=10).set_output()
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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Lovely Complex\EP 01.mkv')


#Деинт
vivtc = core.vivtc.VFM(episode, order=1, field=0)
tivtc = core.tivtc.TFM(vivtc, order=-1, field=-1, mode=1, slow=2, mChroma=True)
TFM = core.tivtc.TDecimate(tivtc)


#Дегало
src_y = get_y(TFM)
masky = vsmask.edge.DoG().edgemask(src_y,0,multi=1).std.Inflate()
mask_out = vsmask.util.expand(masky,4,4)
mask = core.std.Expr([masky,mask_out],'y x -')
deh = vsdehalo.HQDeringmod(TFM,vsdenoise.Prefilter.MINBLUR2,mask,darkthr=40)
deh = vsdehalo.fine_dehalo(deh,None,2.2,2.2,0,0.5,thmi=10,thma=100)


#Рескеил
cr = core.std.Crop(deh, left=8, right=8)
linear = core.resize.Bicubic(cr, format=vs.RGBS, transfer_in_s="709", transfer_s="linear", matrix_in_s="709").fmtc.bitdepth(bits=16)
sigmoidized = haf.SigmoidInverse(linear, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Bicubic(sigmoidized, 720, 540) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
scaled_gamma = core.resize.Bicubic(de_sigmoidized, format=cr.format, transfer_s="709", transfer_in_s="linear", matrix_s="709")





#Нейронка
rgbs = core.resize.Lanczos(scaled_gamma, format=vs.RGBS, matrix_in='1')
ai_01 = core.trt.Model(rgbs, use_cuda_graph=True, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_KemonoScale_v2_mod.engine')
ai_02 = core.timecube.Cube(ai_01, cube=r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\luts\2x_KemonoScale_v2-200.cube')
ai_03 = core.trt.Model(rgbs, use_cuda_graph=True, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\4x_OLDIES_290000_G_FINAL_interp_03_mod.engine').resize.Lanczos(width=1440, height=1080)
ai_04 = core.timecube.Cube(ai_03, cube=r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\luts\Love Complex.cube')
ai_expr = core.std.Expr([ai_02, ai_04], 'x 0.80 * y 0.20 * +')


esrgan = ESRGAN(ai_expr, device="cuda")
vsgan.networks.esrgan.ESRGAN
esrgan.load(r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\2xIronLove_11729_g.pth')
vsgan.networks.esrgan.ESRGAN
esrgan.apply()
vsgan.networks.esrgan.ESRGAN
ai_05 = esrgan.clip


clip16 = core.resize.Lanczos(ai_05, format=vs.YUV420P16, matrix_s='709')
linear = core.resize.Bicubic(clip16, format=vs.RGBS, transfer_in_s="709", transfer_s="linear", matrix_in_s="709").fmtc.bitdepth(bits=16)
sigmoidized = haf.SigmoidInverse(linear, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Bicubic(sigmoidized, 1440, 1080) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
scaled_gamma = core.resize.Bicubic(de_sigmoidized, format=clip16.format, transfer_s="709", transfer_in_s="linear", matrix_s="709")
scaled_gamma.fmtc.bitdepth(bits=10).set_output()
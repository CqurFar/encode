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
ai_03 = core.trt.Model(rgbs, use_cuda_graph=True, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2xGT-v2-evA-01.engine')
ai_expr = core.std.Expr([ai_02, ai_03], 'x 0.70 * y 0.30 * +')

esrgan = ESRGAN(ai_02, device="cuda")
vsgan.networks.esrgan.ESRGAN
esrgan.load(r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\2xIronLove_11729_g.pth')
vsgan.networks.esrgan.ESRGAN
esrgan.apply()
vsgan.networks.esrgan.ESRGAN
ai_04 = esrgan.clip
dpir  = lvsfunc.dpir(ai_04, strength=2, mode='denoise', cuda=True, matrix=1)


#Рескеил
clip16 = core.resize.Lanczos(dpir, format=vs.YUV420P16, matrix_s='709')
linear = core.resize.Bicubic(clip16, format=vs.RGBS, transfer_in_s="709", transfer_s="linear", matrix_in_s="709").fmtc.bitdepth(bits=16)
sigmoidized = haf.SigmoidInverse(linear, thr=0.5, cont=6.5) 
scaled_sigmoid = core.resize.Bicubic(sigmoidized, 1440, 1080) 
de_sigmoidized = haf.SigmoidDirect(scaled_sigmoid, thr=0.5, cont=6.5) 
scaled_gamma = core.resize.Bicubic(de_sigmoidized, format=clip16.format, transfer_s="709", transfer_in_s="linear", matrix_s="709")


#Фильтрация
pf = core.dfttest.DFTTest(scaled_gamma, sigma=0.5, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=2, thsad=40, thsadc=38, blksize=4, overlap=2, pf=pf)
db = core.neo_f3kdb.Deband(den, y=20, cb=10, cr=10, grainy=0, grainc=0, blur_first=False)
aa = HardAA.HardAA(db, mask='simple', mthr=0.1)
gr = core.grain.Add(aa,  var=0.5, uvar=0.1, hcorr=0.1, vcorr=0.1, seed=123456789, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
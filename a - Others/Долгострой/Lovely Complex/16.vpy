from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsutil import get_y
from vsgan import ESRGAN
import vapoursynth as vs
import atomchtools
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


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Lovely Complex\EP 08.mkv')

vivtc = core.vivtc.VFM(episode, order=1, field=0)
tivtc = core.tivtc.TFM(vivtc, order=-1, field=-1, mode=1, slow=2, mChroma=True)

VFM = core.tivtc.TDecimate(vivtc)
TFM = core.tivtc.TDecimate(tivtc)


deint = TFM.std.Trim(0, 507)+VFM.std.Trim(508, 513)+TFM.std.Trim(514, 1930)+VFM.std.Trim(1931, 2002)+TFM.std.Trim(2003, 33711)


src_y = get_y(deint)
masky = vsmask.edge.DoG().edgemask(src_y,0,multi=1).std.Inflate()
mask_out = vsmask.util.expand(masky,4,4)
mask = core.std.Expr([masky,mask_out],'y x -')
deh = vsdehalo.HQDeringmod(deint,vsdenoise.Prefilter.MINBLUR2,mask,darkthr=40)
deh = vsdehalo.fine_dehalo(deh,None,2.2,2.2,0,0.5,thmi=10,thma=100)

cr = core.std.Crop(deh, left=8, right=8)
mg = cr.resize.Lanczos(width=720, height=540)

src_y = get_y(mg)
masky = vsmask.edge.DoG().edgemask(src_y,0,multi=1).std.Inflate()
mask_out = vsmask.util.expand(masky,4,4)
mask = core.std.Expr([masky,mask_out],'y x -')
deh = vsdehalo.HQDeringmod(mg,vsdenoise.Prefilter.MINBLUR2,mask,darkthr=40)
deh = vsdehalo.fine_dehalo(deh,None,2.4,2.4,0,0.7,thmi=10,thma=100)

pf = core.dfttest.DFTTest(deh, sigma=1, tbsize=3, opt=0)
db = core.placebo.Deband(pf, threshold=2, radius=12, dither = True, grain = 0)
rgbs = core.resize.Lanczos(db, format=vs.RGBS, matrix_in='1')


ai_01 = core.trt.Model(rgbs, use_cuda_graph=True, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\2x_KemonoScale_v2_mod.engine')
ai_02 = core.trt.Model(rgbs, use_cuda_graph=True, engine_path=r'C:\Users\Art\AppData\Roaming\.enhancr\models\engine\4x_OLDIES_290000_G_FINAL_interp_03_mod.engine').resize.Lanczos(width=1440, height=1080)
ai_02 = core.timecube.Cube(ai_02, cube=r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\luts\Love Complex.cube')
ai_expr = core.std.Expr([ai_01, ai_02], 'x 0.80 * y 0.20 * +')


clip16 = core.resize.Lanczos(ai_expr, format=vs.YUV420P16, matrix_s='709')
aa = HardAA.HardAA(clip16, mask='simple', mthr=0.1)
gr = core.grain.Add(aa,  var=1, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=123456789, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
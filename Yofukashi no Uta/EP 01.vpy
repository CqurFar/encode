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


#Техническое
core.num_threads = 24
core.max_cache_size = 30000

import os
os.environ['CUDA_MODULE_LOADING'] = 'LAZY'
os.environ['CUDA_FORCE_PRELOAD_LIBRARIES'] = '1'
os.environ['CUDA_AUTO_BOOST'] = '1'
os.environ['CUDA_DEVICE_MAX_CONNECTIONS'] = '32'
os.environ['CUDA_CACHE_MAXSIZE'] = '12884901888'


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Yofukashi no Uta\EP 01.m2ts')


#Склейка OP
op_titles = core.std.Trim(episode, 744, 2900)
ncop = core.lsmas.LWLibavSource(source=r'E:\Работа\Yofukashi no Uta\NCOP.m2ts').std.Trim(24, 2180).fmtc.bitdepth(bits=8)
ncop_fix = core.raws.Source(r'E:\Работа\Yofukashi no Uta\NCOP.y4m').std.Trim(24, 2180).fmtc.bitdepth(bits=8)
op = atf.ApplyCredits(op_titles, ncop, ncop_fix).resize.Lanczos(format=vs.YUV420P16)


#Склейка ED
ed_titles = core.std.Trim(episode, 30715, 32871)
nced = core.lsmas.LWLibavSource(source=r'E:\Работа\Yofukashi no Uta\NCED.m2ts').std.Trim(24, 2180).fmtc.bitdepth(bits=8)
nced_fix = core.raws.Source(r'E:\Работа\Yofukashi no Uta\NCED.y4m').std.Trim(24, 2180).fmtc.bitdepth(bits=8)
ed = atf.ApplyCredits(ed_titles, nced, nced_fix).resize.Lanczos(format=vs.YUV420P16)


#Начальное дегало с маской
dehalo_alph1 = vsdehalo.fine_dehalo(episode,None,2.3,2.3,0,0.4,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph1,None,2.3,2.3,0,0.4,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph2,None,2.3,2.3,0,0.3,thmi=30,thma=100)
dehalo_alph2 = vsdehalo.fine_dehalo(dehalo_alph2,None,2.3,2.3,0,0.2,thmi=30,thma=100)
deh = G41Fun.MaskedDHA(dehalo_alph2, rx=2.3, ry=2.3, darkstr=0, brightstr=0.5)
deh = G41Fun.MaskedDHA(deh, rx=2.3, ry=2.3, darkstr=0, brightstr=0.4)
Mask_01 =  dhh.mask(deh, radius=1.2, thr=None, thr2=100, mode=1, smooth=False, dha=False) 
Filtered = core.std.MaskedMerge(episode, deh, Mask_01, planes=0)
aa = HardAA.HardAA(Filtered, mask='simple', mthr=0.1)
aa = fvf.rfs(aa, atf.ApplyImageMask(aa, Filtered, r'E:\Работа\Yofukashi no Uta\Скрипты\Маски\EP-ab.png'), "[18341 18532]")


#Дегало с маской после нейронки
clip16 = core.resize.Lanczos(aa, format=vs.YUV420P16, matrix_in="1")
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
Mask = atf.retinex_edgemask(episode, sigma=0.1, draft=False, opencl=False)
Filtered = core.std.MaskedMerge(db, Filtered, Mask)


#ED
pf = core.dfttest.DFTTest(episode, sigma=1, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=3, thsad=40, thsadc=38, blksize=8, overlap=4, pf=pf)
db_ed = core.neo_f3kdb.Deband(den, y=30, cb=20, cr=20, grainy=0, grainc=0, blur_first=False)
gr_ed = core.grain.Add(db_ed, var=0.3, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=123456789, constant=False, opt=0).fmtc.bitdepth(bits=16)


#Next
pf = core.dfttest.DFTTest(episode, sigma=5, tbsize=3, opt=3)
den = cooldegrain.CoolDegrain(pf, tr=3, thsad=40, thsadc=38, blksize=8, overlap=4, pf=pf)
db_next = core.neo_f3kdb.Deband(den, y=100, cb=100, cr=100, grainy=0, grainc=0, blur_first=True).fmtc.bitdepth(bits=16)



#Зерно и вывод
sh = core.cas.CAS(Filtered, sharpness=0.4, opt=0)
gr = core.grain.Add(sh, var=0.4, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=123456789, constant=False, opt=0)


#Сценинг вывод
mg = gr.std.Trim(0, 743)+op+gr.std.Trim(2901, 29143)+gr_ed.std.Trim(29144, 32871)+gr.std.Trim(32872, 33494)+db_next.std.Trim(33495, 33639)
mg.fmtc.bitdepth(bits=10).set_output()
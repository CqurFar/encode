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
episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Horimiya\SE 01.mkv')


#Деинтерлейс
episode = haf.QTGMC(episode, Preset='placebo',TFF=True)
episode = haf.srestore(episode, frate=30/1.001, speed=-1, thresh=8)


#Нейронка
rgbs_in = core.resize.Lanczos(episode, format=vs.RGBS, matrix_in='1')
dpir  = lvsfunc.dpir(rgbs_in, strength=6, mode='denoise', cuda=True, matrix=1)


#Остальная фильтрация
clip16 = core.resize.Lanczos(dpir, format=vs.YUV420P16, matrix_s='709')
db = core.neo_f3kdb.Deband(clip16, y=40, cb=30, cr=30, grainy=0, grainc=0, blur_first=True)


#Зерно и вывод
sh = core.cas.CAS(db, sharpness=0.7, opt=0)
deh = vsdehalo.fine_dehalo(sh, ref=None, rx=2.5, ry=2.5, darkstr=0, brightstr=0.8, thmi=30, thma=100, excl=True, ss=1, edgeproc=0.5)
gr = core.grain.Add(deh, var=1.5, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=123456789, constant=False, opt=0)
gr.fmtc.bitdepth(bits=10).set_output()
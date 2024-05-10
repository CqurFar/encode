from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
from vsdpir import DPIR
import vapoursynth as vs
import vsgan
from vapoursynth import core
from vsgan import ESRGAN
import atomchtools
import beatricetools
import havsfunc as haf
import fvsfunc
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


core.num_threads = 24
core.max_cache_size = 30000


episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Ace wo Nerae! 2\EP 01.mkv')


episode = core.vivtc.VFM(episode, order=1, field=0)
episode = core.vivtc.VDecimate(episode)


fd1 = fd.fine_dehalo(episode, None, 2.2, 2.2, 0, 0.5)
fd2 = fd.fine_dehalo(fd1, None, 2.2, 2.2, 0, 0.5)
dha1 = G41Fun.MaskedDHA(fd2, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4)
dha2 = G41Fun.MaskedDHA(dha1, rx=2.2, ry=2.2, darkstr=0, brightstr=0.4).fmtc.bitdepth(bits=16)
db = core.neo_f3kdb.Deband(dha2, y=40, cb=40, cr=40, grainy=0, grainc=0, keep_tv_range=True, blur_first=True)


cr = core.std.Crop(db, left=8, right=8)
rgbs = core.resize.Spline16(cr, width=792, height=540, format=vs.RGBS, matrix_in='1')


esrgan = ESRGAN(rgbs, device="cuda")
vsgan.networks.esrgan.ESRGAN
esrgan.load(r'C:\Users\Art\Downloads\Progi\All\Encode\ai models\2X_DigitalFilmV5_Lite.PTH')
vsgan.networks.esrgan.ESRGAN
esrgan.apply()
vsgan.networks.esrgan.ESRGAN
rgbs = esrgan.clip


clip32 = rgbs.fmtc.bitdepth(bits=32)
dpir  = lvsfunc.dpir(clip32, strength=6, mode='denoise', cuda=True, matrix=1)


mg = dpir.std.Trim(0, 31703)+clip32.std.Trim(31704, 33863)+dpir.std.Trim(33864, 34606)


clip16 = core.resize.Spline16(mg, format=vs.YUV420P16, matrix_s="709")
aa = HardAA.HardAA(clip16, mask='simple', mthr=0.1)
sh = core.cas.CAS(aa, sharpness=0.7, opt=0)
gr = core.grain.Add(sh, var=4, uvar=0.0, hcorr=0.25, vcorr=0.25, seed=1234, constant=False, opt=0)

gr.fmtc.bitdepth(bits=10).set_output()
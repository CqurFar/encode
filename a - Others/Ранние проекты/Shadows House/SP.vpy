from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import atomchtools as atf
import beatricetools as bea
import havsfunc as haf
import fvsfunc as fvf
import kagefunc as kg
import mvsfunc as mvf
import muvsfunc as muf
import descale as dsc
import ccd
import MCDenoise 
import cooldegrain
import finedehalo as fd
import insaneAA
import xaa
import vsTAAmbk as taa
import HardAA




episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Shadows House\Vol 04\BDMV\STREAM\00006.m2ts')


mg = episode


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.8, ry=2.8, useMtEdge=True)
pf = core.dfttest.DFTTest(clip16, sigma=1, tbsize=3, opt=3, planes=[0,1,2])
den = cooldegrain.CoolDegrain(clip16, tr=1, thsad=24, thsadc=12, bits=16, blksize=8, overlap=4, pf=pf)
db = core.neo_f3kdb.Deband(den, y=25, cb=25, cr=25, grainy=40, grainc=40, output_depth=16,  dynamic_grain=False, keep_tv_range=True, blur_first=True)


db.fmtc.bitdepth(bits=10).set_output()




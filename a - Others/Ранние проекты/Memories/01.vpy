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




episode = core.lsmas.LWLibavSource(source=r'E:\Работа\Memories High Spec Edition\BDMV\STREAM\00001.m2ts')
episode = core.std.Crop(episode, left=78, right=78, top=54, bottom=54)


def hard480(episode):
    gray = core.std.ShufflePlanes(episode, 0, GRAY)
    desc = insaneAA.revert_upscale(gray, descale_strength=0.28, kernel='bicubic', descale_height=480) 
    graydh = fd.fine_dehalo(desc, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
    rescale = insaneAA.rescale(graydh, eedi3_mode=0, nnedi3_mode=1, dx=1764, dy=972, nsize=6)  
    aa = insaneAA.insaneAA(episode, external_aa=rescale, output_mode=0, input_mode=1)
    u = core.std.ShufflePlanes(episode, 1, GRAY)
    v = core.std.ShufflePlanes(episode, 2, GRAY)
    u = HardAA.HardAA(u, mask='simple', mthr=0.1)
    v = HardAA.HardAA(v, mask='simple', mthr=0.1)
    mixyuv = HardAA.HardAA(aa, mask='simple', mthr=0.1)
    mixyuv = core.std.ShufflePlanes([mixyuv, u, v], [0,0,0], episode.format.color_family)
    return mixyuv


tutu = hard480(episode)    

mg = episode.std.Trim(0, 3251)+tutu.std.Trim(3252, 3323)+episode.std.Trim(3324, 3742)+tutu.std.Trim(3743, 4032)+episode.std.Trim(4033, 11660)+tutu.std.Trim(11661, 11845)+episode.std.Trim(11846, 18370)+tutu.std.Trim(18371, 18448)+episode.std.Trim(18449, 21021)+tutu.std.Trim(21022, 21115)+episode.std.Trim(21116, 21186)+tutu.std.Trim(21187, 21540)+episode.std.Trim(21541, 22373)+tutu.std.Trim(22374, 22511)+episode.std.Trim(22512, 32352)+tutu.std.Trim(32353, 32594)+episode.std.Trim(32595, 32858)+tutu.std.Trim(32859, 33170)+episode.std.Trim(33171, 33517)+tutu.std.Trim(33518, 33859)+episode.std.Trim(33860, 34203)+tutu.std.Trim(34204, 34419)+episode.std.Trim(34420, 44597)+tutu.std.Trim(44598, 44749)+episode.std.Trim(44750, 46664)+tutu.std.Trim(46665, 46704)+episode.std.Trim(46705, 46822)+tutu.std.Trim(46823, 46956)+episode.std.Trim(46957, 47381)+tutu.std.Trim(47382, 47443)+episode.std.Trim(47444, 50442)+tutu.std.Trim(50443, 50543)+episode.std.Trim(50544, 54726)+tutu.std.Trim(54727, 54817)+episode.std.Trim(54818, 56238)+tutu.std.Trim(56239, 56369)+episode.std.Trim(56370, 56767)+tutu.std.Trim(56768, 56851)+episode.std.Trim(56852, 56982)+tutu.std.Trim(56983, 57126)+episode.std.Trim(57127, 57860)+tutu.std.Trim(57861, 57968)+episode.std.Trim(57969, 58028)+tutu.std.Trim(58029, 58304)+episode.std.Trim(58305, 58358)+tutu.std.Trim(58359, 58494)+episode.std.Trim(58495, 58863)+tutu.std.Trim(58864, 58931)+episode.std.Trim(58932, 59063)+tutu.std.Trim(59064, 59163)+episode.std.Trim(59164, 59469)+tutu.std.Trim(59470, 59714)+episode.std.Trim(59715, 59916)+tutu.std.Trim(59917, 60001)+episode.std.Trim(60002, 60087)+tutu.std.Trim(60088, 60653)+episode.std.Trim(60654, 60773)+tutu.std.Trim(60774, 61147)+episode.std.Trim(61148, 63803)


clip16 = core.fmtc.bitdepth(mg, bits=16)
fd = fd.fine_dehalo(clip16, darkstr=0, brightstr=0.7, showmask=0, thmi=50, thma=95, rx=2.4, ry=2.4, useMtEdge=True)
pf = core.dfttest.DFTTest(fd, sigma=1, tbsize=3, opt=3)
db = core.neo_f3kdb.Deband(pf, y=30, cb=30, cr=30, grainy=100, grainc=100, output_depth=16, keep_tv_range=True, blur_first=False)


db.fmtc.bitdepth(bits=10).set_output()
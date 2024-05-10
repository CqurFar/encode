from turtle import down
import jvsfunc
from vapoursynth import core, VideoNode, GRAY, YUV, GRAY8, GRAYS
import vapoursynth as vs
import havsfunc
import atomchtools as at
import cooldegrain as cd
import HardAAp2
from mixres_lvf import mixed_rescale
import vskernels
import vsdehalo
from vsdenoise import BM3DCudaRTC, nl_means, ccd, CCDMode, MVTools, PelType, SADMode, SearchMode, CCDPoints, MotionMode, mlm_degrain, MVToolsPresets, DeviceType
import dfttest2
import vsdeband
from havsfunc import FastLineDarkenMOD, bbmod
from mvsfunc import ToYUV,ToRGB
import vsmlrt
from vsrgtools import contrasharpening
from vsutil import get_y, depth, get_depth
import rekt
from vsmask.edge import Kroon
import vsscale
# replace frames with mask
def replace_by_mask(clip_a: vs.VideoNode, clip_b: vs.VideoNode, mask: str, frames: list) -> vs.VideoNode:
    return at.rfs(clip_a, at.ApplyImageMask(clip_a, clip_b, mask, preview=False), [frames])

src = core.lsmas.LWLibavSource(r"F:\[1] bea\Encode\Video\ncha 1\001.vob")
ivtc = core.tivtc.TFM(src)
ivtc = ivtc.std.SetFieldBased(0)
ivtc = ivtc.tivtc.TDecimate()

ivtc = core.std.Crop(ivtc,6,0,0,0)
rektc = rekt.rektlvls(ivtc,colnum=[0,1,711,712,713],colval=[-4,10,10,-5,5])
rektc1 = rektc.resize.Bicubic(640,480,transfer=6,matrix=6,primaries=6)
rektc2 = rektc1.resize.Bicubic(src_top=0.85)
rektcf = core.std.ShufflePlanes([rektc1,rektc2],[0,1,2],YUV)

vinv = havsfunc.Vinverse2(rektcf)
c16 = depth(vinv,16)
c16 = ToYUV(vsmlrt.DPIR(ToRGB(c16,6,32),30,backend=vsmlrt.Backend.TRT(),tilesize=[640,360], model=3),6,'420',16)
den = MVTools(c16,3,3,thSAD=200, pel_type=PelType.NONE, block_size=32, overlap=16, range_conversion=1, rfilter=4, sharp=2, sad_mode=SADMode.ADAPTIVE_SATD_DCT.same_recalc, search=SearchMode.HEXAGON.defaults, motion=MotionMode.HIGH_SAD).degrain()
den = ccd(den,4,0,matrix=1,planes=[1,2])
den = contrasharpening(den,c16,3,planes=[0,1,2])
den = FastLineDarkenMOD(den,20)
merged = vsdehalo.fine_dehalo(den,2.2,2.2,0,0.5)
gr = vsdeband.AddNoise.GAUSS((0.15,0),0.95,vskernels.Bicubic,False,luma_scaling=8).grain(merged)
mask = at.retinex_edgemask(merged, 0.1)
gr = core.std.MaskedMerge(gr, merged, mask, planes=[0,1,2])
c10 = depth(gr,10)
gr.set_output()
core.lsmas.LWLibavSource(r"F:\[1] bea\Encode\Slump (TV-1)\scripts\001-1.mkv").set_output(4)
# outputs block
rektcf.set_output(1)
# den.set_output(2)
# c10.set_output(3)
# gr.set_output(4)
# rektc1.set_output(8)

@echo off
FOR %%I IN (01 02 03 04 05 06 6.5 07 08 09 10 11 12 13 SP) DO (
"C:\Users\Art\Downloads\Progi\All\Encode\VapourSynth\core\vspipe.exe" -y %%I.vpy - | "C:\Users\Art\Downloads\Progi\All\Encode\x265\x265-x64-v3.6+30-aMod-gcc13.2.0-opt-znver3.exe" --pme --pmode -F 16 --cutree --qp-adaptation-range 2 --open-gop --cbqpoffs -2 --crqpoffs -2 --no-early-skip --rskip 0 --keyint 240 --ref 4 --bframes 7 --ctu 32 --max-tu-size 16 --b-pyramid --b-adapt 2 --no-sao --no-sao-non-deblock --aq-mode 3 --no-strong-intra-smoothing --aq-strength 1.03 --deblock 1:-1 --tu-intra-depth 2 --refine-intra 4 --dynamic-refine --tu-inter-depth 2 --me 3 --wpp --subme 7 --crf 15 --b-pyramid --weightp --weightb --rd 5 --rdoq-level 2 --psy-rdoq 2  --refine-mv 3 --analyze-src-pics --temporal-mvp --max-merge 5 --qcomp 0.72 --info --colorprim bt709 --transfer bt709 --colormatrix bt709 --output "%%I.hevc" --y4m -
)
pause
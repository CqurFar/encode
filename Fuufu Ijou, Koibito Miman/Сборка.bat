@chcp 1251
@echo off
FOR %%I IN (01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40) DO (


"C:\Program Files\MKVToolNix\mkvmerge.exe" --ui-language ru --priority lower --output ^"E:\������\Fuufu Ijou, Koibito Miman\%%I.mkv^" --language 0:ja --track-name ^"0:BDRip by Zagzad^" ^"^(^" ^"E:\������\Fuufu Ijou, Koibito Miman\�������\%%I.hevc^" ^"^)^" --language 0:ja ^"^(^" ^"E:\������\Fuufu Ijou, Koibito Miman\Sound\EP %%I.mlp^" ^"^)^" --chapter-language und --chapters ^"E:\������\Fuufu Ijou, Koibito Miman\�����\EP %%I.xml^" --track-order 0:0,1:0
)

pause
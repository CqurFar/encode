@chcp 1251
@echo off
FOR %%I IN (01 02 03 04 05 06 6.5 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26) DO (





"C:\Program Files\MKVToolNix\mkvmerge.exe" --ui-language ru --priority lower --output ^"E:\������\Meikyuu Black Company\%%I.mkv^" --language 0:ja --track-name ^"0:BDRip by Zagzad^" ^"^(^" ^"E:\������\Meikyuu Black Company\�������\%%I.hevc^" ^"^)^" --language 0:ja ^"^(^" ^"E:\������\Meikyuu Black Company\Sound\%%I.flac^" ^"^)^" --chapter-language und --chapters ^"E:\������\Meikyuu Black Company\�hapters\%%I.xml^" --track-order 0:0,1:0

)

pause
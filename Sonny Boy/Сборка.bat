@chcp 1251
@echo off
FOR %%I IN (01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26) DO (





"C:\Program Files\MKVToolNix\mkvmerge.exe" --ui-language ru --priority lower --output ^"E:\������\Sonny Boy\%%I.mkv^" --language 0:ja --track-name ^"0:BDRip by Zagzad^" ^"^(^" ^"E:\������\Sonny Boy\%%I.hevc^" ^"^)^" --language 0:ja ^"^(^" ^"E:\������\Sonny Boy\Sound\%%I.dtshd^" ^"^)^" --chapter-language eng --chapters ^"E:\������\Sonny Boy\CH\%%I.xml^" --track-order 0:0,1:0


)

pause
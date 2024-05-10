@chcp 1251
@echo off
FOR %%I IN (01 02 03 04 05 06 6.5 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26) DO (





"C:\Program Files\MKVToolNix\mkvmerge.exe" --ui-language ru --priority lower --output ^"E:\Работа\Mardock Scramble Trilogy Collection\Mardock Scramble The Third Exhaust\IV %%I.mkv^" --language 0:ja --track-name ^"0:BDRip by Zagzad^" ^"^(^" ^"E:\Работа\Mardock Scramble Trilogy Collection\Mardock Scramble The Third Exhaust\Готовое\IV %%I.hevc^" ^"^)^" --language 0:ja ^"^(^" ^"E:\Работа\Mardock Scramble Trilogy Collection\Mardock Scramble The Third Exhaust\Sound\IV %%I.truehd^" ^"^)^" --track-order 0:0,1:0

)

pause
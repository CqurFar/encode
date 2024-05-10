@chcp 1251
@echo off
FOR %%I IN (01 02 03 04 05 06 6.5 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26) DO (





"C:\Program Files\MKVToolNix\mkvmerge.exe" --ui-language ru --priority lower --output ^"E:\Работа\Green Green RUS\%%I.mkv^" --language 0:ja --track-name ^"0:AI-DVDRip by Zagzad^" --aspect-ratio 0:4/3 ^"^(^" ^"E:\Работа\Green Green RUS\Готовое\%%I.hevc^" ^"^)^" --language 0:ja ^"^(^" ^"E:\Работа\Green Green RUS\Sound\Jpn 2.0\EP %%I.ac3^" ^"^)^" --chapter-language und --chapters ^"E:\Работа\Green Green RUS\Сhapters\%%I.xml^" --track-order 0:0,1:0

)

pause
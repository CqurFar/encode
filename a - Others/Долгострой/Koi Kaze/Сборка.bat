@chcp 1251
@echo off
FOR %%I IN (01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40) DO (


"C:\Program Files\MKVToolNix\mkvmerge.exe" --ui-language ru --priority lower --output ^"E:\Работа\Lovely Complex\Готовое\Menu %%I.mkv^" --language 0:ja --aspect-ratio 0:4/3 --track-name ^"0:AI-DVDRip by Zagzad^" ^"^(^" ^"E:\Работа\Lovely Complex\Готовое\Menu %%I.hevc^" ^"^)^" --language 0:ja ^"^(^" ^"E:\Работа\Lovely Complex\Menu\Sound\Menu %%I.mlp^" ^"^)^" --track-order 0:0,1:0
)

pause
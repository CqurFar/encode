@echo off
FOR %%I IN (01 02 03 04 05 06 6.5 07 08 09 10 11 12 13 SP) DO (

"C:\Users\Art\Downloads\Progi\All\Encode\VapourSynth\core\vspipe.exe" -p -y %%I.vpy %%I.y4m

)
pause
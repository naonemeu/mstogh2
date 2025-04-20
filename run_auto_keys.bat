@echo off
REM @echo @ ------------------------------------------------------------------- @
REM @echo @  IF YOUR CHART IS LEAD/RHYTHM, DON'T FORGET THE GUITAR COOP CHART!  @
REM @echo @              (you can copy and paste from guitar part)              @
REM @echo @ ------------------------------------------------------------------- @
REM @echo.
REM @echo.
REM echo Do you want the drums click in practice mode? (recommended if you are using multitracks)
REM echo.
REM echo Type 1 if yes, 2 if not
REM echo.
REM @echo.
REM @echo.
REM echo Is your chart GUITAR/BASS or LEAD/RHYTHM?
REM echo.
REM echo Type 3 if BASS, 4 if RHYTHM
REM echo.
REM @echo.
REM @echo.
REM @echo Is your chart 'metal_singer' or 'metal_keys'?
REM @echo.
REM @echo Type 5 if SINGER, 6 if KEYS
REM @echo.

del *.mid
ren *.chart convert.chart

python adapt_chart2mid.py convert.chart

ren *.mid notes.mid

python 1.py
python 2y.py

del notes_gh2.tempmid

python 3s.py

del notes_gh2.tempmid2

pause

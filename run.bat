@echo off
@echo @ ------------------------------------------------------------------- @
@echo @  IF YOUR CHART IS LEAD/RHYTHM, DON'T FORGET THE GUITAR COOP CHART!  @
@echo @              (you can copy and paste from guitar part)              @
@echo @ ------------------------------------------------------------------- @
@echo.
@echo.
echo Do you want the drums click in practice mode? (recommended if you are using multitracks)
echo.
echo Type 1 if yes, 2 if not
echo.
set /p click=Please enter 1 or 2: 
@echo.
@echo.
echo Is your chart GUITAR/BASS or LEAD/RHYTHM?
echo.
echo Type 3 if BASS, 4 if RHYTHM
echo.
set /p guitar=Please enter 3 or 4: 
@echo.
@echo.
@echo Is your chart 'metal_singer' or 'metal_keys'?
@echo.
@echo Type 5 if SINGER, 6 if KEYS
@echo.
set /p singer=Pleaser enter 5 or 6: 
@echo on

if /I "%guitar%"=="3" (
    python 1.py
) else (
    python 1y.py
)

if /I "%click%"=="1" (
    python 2.py
) else (
    python 2y.py
)

del notes_gh2.tempmid

if /I "%singer%"=="5" (
    python 3.py
) else (
    python 3s.py
)

del notes_gh2.tempmid2

pause

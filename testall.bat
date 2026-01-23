set NYCMAPSUSER=xxx.xxx.xxx
set NYCMAPCREDS=xxxxx
set PROXY=http://xxxx:xxxxx@xxxx.xxxx:xxxx
set PYTHON1=C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
set PYTHON2=C:\Users\%USERNAME%\AppData\Local\Programs\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
if exist "%PYTHON1%" (
    set PROPY=%PYTHON1%
) else if exist "%PYTHON2%" (
    set PROPY=%PYTHON2%
) 
set TEMP=D:\temp\test
REM "-W ignore" to suppress deprecation warnings from import arcgis
CALL %PROPY% -W ignore .\src\py\test-organization.py
CALL %PROPY% -W ignore .\src\py\test-publisher.py
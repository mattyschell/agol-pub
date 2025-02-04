set NYCMAPSUSER=xx.yy.zz
set NYCMAPCREDS=xxxx
set PROXY=http://user:password@proxy.xyz:port
set PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat
REM -W ignore to suppress deprecation warnings from import arcgis
CALL %PROPY% -W ignore .\src\py\test-organization.py
CALL %PROPY% -W ignore .\src\py\test-publisher.py
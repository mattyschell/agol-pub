REM update
set PROXY=http://user:pass@proxy.server:port
REM review
set URL=https://nyc.maps.arcgis.com/
set BASEPATH=C:\gis
set PUBREPO=%BASEPATH%\agol-pub
set PYTHONPATH=%PUBREPO%\src\py;PYTHONPATH%
c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat publishlayer.py %URL% samplelayer
set CSCLGDB=D:\XX\XXX\xxxxx1.gdb
set AGOLGDBNAME=cscl.gdb
set ITEMID=1abcdefghijklmnopqrstuvwxyz0
set WORKDIR=D:\temp
set NYCMAPSUSER=xxx.xxx.xxx
set NYCMAPCREDS=xxxx
set PROXY=http://xxxx:xxxx@xxxx.xxx:xxxxx
set AGOLPUB=D:\gis\agol-pub\
set TARGETLOGDIR=D:\gis\geodatabase-scripts\logs\replace_cscl_gdb\
set BATLOG=%TARGETLOGDIR%replace-cscl-gdb.log
set NOTIFY=xxx@xxx.xxx.xxx
set NOTIFYFROM=xxx@xxx.xxx.xxx
set SMTPFROM=xxxx.xxxx
set PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat
set PYTHONPATH=%AGOLPUB%\src\py;%PYTHONPATH%
echo starting up our work on %AGOLGDBNAME% on %date% at %time% > %BATLOG%
%PROPY% %AGOLPUB%replace-cscl-gdb.py %CSCLGDB% %AGOLGDBNAME% %ITEMID% %WORKDIR% && (
  echo. >> %BATLOG% && echo replaced %AGOLGDBNAME% on %date% at %time% >> %BATLOG%
  %PROPY% %AGOLPUB%notify.py ": Successfully replaced %AGOLGDBNAME% on nycmaps" %NOTIFY% "replace-cscl" 
) || (
  %PROPY% %AGOLPUB%notify.py ": Failed to replace %AGOLGDBNAME% on nycmaps" %NOTIFY% "replace-cscl" && EXIT /B 1
) 
echo. >> %BATLOG% && echo finished notifying the squad on %date% at %time% >> %BATLOG%

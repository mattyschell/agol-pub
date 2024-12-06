set CSCLGDB=D:\XX\XXX\xxxxx1.gdb
set AGOLGDBNAME=xxxx.gdb
set GDBZIPSIZE=500
set ITEMID=1abcdefghijklmnopqrstuvwxyz0
set ENV=XXX
set WORKDIR=X:\xxxx
set NYCMAPSUSER=xxx.xxx.xxxx
set NYCMAPCREDS=xxxxxxx
set PROXY=http://xxxx:xxxx@xxxx.xxx:xxxxx
set BASEPATH=X:\XXX
set AGOLPUB=%BASEPATH%\agol-pub\
set TARGETLOGDIR=%BASEPATH%\geodatabase-scripts\logs\replace_cscl_gdb\
set BATLOG=%TARGETLOGDIR%replace-XXXX-XXX-gdb.log
set NOTIFY=xxxx@xxx.xxx.xxx
set NOTIFYFROM=xxx@xxx.xxx.xxx
set SMTPFROM=xxxx.xxxx
set PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
set PYTHONPATH0=%PYTHONPATH%
set PYTHONPATH=%AGOLPUB%\src\py;%PYTHONPATH%
echo starting up our work on %AGOLGDBNAME% on %date% at %time% > %BATLOG%
%PROPY% %AGOLPUB%replace-cscl-gdb.py %CSCLGDB% %AGOLGDBNAME% %ITEMID% %WORKDIR% && (
   echo. >> %BATLOG% && echo replaced %AGOLGDBNAME% on %date% at %time% >> %BATLOG%
) || (
   %PROPY% %AGOLPUB%notify.py ": Failed to replace %AGOLGDBNAME% (%ENV%) on nycmaps" %NOTIFY% "replace-cscl" && EXIT /B 1
) 
echo. >> %BATLOG% && echo performing %AGOLGDBNAME% QA on %date% at %time% >> %BATLOG%
%PROPY% %AGOLPUB%replace-cscl-qa.py %ITEMID% %AGOLGDBNAME% %WORKDIR% %GDBZIPSIZE% && (
    %PROPY% %AGOLPUB%notify.py "%ENV%: QA of %AGOLGDBNAME% item %ITEMID%" %NOTIFY% "qa"
) || (
    %PROPY% %AGOLPUB%notify.py "%ENV%: Failed QA of %AGOLGDBNAME% item %ITEMID%" %NOTIFY% "qa"
) 
echo. >> %BATLOG% && echo completed notifying the squad of %AGOLGDBNAME% QA results on %date% at %time% >> %BATLOG%
set PYTHONPATH=%PYTHONPATH0%

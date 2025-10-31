import sys
import datetime
import glob
import os
import smtplib
import socket
from email.message import EmailMessage

# meta-notification:
# we modified his notify.py from the similar notify.pys in neighboring repos


def getlogfile(logdir
              ,logtype):

    # ex get most recent qa-* log from a log dir with logs like
    # import.log
    # export-20210126-165353
    # qa-20210126-165300

    list_of_logs = glob.glob(os.path.join(logdir
                                         ,'{0}*.log'.format(logtype)))

    latest_log = max(list_of_logs, key=os.path.getctime)

    with open(os.path.join(logdir, latest_log), 'r') as file:
        loglines = file.read()

    return loglines

def getspecialcontent(notification
                     ,baseurl='https://nyc.maps.arcgis.com/home/item.html?id='
                     ,wiki='https://appdevwiki.nycnet/appdev/index.php?title=GIS_Data_Maintenance_Scripts#CSCL_Publishing_To_NYCMaps'):

    # PRD: Replaced and QAd nycmaps cscl_pub.gdb item 9163b04952354da2bf748abe1788e985
    itemid = notification.split()[-1]

    scontent  = '{0}{1}'.format(baseurl
                               ,itemid)
    scontent += '{0}Running from {1}'.format(os.linesep
                                           ,socket.gethostname())
    scontent += '{0}See the wiki for more info-- {1}'.format(os.linesep,
                                                             wiki)
    
    return scontent


if __name__ == "__main__":

    notification    = sys.argv[1]
    pemails         = sys.argv[2]
    plogtype        = sys.argv[3] # ex 'qa' 'export' '*' (latest)
    
    if len(sys.argv) == 4:
        pchecklogfor = 'nothing'
    else:
        # pass in ERROR for example
        # to only notify if ERROR appears in the log
        pchecklogfor = sys.argv[4]

    logdir          = os.environ['TARGETLOGDIR']
    emailfrom       = os.environ['NOTIFYFROM']
    smtpfrom        = os.environ['SMTPFROM']

    msg = EmailMessage()

    # notification is like "importing buildings onto dev.sde"

    msg['Subject'] = '{0}'.format(notification)

    content  = '{0}{1}'.format(notification
                               ,os.linesep)

    content += 'at {0} {1}'.format(datetime.datetime.now()
                                  ,os.linesep)
    
    if not 'fail' in notification.lower():
        content += '{0}{1}'.format(getspecialcontent(notification)
                                  ,os.linesep)

    content += os.linesep + getlogfile(logdir
                                      ,plogtype)   
    
    msg.set_content(content)    
    msg['From'] = emailfrom

    # this is headers only 
    # if a string is passed to sendmail it is treated as a list with one element!
    msg['To'] = pemails

    if  (pchecklogfor != 'nothing' and pchecklogfor in content) \
    or   pchecklogfor == 'nothing':
        
        smtp = smtplib.SMTP(smtpfrom)

        try:
            smtp.sendmail(msg['From']
                         ,msg['To'].split(",")
                         ,msg.as_string())
        except smtplib.SMTPRecipientsRefused as e:
            print("\n notify.py - Email not sent: relaying denied.")
            print(" notify.py - This is expected from desktop environments.\n")

        smtp.quit()

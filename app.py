from flask import Flask,render_template, request, redirect,url_for,flash
from datetime import datetime
from common import getAzureConfig, writeToJSON, logger, getLogFileSavePath, getInterval, getSecretKey
import pandas as pd
import numpy as np
import secrets

# all graph related operations 
from ops.msgraph import getGroupLogs, processGroupLogs
from db.dbops import insert_interpretation_to_DB
app = Flask(__name__)

#security
app.config['SECRET_KEY'] = getSecretKey("./config/config.yaml")

# all mail related imports 
from ops.mail import notifyChanges


def getLogsFromAzure():

    config = getAzureConfig("./config/config.yaml")
    group_logs = getGroupLogs(config)

    path = getLogFileSavePath("./config/config.yaml")

    filename = path + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ".json"

    writeToJSON(filename,group_logs)
    logger.info('Azure log saved at: ' + filename)

    processGroupLogs(group_logs)
    notifyChanges()
    

# home page 
@app.route("/")
def index():
    from db.dbops import get_actions_overview

    actions_overview = get_actions_overview()

    df = pd.DataFrame (actions_overview)
    # remove the None values and replace it with a '' string 
    df = df.fillna(value="")
    
    # Combine name and source ID as a single column called Affected Objects for ease of processing. Final format will be 
    # name-of-user(36_digit_id)

    df["affectedobjects"] = df['name'].astype(str) +"("+ df["sourceobjectid"]+")"

    # combine common rows and concatenate the affected objects column with a ','
    df2 = df.groupby(['id','activitydatetime','activitydisplayname','interpretation'])['affectedobjects'].apply(', '.join).reset_index()
    df2.sort_values(by=['activitydatetime'], ascending = False, inplace=True)

    # create a dictionary which can be sent to the template 
    df2dict=df2.to_dict('records')

    return render_template("index.html", actions_overview=df2dict)


from apscheduler.schedulers.background import BackgroundScheduler

sync_interval = getInterval("./config/config.yaml")['interval_minutes']
logger.info('Sync interval is : ' + str(sync_interval) + ' minutes')


sched = BackgroundScheduler(daemon=True)
sched.add_job(getLogsFromAzure,'interval',minutes=sync_interval)
sched.start()

if __name__=='__main__':

    app.run(host='0.0.0.0', port =5000, debug=False, use_reloader=False)

    
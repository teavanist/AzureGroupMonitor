from flask import Flask
from flask_mail import Mail, Message
from common import getMailConfig, logger

from db.dbops import get_unnotified_changes, update_notification_status

config = getMailConfig("./config/config.yaml")


def notifyChanges():
  from datetime import datetime
  import pytz

  changes = get_unnotified_changes()

  logger.info('Total entries to notify: ' + str(len(changes)))

  for change in changes:
    title = "Group activity " +str(change['activitydisplayname']) +" detected on " + str(change['activitydatetime'])
    mailbody = 'Date: ' + str(change['activitydatetime']) + '\n' + \
                'Type of action: ' + str(change['activitydisplayname']) + '\n' + \
                'Details:: ' + str(change['interpretation']) 
    testmail(title,mailbody)
    mail_sent_time = pytz.utc.localize(datetime.now())

    logger.info('Sending email for the change: ' + title)
    update_notification_status(change['id'],mail_sent_time) 



def testmail(title, mailbody):

  mail = Mail()
  app = Flask(__name__)
  
  app.config['MAIL_SERVER']=config['MAIL_SERVER']
  app.config['MAIL_PORT'] = config['MAIL_PORT']
  app.config['MAIL_USERNAME'] = config['MAIL_USERNAME']
  app.config['MAIL_PASSWORD'] = config['MAIL_PASSWORD']
  app.config['MAIL_USE_TLS'] = config['MAIL_USE_TLS']
  app.config['MAIL_USE_SSL'] = config['MAIL_USE_SSL']

  mail.init_app(app)
  msg = Message(title, sender =   config['MAIL_SENDER'], recipients = [config['MAIL_RECIPIENT']])
  msg.body = mailbody

  with app.app_context():
      mail.send(msg)

  logger.info('Message sent')




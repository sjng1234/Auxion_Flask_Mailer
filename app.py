# importing libraries
from flask import Flask,request,jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from datetime import datetime

import firebase_admin
from firebase_admin import credentials,firestore
from dotenv import load_dotenv

import os

# For local
# load_dotenv('./.env')

cred_dict = {
  "type": os.environ.get('FB_ACC_TYPE'),
  "project_id": os.environ.get('FB_PROJECT_ID'),
  "private_key_id": os.environ.get('FB_PRIV_KEY_ID'),
  "private_key": os.environ.get('FB_PRIV_KEY').replace('\\n', '\n'),
  "client_email": os.environ.get('FB_CLIENT_EMAIL'),
  "client_id": os.environ.get('FB_CLIENT_ID'),
  "auth_uri": os.environ.get('FB_AUTH_URI'),
  "token_uri": os.environ.get('FB_TOKEN_URI'),
  "auth_provider_x509_cert_url": os.environ.get('FB_AUTH_PROVIDER_CERT_URL'),
  "client_x509_cert_url": os.environ.get('FB_CLIENT_CERT_URL')
}
print(cred_dict)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
db = firestore.client()
email_ref = db.collection("collectionDetails")
   
app = Flask(__name__)
mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']= os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# enable CORS 
CORS(app)
# Testing Admin API
@app.route('/get',methods=['POST'])
def get():
    try:
        id = request.json['id']
        if id:
            email = email_ref.document(id).get()
            return jsonify(email.to_dict()),200
    except Exception as e:
        return f"An Error Occured: {e}"

def retrieve_email_data(email_id):
    try:
        email = email_ref.document(email_id).get()
        return dict(email.to_dict())
    except Exception as e:
        return False

# message object mapped to a particular URL ‘/’
@app.route("/send",methods=['POST'])
def index():
    id = request.json['id']
    print(id)
    email_data = retrieve_email_data(id)
    # print(email_data)
    if email_data:
        toEmail = email_data['toEmail']
        collectTime = str(email_data['collectionTime']).split('+')[0]
        collectVenue = email_data['collectionVenue']
        eventName = email_data['eventName']

        itemImage = email_data['itemImage']
        itemName = email_data['itemName']

        msg = Message(
                    'Reminder for Collection of Auxion Item',
                    sender =("Auxion Service Account",'noreply.auxion@gmail.com'),
                    recipients = [toEmail]
                  )
        msg.html = f'<h1>Thank you for your support for {eventName}</h1>\
        <p>Here\'s a reminder for you to collect your bidded item:</p>\
        <img src="{itemImage}" style="max-height:100px; max-width:auto"/>\
        <p><b>Item Purchased:</b> {itemName}</p>\
        <p><b>Collection Venue:</b> {collectVenue}</p>\
        <p><b>Collection Time:</b> {collectTime}</p>\
        '
        mail.send(msg)
        return 'Sent',200
    else:
        return 'Invalid Email Id',400
   
if __name__ == '__main__':
   app.run()
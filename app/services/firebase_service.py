import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
import json
import logging
import datetime
import time


# create credentials json
load_dotenv()
cred_json = {
  "type": os.getenv("FB_TYPE"),
  "project_id": os.getenv("FB_PROJECT_ID"),
  "private_key_id": os.getenv("FB_PRIVATE_KEY_ID"),
  "private_key": os.getenv("FB_PRIVATE_KEY").replace('\\n', '\n'),
  "client_email": os.getenv("FB_CLIENT_EMAIL"),
  "client_id": os.getenv("FB_CLIENT_ID"),
  "auth_uri": os.getenv("FB_AUTH_URI"),
  "token_uri": os.getenv("FB_TOKEN_URI"),
  "auth_provider_x509_cert_url": os.getenv("FB_AUTH_PROVIDER_X509_CERT_URL"),
  "client_x509_cert_url": os.getenv("FB_CLIENT_X509_CERT_URL"),
  "universe_domain": os.getenv("FB_UNIVERSE_DOMAIN")    
}
cred = credentials.Certificate(cred_json)

#Check if firebase app already exists
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)
    firestore.client()

db = firestore.client()

# Add a new thread to the database
def store_thread_in_firestore(wa_id, thread_id):
    logging.info(f"FIRESTORE: Storing {thread_id} for {wa_id} in firestore")

    doc_ref = db.collection(u'threads').document(wa_id)
    doc_ref.set({
        u'thread_id': thread_id
    })

# Retrieve a thread from the database
def check_if_thread_exists_in_firestore(wa_id):
    logging.info(f"FIRESTORE: Checking firestore for thread {wa_id}")

    doc_ref = db.collection(u'threads').document(wa_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()['thread_id']
    else:
        return None 

def store_message(role, wa_id, data):
    # wa_id = '18583496538'
    logging.info(f"FIRESTORE: Storing data for {wa_id}")
    
    doc_ref= db.collection(u'threads').document(wa_id).collection(u'messages').document()
    # data = {"messaging_product": "whatsapp", "recipient_type": "individual", "to": "18583496538", "type": "text"}
    data = json.loads(data)
    data['role'] = role
    data['timestamp'] = time.time()
    data['utcDateTime'] = datetime.datetime.now(datetime.UTC)
    doc_ref.set(data)

    
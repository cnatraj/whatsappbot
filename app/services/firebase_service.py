import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
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

#TODO:Change this. Hardcoded Values for now
org_uuid = os.getenv("ORG_UUID")
bot_id = os.getenv("PHONE_NUMBER_ID")

#Check if firebase app already exists
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred)
    firestore.client()

db = firestore.client()

# Add a new thread to the database
def store_thread_in_firestore(wa_id, thread_id, name):
    logging.info(f"FIRESTORE: Storing {thread_id} for {wa_id} and {name} in firestore")

    doc_id = wa_id + "_" + bot_id
    threads_ref = db.collection("threads").document(doc_id)
    
    thread_data = {
        "bot_id":bot_id,
        "createdAt":datetime.datetime.now(datetime.UTC),
        "org_uuid":org_uuid,
        "thread_id":thread_id,
        "wa_id": wa_id,
        "name": name
    }
    threads_ref.set(thread_data)

# Retrieve a thread from the database
def check_if_thread_exists_in_firestore(wa_id):
    

    logging.info(f"FIRESTORE: Checking firestore for thread {wa_id}")
    doc_id = wa_id + "_" + bot_id
    threads_ref = db.collection("threads").document(doc_id)

    doc = ( threads_ref.get() )
    if doc.exists:
        return doc.to_dict()['thread_id']
    else:
        return None

def store_message(role, wa_id, data):
    # wa_id = '18583496538'
    logging.info(f"FIRESTORE: Storing data for {wa_id}")
    doc_id = wa_id + "_" + bot_id
    threads_ref = db.collection("threads").document(doc_id)
    messages_ref = threads_ref.collection('messages').document()

    # doc_ref= db.collection(u'threads').document(wa_id).collection(u'messages').document()
    # data = {"messaging_product": "whatsapp", "recipient_type": "individual", "to": "18583496538", "type": "text"}
    data = json.loads(data)
    data['role'] = role
    data['timestamp'] = time.time()
    data['utcDateTime'] = datetime.datetime.now(datetime.UTC)
    messages_ref.set(data)
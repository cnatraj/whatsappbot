import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import logging
import datetime
import time

# get the credentials from the json file
dir_path = os.path.dirname(os.path.realpath(__file__))
cred = credentials.Certificate(f'{dir_path}/firebase_credentials.cred.json')

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

    
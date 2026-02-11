from google.cloud import firestore

db = firestore.Client()

COLLECTION = "moto"
DOC_ID = "estado"

def load_data() -> dict:
    doc_ref = db.collection(COLLECTION).document(DOC_ID)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    return {}

def save_data(data: dict):
    doc_ref = db.collection(COLLECTION).document(DOC_ID)
    doc_ref.set(data)

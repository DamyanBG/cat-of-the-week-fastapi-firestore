from google.cloud import firestore

from sa import credentials
from config import DATABASE_NAME


db = firestore.Client(credentials=credentials, database=DATABASE_NAME)

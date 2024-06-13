from dotenv import load_dotenv
import os

load_dotenv()

SA_KEY_PATH = os.environ["SA_KEY_PATH"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
JWT_KEY = os.environ["JWT_KEY"]

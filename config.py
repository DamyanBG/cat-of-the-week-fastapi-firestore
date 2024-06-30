from dotenv import load_dotenv
import os

load_dotenv()

SA_KEY_PATH = os.environ["SA_KEY_PATH"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
JWT_KEY = os.environ["JWT_KEY"]

# AWS credentials
AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
AWS_BUCKET_NAME = os.environ["AWS_BUCKET_NAME"]
AWS_REGION = os.environ["AWS_REGION"]
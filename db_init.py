from dotenv import load_dotenv
import os
import firebase_admin

load_dotenv('.env')

credentials = firebase_admin.credentials.Certificate(
    os.getenv('DATABASE_CREDENTIALS'))

app = firebase_admin.initialize_app(credentials,
                                    {'databaseURL': os.getenv('DATABASE_URL')})

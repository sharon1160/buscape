import firebase_admin

cred_path = 'credentials.json'
db_URL = 'https://wikisearcher-3d8ed-default-rtdb.firebaseio.com/'

credentials = firebase_admin.credentials.Certificate(cred_path)
app = firebase_admin.initialize_app(credentials, {
    'databaseURL': db_URL
})

#%%
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

#%%
configFile = "/Users/giuseppecrosti/virtualenvs/pelican/file-generator/firebase-remote-db/brine-599f1-firebase-adminsdk-gw1vi-af9879964f.json"
cred = credentials.Certificate(configFile)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://brine-599f1.firebaseio.com/',
    'databaseAuthVariableOverride': None,
    'storageBucket': "brine-599f1.appspot.com"
})

#%%
bucket = firebase_admin.storage.bucket()
print(bucket.list_blobs())

# %%
for blob in bucket.list_blobs():
    #blob.make_public()
    #print(blob.public_url)
    print(blob)

# %%
path = 'duSOWxfjRWKtJ6c3NnJgso/10/7'
print(bucket.get_blob(path))


# %%

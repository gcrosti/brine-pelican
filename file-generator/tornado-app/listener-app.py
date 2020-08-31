import tornado.ioloop
import tornado.web
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import json
from localdbutils import *

referenceId = 'asdkfjhasdlfaxdoifasfjndls'


configFile = "/Users/giuseppecrosti/virtualenvs/pelican/file-generator/firebase-remote-db/brine-599f1-firebase-adminsdk-gw1vi-af9879964f.json"
cred = credentials.Certificate(configFile)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://brine-599f1.firebaseio.com/',
    'databaseAuthVariableOverride': None,
    'storageBucket': "brine-599f1.appspot.com"
})

bucket = firebase_admin.storage.bucket()

def ignore_first_call(fn):
    called = False

    def wrapper(*args, **kwargs):
        nonlocal called
        if called:
            return fn(*args, **kwargs)
        else:
            called = True
            return None

    return wrapper



@ignore_first_call
def listener(event):
    #print(event.event_type)  # can be 'put' or 'patch'
    #print(event.path)  # relative to the reference, it seems
    #print(event.data)  # new data at /reference/event.path. None if deleted
    #print(bucket.list_blobs())
    print()

    s3DAO = S3DAO()

    is_dish_new = False
    is_dish_deleted = False

    if event.event_type == 'put':
        parsedPath = parsePath(event.path)
        is_dish_new = s3DAO.isDishNew(parsedPath.userId,parsedPath.dishId)

    if parsedPath.dataType == 'MEAL':
        if is_dish_new:
            s3DAO.addDishToUsersDishes(parsedPath.userId,parsedPath.dishId)
            s3DAO.addDishToPagesContent(parsedPath.userId,parsedPath.dishId)
        
    if parsedPath.dataType == 'IMAGES':
        print(event.data)
    
    if parsedPath.dataType == 'FUNCTIONS':
        print(parseFunctions(event.data))
    
    if parsedPath.dataType == None:
        try:
            s3DAO.deleteDishFromUsersDishes(parsedPath.userId,parsedPath.dishId)
            is_dish_deleted = True
        except:
            print("DELETION FAILED") 
            
    if is_dish_deleted or is_dish_new:
        s3DAO.saveUsersDishesToS3(parsedPath.userId)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world here I come")
        
        

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    db.reference(referenceId).listen(listener)
    tornado.ioloop.IOLoop.current().start()




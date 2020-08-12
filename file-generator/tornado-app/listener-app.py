import tornado.ioloop
import tornado.web
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
referenceId = 'asdkfjhasdlfaxdoifasfjndls'

configFile = "/Users/giuseppecrosti/virtualenvs/pelican/file-generator/firebase-remote-db/brine-599f1-firebase-adminsdk-gw1vi-af9879964f.json"
cred = credentials.Certificate(configFile)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://brine-599f1.firebaseio.com/',
    'databaseAuthVariableOverride': None
})



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
    print(event.event_type)  # can be 'put' or 'patch'
    print(event.path)  # relative to the reference, it seems
    print(event.data)  # new data at /reference/event.path. None if deleted

    if event.event_type == 'put':
        if event.data != None:
            print(event)

    node = str(event.path).split('/')[-2] #you can slice the path according to your requirement
    property = str(event.path).split('/')[-1] 
    value = event.data




class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world here I come")
        db.reference(referenceId).listen(listener)
        

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()




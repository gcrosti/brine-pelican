#%%
from yattag import Doc
from yattag import indent
import json
firebaseKey = 'asdkfjhasdlfaxdoifasfjndls'
from datetime import date
import html

#%% LOAD DATA
with open("/Users/giuseppecrosti/virtualenvs/pelican/file-generator/brine-599f1-export-sample.json",'r') as f:
    testData = json.loads(f.read())

#%%
doc, tag, text = Doc().tagtext()
doc.asis(page)
with tag('head'):
        with tag('title'):
            text("this is a new title")

print(doc.getvalue())
#%% RETRIEVE INSTANCE IDs
instanceIds = []

for instanceId in testData[firebaseKey]:
    
    instanceIds.append(instanceId)
print(instanceIds)

#%% RETRIEVE MEAL NAMES
mealNames = []
instanceId = instanceIds[0]

for data in testData[firebaseKey][instanceId]:
    if data == None:
        continue
    mealName = data['MEAL']['name']
    mealNames.append(mealName)

print(mealNames)

#%% CREATE PAGE FOR EACH MEAL
todayDate = date.today()
for name in mealNames:
    doc, tag, text = Doc().tagtext()
    with tag('head'):
        with tag('title'):
            text(name)
        doc.stag('meta',name='date',content='2020-07-22')
        doc.stag('meta',name='category',content=instanceId)


    destination = '/Users/giuseppecrosti/virtualenvs/pelican/content/' + name + '.html'
    with open(destination,'w') as f:
        f.write(indent(doc.getvalue()))
# %%

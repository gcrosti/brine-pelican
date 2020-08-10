
#%%
from yattag import Doc
from yattag import indent
import json

#%% LOAD DATA
with open("/Users/giuseppecrosti/virtualenvs/pelican/file-generator/brine-599f1-export-sample.json",'r') as f:
    out = json.loads(f.read())

print(out)
#%%
doc, tag, text = Doc().tagtext()

with tag('head'):
    with tag('title'):
        text('hello world from the bot!')
    doc.stag('meta',name='date',content='2020-07-22')


with open("/Users/giuseppecrosti/virtualenvs/pelican/content/helloworld.html",'w') as f:
    f.write(indent(doc.getvalue()))
# %%

#%%
import boto3
import json
from datetime import datetime
import ast
USERS_DISHES_S3_KEY = 'users-dishes'
PAGE_CONTENT_S3_KEY = 'page-content'
BRINE_DATA_BUCKET_NAME = 'brine-data'

#%%
s3 = boto3.client('s3')
buckets = s3.list_buckets()

for bucket in buckets['Buckets']:
    print (bucket["Name"])

# %%
with open("/Users/giuseppecrosti/virtualenvs/pelican/file-generator/brine-599f1-export-sample.json",'r') as f:
    testData = json.loads(f.read())

# %%
emptyDict = {}
s3.put_object(Bucket = BRINE_DATA_BUCKET_NAME, Key = USERS_DISHES_S3_KEY, Body = json.dumps(emptyDict))
s3.put_object(Bucket = BRINE_DATA_BUCKET_NAME, Key = PAGE_CONTENT_S3_KEY, Body = json.dumps(emptyDict))
#%%
s3Object = s3.get_object(Bucket = BRINE_DATA_BUCKET_NAME, Key = USERS_DISHES_S3_KEY)
usersDishesBytes = s3Object['Body'].read()
usersDishesStr = usersDishesBytes.decode("UTF-8")
usersDishes = ast.literal_eval(usersDishesStr) 
print(usersDishes)
#%%
s3Object = s3.get_object(Bucket = 'brine-pelican-users-dishes', Key = 'type-json')
usersDishes = s3Object['Body'].read()
timestampString = s3Object['ResponseMetadata']['HTTPHeaders']['last-modified']
nowDatetime = datetime.now()
dataDatetime = datetime.strptime(timestamp[:-4],"%a, %d %b %Y %H:%M:%S")

print(type(timestamp))
print(dataDatetime)
print(nowDatetime < dataDatetime)
print(nowDatetime > dataDatetime)
print(nowDatetime == dataDatetime)
# %%

#%%
import boto3
import json
USERS_DISHES_S3_KEY = 'users-dishes'
PAGE_CONTENT_S3_KEY = 'page-content'

#%%
s3 = boto3.client('s3')
buckets = s3.list_buckets()

for bucket in buckets['Buckets']:
    print (bucket["Name"])

# %%
with open("/Users/giuseppecrosti/virtualenvs/pelican/file-generator/brine-599f1-export-sample.json",'r') as f:
    testData = json.loads(f.read())

# %%
s3.put_object(Bucket = 'brine-pelican-users-dishes', Key = 'type-json', Body = json.dumps(testData))
# %%
s3Object = s3.get_object(Bucket = 'brine-pelican-users-dishes', Key = 'type-json')
usersDishes = s3Object['Body'].read()

print(s3Object['ResponseMetadata']['HTTPHeaders']['last-modified'])

# %%

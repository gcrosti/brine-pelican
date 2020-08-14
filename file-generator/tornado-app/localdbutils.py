import json



def loadLocalDb(): 
    with open("/Users/giuseppecrosti/virtualenvs/pelican/file-generator/local-db/local-db.json","r") as d:
        data = json.loads(d.read())
    
    return data


def saveDbToLocal(data: dict):
    with open("/Users/giuseppecrosti/virtualenvs/pelican/file-generator/local-db/local-db.json","w") as d:
        d.write(json.dumps(data))

def isUserInLocalDb(userId:str, data:dict):
    for id in data:
        if id == userId:
            return True
    return False

def addOrUpdateUser(userId:str,dishes:list,data: dict):
    data[userId] = dishes


def parsePath(path:str):
    firstSlash = path.find("/",1)
    secondSlash = path.find("/",firstSlash+1)
    userId = path[1:firstSlash]
    dishId = path[firstSlash+1:secondSlash]
    dataType = path[secondSlash+1:]
    if secondSlash == -1:
        dishId = path[firstSlash+1:]
        dataType = None
    
    return ParsedPath(userId,dishId,dataType)


class ParsedPath:
    def __init__(self, userId: str, dishId: int, dataType: str):
        self.userId = userId
        self.dishId = dishId
        self.dataType = dataType
        

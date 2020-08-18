import json



def loadUsersDishesFromS3(): 
    with open("/Users/giuseppecrosti/virtualenvs/pelican/file-generator/local-db/local-db.json","r") as d:
        data = json.loads(d.read())
    
    return data


def saveUsersDishesToS3(data: dict):
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


def parseFunctions(functions:dict):
    out = ""
    ingredientEmoji = "🌶️"
    beverageEmoji = "🍹"
    dessertEmoji = "🍩"
    proteinEmoji = "🍖"
    starchEmoji = "🥖"
    vegetableEmoji = "🥦"
    dipEmoji = "🥣"
    dressingEmoji = "🥗"
    commaSpace = ", "

    if functions["beverage"]:
        out += (beverageEmoji + " Beverage")
    if functions["dessert"]:
        out += (commaSpace + dessertEmoji + " Dessert")
    if functions["dip"]:
        out += (commaSpace + dipEmoji + " Dip")
    if functions["dressing"]:
        out += (commaSpace + dressingEmoji + " Dressing")
    if functions["ingredient"]:
        out += (commaSpace + ingredientEmoji + " Ingredient")
    if functions["protein"]:
        out += (commaSpace + proteinEmoji + " Protein")
    if functions["starch"]:
        out += (commaSpace + starchEmoji + " Starch")
    if functions["veg"]:
        out += (commaSpace + vegetableEmoji + " Vegetable")
    
    return out

class ParsedPath:
    def __init__(self, userId: str, dishId: int, dataType: str):
        self.userId = userId
        self.dishId = dishId
        self.dataType = dataType
        
class ParsedDishData:
    def __init__(self, userId: str, title: str, description = "", images = [], content = ""):
        self.userId = userId
        self.title = title
        self.description = description
        self.images = images
        self.content = content
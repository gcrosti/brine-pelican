import json
import boto3
from datetime import datetime
import ast

class S3DAO:
    USERS_DISHES_S3_KEY = 'users-dishes'
    PAGE_CONTENT_S3_KEY = 'page-content'
    BRINE_DATA_BUCKET_NAME = 'brine-data'

    def __init__(self):
        self.s3_client = None
        self.users_dishes_last_modified = None
        self.page_content_last_modified = None
        self.users_dishes = None
        self.pages_content = None

    def __getS3Client(self):
        if self.s3_client is None:
            self.s3_client = boto3.client('s3')
        return self.s3_client


    # GETTERS AND SETTERS FOR USERS DISHES

    def __getUsersDishesFromS3(self): 
        if self.users_dishes is None:
            s3 = self.__getS3Client()
            s3Object = s3.get_object(Bucket = self.BRINE_DATA_BUCKET_NAME, Key = self.USERS_DISHES_S3_KEY)
            users_dishes_str = s3Object['Body'].read().decode("UTF-8")
            self.users_dishes = ast.literal_eval(users_dishes_str)
            self.users_dishes_last_modified = self.__getTimeStampOfLastUpdateFromS3(self.USERS_DISHES_S3_KEY,s3Object)
        
        return self.users_dishes

    def __getTimeStampOfLastUpdateFromS3(self,bucketKeyName: str, s3Object = None):
        if s3Object is None:
            s3 = self.__getS3Client()
            s3Object = s3.get_object(Bucket = self.BRINE_DATA_BUCKET_NAME, Key = bucketKeyName)
        timestamp = self.__getTimeStampFromS3Object(s3Object)

        return timestamp

    def __saveUsersDishesToS3(self,data: dict):
        s3 = self.__getS3Client()
        data_as_json = json.dumps(data)
        s3.put_object(Bucket = self.BRINE_DATA_BUCKET_NAME, Key = self.USERS_DISHES_S3_KEY, Body = data_as_json)

    def __getTimeStampFromS3Object(self,s3Object):
        timeAsString = s3Object['ResponseMetadata']['HTTPHeaders']['last-modified']
        timeAsDt = datetime.strptime(timeAsString[:-4],"%a, %d %b %Y %H:%M:%S")

        return timeAsDt

    def __isUserInDb(self,userId:str):
        usersDishes = self.__getUsersDishesFromS3()
        for id in usersDishes:
            if id == userId:
                return True
        return False

    def __createNewUserInUsersDishes(self,userId:str):
        self.users_dishes[userId] = []

    def addDishToUsersDishes(self,userId: str, dishId:str):
        usersDishes = self.__getUsersDishesFromS3()
        isUserInDB = self.__isUserInDb(userId)
        if not isUserInDB:
            self.__createNewUserInUsersDishes(userId)
        usersDishes[userId].append(dishId)
    
    def deleteDishFromUsersDishes(self,userId: str, dishId: str):
        isDishNew = self.isDishNew(userId,dishId)
        if isDishNew:
            return
        self.users_dishes[userId].remove(dishId)

    def isDishNew(self,userId: str, dishId: str):
        userDishes = self.__getUsersDishesFromS3()[userId]
        if dishId in userDishes:
            return False
        return True
    
    def saveUsersDishesToS3(self, userId:str):
        latest_update_timestamp = self.__getTimeStampOfLastUpdateFromS3(self.USERS_DISHES_S3_KEY)
        usersDishesToSave = dict(self.users_dishes)
        if latest_update_timestamp < self.users_dishes_last_modified:
            usersDishesToSave = self.__getUsersDishesFromS3()
            usersDishesToSave[userId] = self.users_dishes[userId]
        print('users dishes to save')
        print(usersDishesToSave)
        self.__saveUsersDishesToS3(usersDishesToSave)  

    # GETTERS AND SETTERS FOR PAGE CONTENT

    def getPageContentFromS3(self):

        return

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
            out += (beverageEmoji + " Beverage" + commaSpace)
        if functions["dessert"]:
            out += (dessertEmoji + " Dessert" + commaSpace)
        if functions["dip"]:
            out += (dipEmoji + " Dip" + commaSpace)
        if functions["dressing"]:
            out += (dressingEmoji + " Dressing" + commaSpace)
        if functions["ingredient"]:
            out += (ingredientEmoji + " Ingredient" + commaSpace)
        if functions["protein"]:
            out += (proteinEmoji + " Protein" + commaSpace)
        if functions["starch"]:
            out += (starchEmoji + " Starch" + commaSpace)
        if functions["veg"]:
            out += (vegetableEmoji + " Vegetable" + commaSpace)
        
        return out[:-2]

class ParsedPath:
    def __init__(self, userId: str, dishId: int, dataType: str):
        self.userId = userId
        self.dishId = dishId
        self.dataType = dataType
        
class PageContent:
    def __init__(self, userId: str, dishId: str, title: str, description = "", images = [], content = ""):
        self.userId = userId
        self.dishId = dishId
        self.title = title
        self.description = description
        self.images = images
        self.content = content
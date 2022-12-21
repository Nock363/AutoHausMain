from pymongo import MongoClient
import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class MongoHandler():

    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db  = self.client.main 

    
    def getPin(self,pinID):
        pins = self.db.pins
        return pins.find_one({'pinID':6})




# def main():
#     mongoHandler = MongoHandler()
#     pinData = mongoHandler.getPin(6)
#     logging.info(f"found pin: {pinData}")



# main()
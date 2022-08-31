from pymongo import MongoClient
import json

# 몽고DB PortNumber= 27017
client = MongoClient(port=27017)
db = client.bitDB

# inventory collection 의 모든것을 inventory 변수에 저장
inventory = db.inventory.find()
for inv in inventory:  # inventory내의 객체 1개씩 출력
    print(inv)

# inventory 변수에 insert
newInvent = {
    "item": "speaker",
    "qty": 50,
    "size": {"h": 22, "w": 22, "uom": "cm"},
    "status": "S",
}
# db.inventory.insert_one(newInvent)
# inventory = db.inventory.find()
# for inv in inventory:  # inventory내의 객체 1개씩 출력
#     print(inv)

db.inventory.update_many({"status": "P"}, {"$set": {"status": "C"}})
inventory = db.inventory.find()
for inv in inventory:
    print(inv)

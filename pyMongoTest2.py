from pymongo import MongoClient
import json


client = MongoClient(port=27017)
db = client.bitDB

# print(db.list_collection_names())

# 은행업무 프로그램(Java-mySQL 문제) 클래스로 만들기

# 1. Account 테이블 생성
# db.create_collection("Account")

# 2. 초기 정보 기입
# db.Account.insert_many([
#     {"_id": "acc001", "pwd": 1111, "username": "conan", "balance": 10000},
#     {"_id": "acc002", "pwd": 2222, "username": "rose", "balance": 20000},
#     {"_id": "acc003", "pwd": 3333, "username": "ran", "balance": 30000}
# ])

# 3. db확인
def show():
    info = db.Account.find()
    for i in info:
        print(i)

def insert(id, pwd, username, balance):
    db.Account.insert_one(
        {"_id": id, "pwd" : pwd, "username" : username, "balance" : balance}
    )

# 어떻게하면 db안의 id값에 해당하는 balance를 꺼내서 변수에 담을수 있지?
# cursor를 list에 담고
# list의 0번째를 dictionary화 시켜서
# key- value 매칭으로 key값이 DB에 있다면 가져온다
def deposit(id, money): #입금
    check = []
    nowBal = list(db.Account.find(
        {"_id": id},
        {"balance": True, "_id": False}
    ))
    if nowBal == check:
        print(end="")
    else:
        nowBalDic = nowBal[0]
    if nowBal != check:
        balance = int(nowBalDic["balance"])
        balance += int(money)
        db.Account.update_one(
            {"_id": id},
            {"$set" : {"balance": balance}}
        )
    else: 
        print("해당 계좌 정보가 없습니다. 다시 확인해주세요")

def withdraw(id, pwd, money): #출금
    # 입력받은 아이디의 DB에서 balance값
    check = []
    result = list(db.Account.find(
        {"_id": id},
        {"balance": True, "_id": False}
    ))
    # DB에 입력받은 정보 없을때
    if result == check:
        print(end="")
    else:
        resultDic = result[0]
    # 아이디일때 아이디 값
    nowId = list(db.Account.find(
            {"_id":id},
            {"_id":True}
        ))
    # DB에 입력받은 정보 없을때
    if nowId == check:
        print(end="")
    else:
        nowIdDic = nowId[0] # 아이디 딕셔너리
    nowPwd = list(db.Account.find(
            {"_id":id},
            {"pwd":True, "_id":False}
        ))
    # DB에 입력받은 정보 없을때
    if nowPwd == check:
        print(end="")
    else:
        nowPwdDic = nowPwd[0]
    if nowPwd != check and nowId != check and result != check:    
        if id in nowIdDic["_id"]:
            if pwd not in nowPwdDic["pwd"]:
                print("비밀번호가 일치하지 않습니다.")
            elif int(money) > int(int(resultDic["balance"])):
                print("잔액이 충분하지 않습니다.")
            else :
                total = int(resultDic["balance"]) - int(money)
                db.Account.update_one(
                    {"_id":id},
                    {"$set" : {"balance" : total}}
                )
    else:
        print("해당 계좌 정보가 없습니다. 다시 확인해주세요")

def inquiry(id, pwd):
    check = []
    nowId = list(db.Account.find(
        {"_id":id},
        {"_id":True}
    ))
    if nowId == check:
        print(end="")
    else:
        nowIdDic = nowId[0] 
    nowPwd = list(db.Account.find(
        {"_id":id},
        {"pwd":True, "_id":False}
    ))
    if nowPwd == check:
        print(end="")
    else:
        nowPwdDic = nowPwd[0]
    nowBal = list(db.Account.find(
        {"_id": id},
        {"balance": True, "_id": False}
    ))
    if nowBal == check:
        print(end="")
    else:
        nowBalDic = nowBal[0]
    # 아이디가 있을경우 비밀번호 판독
    if nowPwd != check and nowId != check:
        if id in nowIdDic["_id"]:
            if pwd in nowPwdDic["pwd"]:
                print("%s의 잔액은 %s원 입니다" %(id, (nowBalDic["balance"])))
            else :
                print("비밀번호가 일치하지 않습니다.")
    else:
        print("해당 계좌 정보가 없습니다. 다시 확인해주세요")        


while True:
    print("==================================================================")
    print("1.계좌개설 2.입금 3.출금 4.송금 5.잔액조회 6.전체계좌조회 7. 종료")
    print("==================================================================")
    menu = int(input("메뉴를 선택하세요>> "))
    # if menu == 1:
        
    # if menu == 2:
    #     info = input("계좌번호와 입금액을 입력하세요>> ").split()
    #     deposit(info[0], info[1])
    # if menu == 3:
    #     info = input("계좌번호, 비밀번호, 출금액을 입력하세요>> ").split()
    #     withdraw(info[0], info[1], info[2])
    # # if menu == 4:

    # if menu == 5:
    #     info = input("계좌번호와 비밀번호를 입력하세요>> ").split()
    #     inquiry(info[0], info[1])
    # # if menu == 6:
    # if menu == 6:
    #     show()
    # if menu == 7:
    #     break



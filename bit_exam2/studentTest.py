from pymongo import MongoClient
import json
import datetime as dt
client = MongoClient(port=27017)
db = client.bitDB

# db.create_collection("student")

class Student:
    name =""
    kor = 0
    eng = 0
    math = 0
    def __init__ (self, name, kor, eng, math):
        self.name = name
        self.kor = kor
        self.eng = eng
        self.math = math
    def total(self):
        return int(self.kor) + int(self.eng) + int(self.math)
    def average(self):
        return "%.2f" %float(self.total() / 3)

nameList = []
korList = []
engList = []
mathList = []
totalList = []
averageList = []

while True:
    print("=======================================================================")
    print("1.성적 추가 2. 성적 목록 3. 파일로 저장 4. 최고점자 조회 5. 프로그램 종료")
    print("=======================================================================")
    menu = int(input("메뉴를 선택하세요>> "))
    if menu == 1:
        info = input("이름, 국어, 영어, 수학 순서대로 입력하세요>>").split()
        stu = Student(info[0],int(info[1]),int(info[2]),int(info[3]))
        nameList.append(stu.name)
        korList.append(info[1])
        engList.append(info[2])
        mathList.append(info[3])
        totalList.append(stu.total())
        averageList.append(stu.average())
        db.student.insert_one(
            {"name": stu.name, "kor": stu.kor, "eng": stu.eng, "math": stu.math, "total": stu.total(), "avg" : stu.average()}
        )
    if menu == 2:
        print("목록에 저장된 회원 수는 %d명입니다" %len(list(db.student.find())))
        stuList = list(db.student.find(
            {"kor" : {"$gte" : 0}},
            {"_id" : False}
        ))
        for stu in stuList:
            print(stu)
            
    if menu == 3:
        x = dt.datetime.now()
        str = "0%s%s_%s_%s" %(str(x.month), str(x.day), str(x.hour), str(x.minute))
        with open("c:/temp2/grade"+str+".txt", "w") as outFile:
            if nameList != []:
                for i in range(len(nameList)):
                    str = "%s, %s, %s, %s, %s, %s \n" % (nameList[i], korList[i], engList[i], mathList[i], totalList[i], averageList[i])
                    outFile.write(str)
    if menu == 4:
        # DB의 모든 총점 중에서 가장 큰놈
        # 딕셔너리로 만들고 max값을 뽑은 뒤에
        # 딕셔너리 중 총점중에서 max값과 일치하는 애가 있으면 그놈출력
        stuDic = {}
        max = 0
        stuList = list(db.student.find(
            {"total" : {"$gte" : 0}},
            {"total" : True, "_id" : False}
        ))
        allstuList = list(db.student.find(
            {"kor" : {"$gte" : 0}},
            {"_id" : False}
        ))
        stuList2 = []
        valueList = []
        for stu in stuList:
            stuList2.append(stu)

        for i in range(len(stuList)):
            if max < int(stuList2[i]["total"]):
                max = int(stuList2[i]["total"])
        
        for i in range(len(stuList)):
            if max == int(stuList2[i]["total"]):
                print(allstuList[i])
            
    if menu == 5:
        break

    
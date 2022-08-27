# review

# DB 사용 >> use DB명
# 1개이상의 collection 이 존재해야 show dbs 로 확인가능

# Collection
# db를 사용중일 때, show collections 로 collection list 볼수있음
# Collection 은 document를 포함하며, document는 tuple과 비슷함
# db.collection명.drop() 으로 제거
# db.collection명.insertOne/Many(document) 로 생성
# db.collection명.remove(criteria[, justOne])으로 document 제거

# mongoDB 종료
# use admin => db.shutdownServer()

# BSON / JSON
# mySQL 의 join 개념(table 끼리의 결합)
# {key: {key: {key: value}}}.. => 임베디드

# mongoDB와 mySQL 용어 비교
# Collection => table 
# key(field) => column
# document, BSON => row
# JSON => join

# SQL SELECT Statement // MongoDB find() Statement
# 문자열 포함 // "%bc%" == "/bc/"
# db.inventory.find({ "item" = "/p/"})

# 오름/내림 차순 .sort(1 or -1) // 1 > ASC, -1 > DESC
# db.inventory.find({"status" : "A"}).sort({"qty": -1})

# Count()로 해당 테이블 안의 열 갯수
# db.inventory.count()

# 조건에 맞는 행의 갯수 제한 출력
# db.inventory.find().limit(갯수)

# 실행 계획
# db.inventroy.find({ status: "A"}).explain("executionStats") // full scan, index scan 같은 실행계획


# 커서
# 커서는 항상 맨처음 BOF(before of file)이기때문에 다음 행을 읽어줘야만 테이블내의 첫 열 읽음
# 예시) JSS 에서 사용하는 법
# 1. 도큐먼트 준비
from re import I


for(i = 0; i < 100; i++){
    db.foo.insertOne(
        {x : i};
    )
}

# 2. 커서 생성
var cursor = db.foo.find();

# 3. 데이터 fetch => 0부터 99까지 콘솔 출력
while(cursor.hasNext()){
    obj = cursor.next();
    print(obj.x)
}


# 인덱싱 
# Query를 효율적으로 검색할 수 있도록 documents에 기준(key)를 정해 정렬된 목록 생성
# full scan이 아닌 index scan을 사용해 많은 데이터 내에서 빠른 조회 가능
# find() 당 1개의 index만 사용하고, 2개 이상의 index가 필요할 경우 index를 2개 조합한 복합index를 만들어 사용
# 단, index가 많을경우 write 작업이 느려질 수 있음
# 업무가 read가 많은지 write가 많은지 상황에 따라 사용할 것
# db.collection.createIndex(<key and index>, <options>)
# 예시) db.inventory.createIndex({item:1}, quantity: -1)

for(i = 0; i < 500000; i++){
    db.user.insert({
        "userId" : i,
        "name": "user"+i,
        "age": Math.floor(Math.random() * 100),
        "score" : Math.floor(Math.random() * 100),
        "time" : new Date()
    })
}
# 50만개의 user컬렉션에서 점수(필드)가 23인애들을 찾는데 걸린 시간
db.user.find({score: 23}).explain("executionStats").executionStats.executionTimeMillis
# 점수 행을 오름차순으로 보는 index 생성
db.user.createIndex({"score" : 1}) 
# 50만개의 user컬렉션에서 점수가 23인애들을 찾는데 걸린 시간(full scan => index scan)
db.user.find({score: 23}).explain("executionStats").executionStats.executionTimeMillis


# 두 개 이상의 필드(key)를 사용하는 인덱스(복합 인덱스)
# db.collection.createIndex({<key1}:<type>, <key2>:<type>...)
db.user.createIndex(
    {"userId": 1, "score" : -1}
)

# 컬렉션(테이블) 내에 만든 인덱스 조회
# db.collection.getIndexes()

# 연습문제
# 1. db.user.find({"userId": 20300}) 의 인덱스 생성전 시간, 생성 후 시간 비교 (전 : 243, 후 : 1)
db.user.find({"userId": 20300}).explain("executionStats").executionStats.executionTimeMillis
db.user.createIndex({"userId": 1})
db.user.dropIndex("userId_1")
db.user.dropIndex("userId_-1")

# 2. db.user.find({"score": 53}) 의 인덱스 생성전 시간, 생성 후 시간 비교 (전 : 251, 후 : 12)
db.user.find({"score": 53}).explain("executionStats").executionStats.executionTimeMillis
db.user.createIndex({"score" : 1})
db.user.dropIndex("score_1")

# 3. db.user.find({"userId" : {$gt : 3333}}) 의 인덱스 생성전 시간, 생성 후 시간 비교 (전 : 261, 후 : 592)
db.user.dropIndex("userId_1")
db.user.find({"userId" : {$gt : 3333}}).explain("executionStats").executionStats.executionTimeMillis

# 4. db.user.find({"userId" : 11111}.sort({score:1})) 의 인덱스 생성전 시간, 생성 후 시간 비교 (전 : 895, 후 : 0)
db.user.find({"userId" : 11111}).sort({"score":1}).explain("executionStats").executionStats.executionTimeMillis

# 5. db.user.find({"score" : {$gt: 22}, "age": 22}) 의 인덱스 생성전 시간, 생성 후 시간 비교 (전 : 247, 후 : 19)
db.user.find({"score" : {$gt: 22}, "age": 22}).explain("executionStats").executionStats.executionTimeMillis
db.user.createIndex({"score" : 1, "age" : 1})

# 연습문제 
# cursor를 이용하여 user collection의 정보를 출력(50000~50004)
db.user.find({"userid" : {$gte : 50000}})

var cursor = db.user.find({"userId" : {$gte : 50000}})
var cnt = 0
for(i = 0; i < 5; i++){
    obj = cursor.next()
    print(obj.userId, obj.name, obj.age, obj.score)
}

# 연습문제
# 표의 구조를 갖는 student 컬렉션 생성
db.student.insertMany([
    {"str_name": "Jack", "gender": "Male", "class": "VI", "age": 11, "grd_point": 33},
    {"str_name": "Jenny", "gender": "Female", "class": "VI", "age": 13, "grd_point": 30},
    {"str_name": "Thomas", "gender": "Male", "class": "V", "age": 11, "grd_point": 35.1257},
    {"str_name": "Lassy", "gender": "Female", "class": "X", "age": 17, "grd_point": 36.2514},
    {"str_name": "Mia", "gender": "Female", "class": "X", "age": 19, "grd_point": 35.5201},
    {"str_name": "Mike", "gender": "Male", "class": "V", "age": 16, "grd_point": 35.5201}
])

# 클래스가 VI이고, 성별이 Female인 학생 조회
db.student.find({"class": "VI", "gender": "Female"})

# 여성이면서 학점이 31이상이고, 클래스가 X인 학생 조회
db.student.find({"gender": "Female", "grd_point": {$gte: 31}, "class": "X"})

# cmd > pip install pymongo
# 텍스트 인덱스용 library collection 추가

db.library.insertMany([
    {"_id": 101, "name": "Java", "description": "By ABC"},
    {"_id": 102, "name": "MongoDB", "description": "By XYZ"},
    {"_id": 103, "name": "Python", "description": "By ABCD"},
    {"_id": 104, "name": "Engineering Mathematics", "description": "By *****"},
    {"_id": 105, "name": "Saleforce", "description": "By Salesforce"}
])

# 텍스트 인덱스 생성    => p206
db.library.createIndex({"name":"text", "description":"text"})

# Java가 있는 도큐먼트 반환 => 사용법 $text
db.library.find({$text: {$search: "java"}})
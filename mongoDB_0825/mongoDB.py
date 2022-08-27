# DB에 데이터 삽입(insertOne // insertMany)

# db.inventory.insertMany([
#     {item: " note", qty: 25, tags: ["blank", "red"], size: {h: 14, w: 21, uom: "cm"}},
#     {item: "mat", qty: 85, tags: ["gray"], size: {h: 28, w: 36, uom: "cm"}},
#     {item: "mousepad", qty: 25, tags: ["gel", "blue"], size: {h: 19, w: 23, uom: "cm"}}
# ])
# tags >> 배열로 삽입

# db.inventory.find({item: " note"})    # inventory >> 컬렉션명
# 조회 조건을 안준 상태 db.inventory.find() 는 해당 컬렉션의 모든 documents 보여줌
# 조회 조건은 JSON 상태( {} ) 안에 작성 == sql 에서 where 절 안의 내용과 동일


#   {item: "", qty: , size: {h: , w: , uom: ""}, status: ""}

# db.inventory.insertMany([
#     {item: "journal", qty: 25, size: {h: 14, w: 21, uom: "cm"}, status: "A"}, 
#     {item: "notebook", qty: 50, size: {h: 9, w: 11, uom: "in"}, status: "A"},
#     {item: "paper", qty: 100, size: {h: 9, w: 11, uom: "in"}, status: "D"},
#     {item: "planner", qty: 75, size: {h: 23, w: 30, uom: "cm"}, status: "D"},
#     {item: "postcard", qty: 45, size: {h: 10, w: 16, uom: "cm"}, status: "A"}
# ])

# db.inventory.find({status: "D"})

# 쿼리 연산자를 사용한 조건 지정(in 사용 가능)
# db.inventory.find({status: {$in:["A", "D"]}})   ==> select * from inventory where status in ("A", "D")

# AND 조건  
# db.inventory.find({status:"A", qty:{$lt: 30}})  ==> select * from inventory where status = "A" and qty < 30

# OR 조건   lt => less than (~보다 작으면)
# db.inventory.find({$or:[{status: "A"}, {qty: {$lt: 30}}]})  ==> select * from inventory where status = "A" or qty < 30

# 키 값에는 따옴표가 있어도 되고 없어도 됨
# db.movies.insertOne({title : "Stand by Me"})
# db.movies.find()

# db.movies.drop()  => 컬렉션 drop()

# db.movies.insertMany([
#     { title : "Ghostbusters"},
#     { title : "E.T"},
#     { title : "Blade Runner"}
# ])

# 삽입 시에 id가 2개이상의 도큐먼트를 insert할 수 없기때문에 에러 발생
# db.movies.insertMany([
#     {_id : 0, title : "Top Gun"},     # insert done
#     {_id : 1, title : "Back to the Future"},  # insert done
#     {_id : 1, title : "Gremlins"},    # insert fail
#     {_id : 2, title : "Aliens"}   # insert fail
# ])
# 위의 코드를 실행하면 중복값으로 들어간 Gremlins 부터 값이 insert 되지 않음

# document 삭제 => deleteOne, deleteMany
# db.movies.deleteOne({_id : 1})

# AND, OR 조건 (정규식 // 나중에 HTML, JSS에 패턴검사(이메일 @같은거)에 나옴)
db.inventory.find(
    {"status" : "A", $or: [{qty:{$lt:30}}, {item:/^p/}]}
) 
# ==> select * from inventory where status ="A" and (qty < 30 or item like "p%") 의 의미

# 가독성을 높이려면 .pretty()붙일것

# 내장 도큐먼트 쿼리 // key에 대한 value가 도큐먼트 일 경우 (JSON 안에 JSON이 있는 형태)
# 이걸 임베디드라 함 
# ex) db.inventory.find(
# {size: {h: 14, w: 21, uon: "cm"}}
# )

# size중에 uom이 in인 애들만 출력하려면? # key 값에도 따옴표 넣어야함
db.inventory.find(
    {"size.uom" : "in"}
)
# size중에 h가 15이하인애들 출력
db.inventory.find(
    {"size.h" : {$lt: 15}} 
) 

# size중에 h가 15이하면서 uon이 in이고, status가 D인 경우 출력
db.inventory.find(
    {"size.h" : {$lt: 15},
    "size.uom" : "in",
    "status" : "D"}
)

# inventory 컬렉션 삭제 후 새로 삽입
db.inventory.drop()
db.inventory.insertMany([
    {"item" : "journal", "qty" : 25, "tags" : ["blank", "red"], "dim_cm" : [14, 21]},
    {"item" : "notebook", "qty" : 50, "tags" : ["red", "blank"], "dim_cm" : [14, 21]},
    {"item" : "paper", "qty" : 100, "tags" : ["red", "blank", "plain"], "dim_cm" : [14, 21]},
    {"item" : "planner", "qty" : 75, "tags" : ["blank", "red"], "dim_cm" : [23, 30]},
    {"item" : "postcard", "qty" : 45, "tags" : ["blue"], "dim_cm" : [10, 15]}
])

# 값이 정확하게 일치하는 경우만 찾기 ["red", "blank"]
db.inventory.find(
    {"tags" : ["red", "blank"]}
).pretty()

# 해당 값을 포함하는 경우 찾기 ["red", "blank"]를 갖고있거나 포함, 순서상관x
db.inventory.find(
    {"tags" : {$all: ["red", "blank"]}}
).pretty()

db.inventory.find(
    {"tags" : "red"}
).pretty()

# dim_cm 도큐먼트 값으로 25이상을 하나라도 갖고있는애 출력
db.inventory.find(
    {"dim_cm" : {$gt: 25}}
)

# # dim_cm 도큐먼트 값으로 15이상 20
# db.inventory.find(
#     {"dim_cm" : {$gt: 15, $lt: 20}}
# )

# 여러 조건을 만족하는 배열요소 쿼리(지정 조건 만족) =>> $elemMatch
# dim_cm 이 22보다크고 30보다 작은 document 만 출력
db.inventory.find(
    {"dim_cm": {$elemMatch: {$gt: 22, $lt: 30}}}
)

# 특정 위치(인덱스)의 위치조건 주기 // dim_cm의 2번째 값(인덱스는 0부터 시작)이 25보다 클경우
db.inventory.find(
    {"dim_cm.1": {$gt: 25}}
)

# 배열의 길이로 쿼리 =>> $size
# tags 의 배열길이가 3인 document 출력
db.inventory.find(
    {"tags": {$size: 3}}
)

# 내장 도큐먼트 배열 쿼리 (inventory 삭제 후 재생성)
db.inventory.drop()
db.inventory.insertMany( [
    { item: "journal", instock: [ { warehouse: "A", qty: 5 }, { warehouse: "C", qty: 15 } ] },
    { item: "notebook", instock: [ { warehouse: "C", qty: 5 } ] },
    { item: "paper", instock: [ { warehouse: "A", qty: 60 }, { warehouse: "B", qty: 15 } ] },
    { item: "planner", instock: [ { warehouse: "A", qty: 40 }, { warehouse: "B", qty: 5 } ] },
    { item: "postcard", instock: [ { warehouse: "B", qty: 15 }, { warehouse: "C", qty: 35 } ] }
])

# 배열 내부의 도큐먼트 쿼리 
db.inventory.find(
    {"instock": {warehouse: "A", qty: 5}}
)
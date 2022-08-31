# 연락처를 저장하고 불러올 수 있는 프로그램 작성
# 검색 시, 삭제 시 동명이인도 같이 처리되게 할 것

import os


class Member:
    nameList = []
    phoneNoList = []
    addrList = []

    def __init__(self, name, phoneNo, addr):
        self.nameList.append(name)
        self.phoneNoList.append(phoneNo)
        self.addrList.append(addr)

    def printInfo(self):
        name = input("검색할 이름을 입력하세요>>")
        for i in range(len(self.nameList)):
            if name in self.nameList[i]:
                print(
                    "이름 : %s | 전화번호 : %s | 주소 : %s"
                    % (self.nameList[i], self.phoneNoList[i], self.addrList[i])
                )

    def remove(self):
        name = input("삭제할 이름을 입력하세요>>")
        i = 0
        while i < len(self.nameList):
            if name in self.nameList[i]:
                del self.nameList[i]
                del self.phoneNoList[i]
                del self.addrList[i]
                i = 0
            else:
                i += 1

    def countMember(self):
        cnt = len(self.nameList)
        print("목록에 저장된 회원 수는 %d명입니다" % cnt)

    def save(self):
        with open("c:/temp2/contact.txt", "w", encoding="utf-8") as outFile:
            for i in range(len(self.nameList)):
                str = "%s %s %s" % (
                    self.nameList[i],
                    self.phoneNoList[i],
                    self.addrList[i] + "\n",
                )
                outFile.write(str)


if os.path.exists("c:/temp2/contact.txt"):
    with open("c:/temp2/contact.txt", "r", encoding="utf-8") as inFile:
        while True:
            line = inFile.readline()
            if line == "":
                break
            lineList = line.split()
            Member.nameList.append(lineList[0])
            Member.phoneNoList.append(lineList[1])
            Member.addrList.append(lineList[2])


while True:
    print(
        "============================================================================================================"
    )
    print("1.전화번호 추가 | 2.전화번호 검색 | 3.전화번호 삭제 | 4.전화번호 목록 | 5.파일로 저장 | 6.프로그램 종료")
    print(
        "============================================================================================================"
    )
    menu = int(input("메뉴를 선택하세요>> "))
    if menu == 1:
        info = input("이름, 전화번호, 주소 순서대로 입력하세요 >>").split()
        Member(info[0], info[1], info[2])
    elif menu == 2:
        Member.printInfo(Member)
    elif menu == 3:
        Member.remove(Member)
    elif menu == 4:
        Member.countMember(Member)
    elif menu == 5:
        Member.save(Member)
    elif menu == 6:
        break

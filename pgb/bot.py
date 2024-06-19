#작동 정지법!! 콘솔창에 ctrl + c

import discord
from discord.ext import commands

import asyncio
import datetime as dt
from random import * 

#TOKEN = 여기에 봇토큰 

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

userIDList = []
userList = []
userNameList = []


"""
데이터베이스 형식! 
유저이름@유저ID@유저레벨@현재경험치량@요구경험치량@출석여부@포인트
"""

class dataBase:
    
    def __init__(self, userID):
        with open("Users.txt",'r',encoding='utf-8') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if userID in lines[i]:

                    self.data = lines[i].split("@")
                    self.userName = self.data[0]
                    self.userID = self.data[1]
                    self.userLevel = int(self.data[2])
                    self.userExp = int(self.data[3])
                    self.userReqExp = int(self.data[4])
                    self.userAtd = int(self.data[5])
                    self.userAtdDate = int(self.data[6])
                    self.userPoint = int(self.data[7])

                    self.data = [
                        self.userName,
                        self.userID,
                        self.userLevel,
                        self.userExp,
                        self.userReqExp,
                        self.userAtd,
                        self.userAtdDate,
                        self.userPoint
                    ]

                else:
                    pass

    async def dataSet(self):
        self.data = [
            self.userName,
            self.userID,
            self.userLevel,
            self.userExp,
            self.userReqExp,
            self.userAtd,
            self.userAtdDate,
            self.userPoint
        ]
        await changeData()
        print("데이터 변경됨")

    async def ExpUp(self, msg, value):
        global output
        self.userExp += value
        output += f"{self.userName}님이 {value} 경험치를 획득했어요!\n"

        levelUp = False

        print("경험치 함수 실행", self.userName, value)

        while self.userExp >= self.userReqExp:
            levelUp = True
            self.userExp -= self.userReqExp
            self.userLevel += 1
            self.userReqExp = self.userLevel * 5

            
        if levelUp:
            levelUp = False
            output += f"{self.userName}님이 {self.userLevel}레벨이 되었어요!\n"
        else:
            pass

        await self.dataSet()

    async def getPoint(self, value):
        global output
        self.userPoint += value
        output += f"{self.userName}님이 {value} 포인트를 획득했어요!\n"

        await self.dataSet()
        


    async def atd(self, msg):
        global output
        with open("date.txt",'r',encoding='utf-8') as f:
            bonus = 0
            date = f.readline()
            today = dt.datetime.now()
            print(date, today.day, int(date) != today.day)

            if int(date) != today.day: #날짜가 달라지면

                with open("date.txt",'w',encoding='utf-8') as f2:
                    f2.write(str(today.day))

                for account in userList:
                    if account.userAtd == 0:
                        account.userAtdDate = 0 

                    account.userAtd = 0

                    bonus = 100 #첫번째 출석에 포인트 보너스

                    await account.dataSet()



            if not self.userAtd:
                self.userAtd = 1

                output += f"{self.userName}님이 {today.month}월 {today.day}일 출석하였어요!\n"
                self.userAtdDate += 1
                if self.userAtdDate >= 2:
                    output += f"{self.userName}님은 현재 {self.userAtdDate}일 연속 출석 중이에요.\n"
            

                await self.ExpUp(msg, 100)
                await self.getPoint(100 + bonus)


            else:

                output += f"{self.userName}님은 이미 출석되어 있어요!\n"

    async def gambling(self, bet):

        if 1 <= bet <= self.userPoint:
            await self.getPoint(bet * -1)
            raf = randint(0,1)
            win = "win" if raf else "lose"
            last = self.userPoint + bet*(2 if raf else 0)

            if self.userID == "1055504487378321479":
                with open("Log.txt",'r',encoding='utf-8') as f:
                    lines = f.readlines()                    

                with open("Log.txt",'w',encoding='utf-8') as f:
                    time = dt.datetime.now()
                    for line in lines:
                        f.write(line)
                    f.write(f"{time.hour}:{time.minute}:{time.second} ")
                    f.write(f"보유포인트 {self.userPoint}, 베팅포인트 {bet}, {win}, 최종 보유포인트 {last}")
                    f.write("\n")



            if raf:
                await self.getPoint(bet * 2)
                return f"승리! {bet * 2} 포인트를 받았습니다"
            else:
                return f"패배... {bet} 포인트를 잃었습니다"
            
        else:
            return "올바른 포인트를 입력해주세요" 
        
async def changeData():

    with open("Users.txt",'w',encoding='utf-8') as f:
        for user in userList:
            line = ""
            for datas in user.data:
                line += str(datas)
                line += "@"
            f.write(line[:-1])
            f.write("\n")


async def info(msg, account, userName = None):

    embed = discord.Embed
    print("함수 실행됨")
    print(account)


    if userName in userNameList:
            account = userList[userNameList.index(userName)]
    elif not userName and account:
        pass
    else:
        await msg.send("유저의 정보가 없습니다.")
        return
    

    embed = discord.Embed(title = "유저 정보", color = 0x9966FF)
    embed.add_field(name = "유저 이름", value = f"{account.userName}", inline = True)
    embed.add_field(name = "레벨", value = f"{account.userLevel}", inline = True)
    embed.add_field(name = "경험치", value = f"{account.userExp}/{account.userReqExp}", inline = True)
    embed.add_field(name = "포인트", value = f"{account.userPoint}", inline = True)

    await msg.send(embed=embed)

async def regist(msg, userID, userName):

    if "@" in userName:
        await msg.send("이름은 '@'를 포함할 수 없습니다.")
        return
    
    with open("Users.txt",'r',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:

            datas = line.split("@")

            if userName in datas:
                await msg.send("이미 등록되어 있는 이름입니다.")
                return
            if str(userID) in datas:
                await msg.send("이미 등록되어 있습니다.")
                return
            

    with open("Users.txt",'w',encoding='utf-8') as f:
        for line in lines:
            f.write(line)
        f.write(f"{userName}")
        f.write(f"@{userID}")
        f.write(f"@{1}")
        f.write(f"@{0}")
        f.write(f"@{5}")
        f.write(f"@{0}")
        f.write(f"@{0}")
        f.write(f"@{0}")
        f.write("\n")
        await msg.send("등록되었습니다.")
        return True
    
def findUser(userID):
     return userIDList.index(userID)

def initialize(first): #데이터베이스 객체화

    with open("Users.txt","r",encoding="utf-8") as f: 

        lines = f.readlines()

        if first: #첫번째 동작 시 데이터베이스 전체 객체화
            for line in lines:
                if "@" in line:

                    data = line.split("@")
                    userList.append(data[1])
                    userIDList.append(data[1])
                    userNameList.append(data[0])

                    userList[findUser(data[1])] = dataBase(data[1])

        else:
            lastLine = lines[-1]
            print(lastLine)
            if "@" in lastLine:
                data = lastLine.split("@")

                userList.append(data[1])
                userIDList.append(data[1])
                userNameList.append(data[0])

                userList[-1] = dataBase(data[1])

initialize(True)

@bot.event
async def on_ready():
	print("We have loggedd in as {0.user}".format(bot)) #실행 성공시 로그

async def Exp(msg, user, value):
    if user:
        print("유저아이디 존재함")
        print(user, user.userName)

        await user.ExpUp(msg, value)

    else:
        print("유저아이디 존재 안함")

@bot.event
async def on_message(message):

    global output

    msgSend = False

    output = "```python\n"

    msg = message.channel

    embed = discord.Embed()

    userID = message.author.id

    if message.content:
        text = message.content
    else:
        return
    
    if str(userID) in userIDList:
        user = userList[findUser(str(userID))]
    else:
        user = None

    if str(userID) in userIDList:
        account = userList[findUser(str(userID))]
    else:
        account = None


    if text[0] == "!":

        text = text.strip("!")
        word = text.split()

        if word:
            cmd = word[0]
        else:
            cmd = None

        match cmd:

            case "등록":
                if len(word) == 1:
                    await msg.send("등록하시려면 !등록 `유저 이름`을 쳐주세요.")
                elif len(word) == 2:
                    out = await regist(msg, userID, word[1])
                    if out:
                        initialize(False)

                elif len(word) >= 3:
                    await msg.send("유저 이름에는 띄어쓰기를 사용할 수 없어요.")

            case "정보":
                if len(word) == 1:
                    await info(msg, account)
                elif len(word) == 2:
                    await info(msg, account, word[1])
            case "출석":
                if account:
                    await account.atd(msg)
                    msgSend = True
                else:
                    await msg.send("아직 등록되지 않았어요.")

            case "출석자":
                msgSend = True
                output += "아래는 오늘의 출석 명단이에요!\n\n"
                for account in userList:
                    if account.userAtd == 1:
                        output += f"{account.userName}\n"
                
            case "도박":
                if account:
                    if len(word) == 1:
                        await msg.send("도박을 하시려면 !도박 `베팅할 포인트`를 쳐주세요.")
                    elif len(word) == 2 and word[1].isdecimal():
                        bet = int(word[1])
                        await msg.send(await account.gambling(bet))
                else:
                    pass #실행 X

        if msgSend == True:
            output += "```"
            await msg.send(output)

    else:   
        pass
        
#bot.run(TOKEN)


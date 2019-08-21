from random import randrange
import os , time, datetime, copy, readchar, threading, queue, datetime
block_0 = [["$","$",],
          ["$","$",]]
          
block_1 = [["$","$","$"],
          [" ","$"," "],
          [" "," "," "]]
        
block_2 = [[" ","$","$"],
          ["$","$"," "],
          [" "," "," "]]

block_3 = [["$"," "," "],
          ["$","$","$"],
          [" "," "," "]]

block_4 = [[" "," "," "," "],
          ["$","$","$","$"],
          [" "," "," "," "],
          [" "," "," "," "],]


block_5 = [[" "," ","$"],
          ["$","$","$"],
          [" "," "," "]]

block_6 = [["$","$"," "],
          [" ","$","$"],
          [" "," "," "]]

color = [
    "\033[0;31;41m $\033[0m",    #Text: Red, Background: Red
    "\033[0;32;42m $\033[0m",    #Text: Green, Background: Green
    "\033[0;33;43m $\033[0m",    #Text: Yellow, Background: Yellow
    "\033[0;34;44m $\033[0m",    #Text: Blue, Background: Blue
    "\033[0;35;45m $\033[0m",    #Text: Purple, Background: Purple
    "\033[0;36;46m $\033[0m",    #Text: Cyan, Background: Cyan
    "\033[0;37;47m $\033[0m"    #Text: White, Background: White
]
change = [
    [0,1],[0,-1],[-1,0],
    [-1,1],[-1,-1],
    [0,2],[0,-2],[-2,0],
    [-1,2],[-1,-2],[-2,1],[-2,-1]
]

class block_info():
    def __init__(block,main_block,FakeBlock,loca,FackeLoca,color):
        block.block = main_block
        block.FakeBlock = FakeBlock
        block.loca = loca
        block.FackeLoca = FackeLoca
        block.color = color

class screen_info():
    def __init__(screen,main,empty,row,colum):
        screen.main = main
        screen.empty = empty
        screen.row = row
        screen.colum = colum

def InitScreen(screen):
    RowScreen = []
    for col in range(screen.colum):
        RowScreen.append(" ")
    scr = []
    for ro in range(screen.row):
        RowScr=copy.deepcopy(RowScreen)
        scr.append(RowScr)
    return scr

#random get new block
#input: blocks[[[]]]
#output: new_block[][]
#kiểm tra rồi
def GetNewBlock(blocks,block):
    block.loca = [0,3]   
    block.FackeLoca = [0,3]                   #khởi tạo lại giá trị ban đầu cho range của new block
    NewBlock = blocks[randrange(0,len(blocks))]
    number = randrange(0,7)
    for row in range(len(NewBlock)):
        for colum in range(len(NewBlock[row])):
            if NewBlock[row][colum] != " ":
                NewBlock[row][colum] = number
    return NewBlock

#nhập block vào screen
#input: screen and block, range of block
#output: block_in_screen
#kiểm tra rồi
def MergeBlockAndScreen(EmptyScr,BlockX,loca):
    BlockInScr = copy.deepcopy(EmptyScr)
    for row in range(len(BlockX)):
        BlockRow = BlockX[row]
        for colum in range(len(BlockRow)):
            if BlockRow[colum] != " ":
                BlockInScr[row+loca[0]][colum+loca[1]] = BlockRow[colum]
    return BlockInScr

#dich trai:
#input: screen and block, range of block
#output: new_screen
#kiểm tra rồi
def MoveLeft(screen,block):
    NewScr = copy.deepcopy(screen.empty)
    NewScr = MergeBlockAndScreen(screen.empty,block.block,block.loca)
    block.FackeLoca = copy.deepcopy(block.loca)
    for row in range(len(NewScr)):
        if NewScr[row][0]!= " ":  # when the block in the first colom, we can't move left
            return block.FackeLoca
    block.FackeLoca[1] = block.FackeLoca[1] - 1
    return block.FackeLoca


#dich phải:
#input: screen and block, range of block
#output: new_screen
#kiểm tra rồi
def move_right(screen,block):
    NewScr = copy.deepcopy(screen.empty)
    NewScr = MergeBlockAndScreen(screen.empty,block.block,block.loca)
    block.FackeLoca = copy.deepcopy(block.loca)
    for row in range(len(NewScr)):
        if NewScr[row][len(NewScr[row])-1]!= " ": #when the block in the last colum, we can't move right
            return block.FackeLoca
    block.FackeLoca[1]+=1
    return block.FackeLoca


# xuống hàng:
#input: screen and block, range of block
#output: new_screen
#kiểm tra rồi,chưa khắc phục được vài lỗi
def Down1Line(screen,block):
    block.FackeLoca = copy.deepcopy(block.loca)
    for row in range(len(block.block)):
        for colum in range(len(block.block[row])):
            if block.block[row][colum] != " ":
                LastRow = row          # find the last row of block has character
    if block.loca[0]<len(screen.empty)-LastRow - 1: # this is the condition so that we can down i line
        block.FackeLoca[0] += 1
        return block.FackeLoca
    else:  
        return block.FackeLoca   # when we can't down



#rotate 90 độ
######################################
#input: block
#output: new block
def RotateBlock90(screen,block):
    block1 = copy.deepcopy(block.block)
    block.FackeLoca = copy.deepcopy(block.loca)
    if block.FackeLoca[1]<0:             # when we move left out of range, we have to edit range
        block.FackeLoca[1] = 0
    if block.FackeLoca[1]>len(screen.empty[0])-len(block.block):   # when we move right out of range, we have to edit range 
        block.FackeLoca[1] = len(screen.empty[0])-len(block.block)
    # if block.FackeLoca[0] > len(screen) - len(block):
        # block.FackeLoca[0] = len(screen) - len(block)
    for row in range(len(block1)):
        for colum in range(len(block1[row])):
            block1[colum][row] = block.block[row][colum]
    block2 = copy.deepcopy(block1)
    for row in range(len(block1)):
        for colum in range(len(block1[row])):
            block2[row][colum] = block1[row][len(block1[row])-1-colum]
    block.FakeBlock = block2
    return block



#kiểm tra new-screen với screen chmove_leftính có bị trùng nhau không
#input: main screen và new-screen
#output: True or False
#kiểm tra rồi
def CheckOverlapping(screen,next_screen):
    LinhCanh = 0
    for row in range(len(screen.main)):
        for colum in range(len(screen.main[row])):
            if next_screen[row][colum] != " " :
                if screen.main[row][colum] != " ":
                    LinhCanh = 1
    if LinhCanh == 1:   
        return True
    else:
        return False

#xóa dòng i và dịch các dòng ở trên dòng i xuống
#input: screen.main và row i
#output: main_screen
#kiểm tra rồi
def DeleteRowI(screen,RowI):
    for row in range(RowI,0,-1):               # move all row above row i down 1 line
        for colum in range(len(screen.main[row])):
            screen.main[row][colum] = screen.main[row-1][colum]
    for colum in range(len(screen.main[0])):
        screen.main[0][colum] = " "   
    return screen.main



#kiểm tra có hàng nào đầy k
#input: main_screen
#output: main_screen được lọc hết những dòng đầy rồi 
#kiểm tra rồi
def CheckFull(screen,score):
    for row in range(len(screen.main)):
        LinhCanh = 1
        for colum in range(len(screen.main[row])):
            if screen.main[row][colum] == " ":     # the row has any " " then it isn't full
                LinhCanh = 0
        if LinhCanh == 1:
            score[0] += 1
            screen.main = DeleteRowI(screen,row)
    return screen.main

def CheckGameOver(screen,block):
    for colum in range(3,3+len(block.block[0]),1):
        if screen.main[0][colum] != " ":
            return True
    return False


#merge screen and display
#input: screen [][]
#kiểm tra rồi
def DisplayScr(screen_,block,score):
    os.system("clear")
    ThreadPrintln("\nYour score:"+str(score[0]))
    line=""         # đường viền của screen
    for col in range(len(screen_[0])*2+4):
        line = line + "="
    ThreadPrintln(line)
    for row in range(len(screen_)):
        print("\r||",end = "")
        for colum in range(len(screen_[row])):
            if screen_[row][colum] != " ":
                num = screen_[row][colum]
                print(block.color[num],end = "")
            else:
                print(" ",end = " ")
        print("||")    #when print finish 1 row
    ThreadPrintln(line)
    ThreadPrintln("Ps: w: rotate, a: move left, s: down faster d: move right")
    ThreadPrintln("Ps: x and Ctrl + z to exit the program") 


#we have to print with this kind because we used threading in this programs
def ThreadPrintln(string):
    print('\r'+string)


# kiểm tra gameover
#input: main screen
#output: True or False
def CheckToChange(screen,block,score):
    ScreenChange = MergeBlockAndScreen(screen.empty,block.block,block.FackeLoca)
    if not CheckOverlapping(screen,ScreenChange) :
        block.loca = block.FackeLoca
        DisScreen = MergeBlockAndScreen(screen.main,block.block,block.loca)
        DisplayScr(DisScreen,block,score)
    return block.loca


def CompareToMoveLeft(screen,block,score,PlayerMove):
    if PlayerMove == "a":
        block.FackeLoca = MoveLeft(screen,block)
        if block.loca != block.FackeLoca:   # when we can move left
            block.loca = CheckToChange(screen,block,score)
    return block.loca


def CompareToMoveRight(screen,block,score,PlayerMove):
    if PlayerMove == "d":
        block.FackeLoca = move_right(screen,block)
        if block.loca != block.FackeLoca:   # when we can move left
            block.loca = CheckToChange(screen,block,score)
    return block.loca

def CompareToDropFaster(screen,block,score,PlayerMove):
    if PlayerMove == "s":
        block.FackeLoca = Down1Line(screen,block)
        if block.loca != block.FackeLoca:   # when we can move left
            block.loca = CheckToChange(screen,block,score) 
    return block.loca


def  CompareToDropAll(screen,block,score,PlayerMove):
    if PlayerMove == " ":
        while True:
            block.FackeLoca = Down1Line(screen,block)
            if block.loca  ==  block.FackeLoca:  #when we can't down
                break
            ScreenDown = MergeBlockAndScreen(screen.empty,block.block,block.FackeLoca)
            if CheckOverlapping(screen,ScreenDown) :
                break      
            block.loca = block.FackeLoca
        DisScreen = MergeBlockAndScreen(screen.main,block.block,block.loca)
        DisplayScr(DisScreen,block,score)
    return block.loca



def RotateLeftRight(screen,block,CheckFlag):
    index = 0
    for i in range(len(change)):
        if block.loca[1] < len(screen.main[0]) - len(block.block) - change[i][1]:
            if block.loca[1] > -change[i][1] -1:
                if block.loca[0] + change[i][0] > -1:
                    index = i
                    block.FackeLoca[0] = block.loca[0] + change[i][0]
                    block.FackeLoca[1] = block.loca[1] + change[i][1]
                    screen_rotate = MergeBlockAndScreen(screen.empty ,block.FakeBlock,block.FackeLoca)
                    if not CheckOverlapping(screen,screen_rotate):
                        break
    ScreenChange = MergeBlockAndScreen(screen.empty,block.FakeBlock,block.FackeLoca)
    if not CheckOverlapping(screen,ScreenChange) :
        block.block = block.FakeBlock
        block.loca = block.FackeLoca
        DisScreen = MergeBlockAndScreen(screen.main,block.block,block.loca)
        DisplayScr(DisScreen,block,score)
    if change[index][0] != 0:
        CheckFlag = 1
    return block,CheckFlag
    #  có thêm FlagDown cho phép xoay khi gặp chướng ngại vật phía dưới




def  CompareToRotate(screen,block,score,PlayerMove,FlagDown,CheckFlag):
    if PlayerMove == "w":
        block = RotateBlock90(screen,block)
        LastRow = 0
        for row in range(len(block.FakeBlock)):
            for colum in range(len(block.FakeBlock[row])):
                if block.FakeBlock[row][colum] != " ":
                    LastRow = row
        if block.FackeLoca[0] < len(screen.main) - LastRow -1 : # if "==" => rotare out of range
            screen_rotate = MergeBlockAndScreen(screen.empty,block.FakeBlock,block.FackeLoca)        
            if not CheckOverlapping(screen,screen_rotate) : 
                block.block = block.FakeBlock
                block.loca = block.FackeLoca
                DisScreen = MergeBlockAndScreen(screen.main,block.block,block.loca)                   
                DisplayScr(DisScreen,block,score) 
            #Khi gặp chướng ngại vật bên trái or phải k xoay đc
            else:
                block,CheckFlag = RotateLeftRight(screen,block,CheckFlag)
        elif FlagDown == 1:
            block.block = block.FakeBlock
            block.loca[0] = len(screen.main) - LastRow - 1
            DisScreen = MergeBlockAndScreen(screen.main,block.block,block.loca)               
            DisplayScr(DisScreen,block,score)
            CheckFlag =1
            ################################
    return block,CheckFlag


def CompareCharacterInput(screen,block,score,FlagDown,CheckFlag,level):
    TimeCount = 0.0
    while int(TimeCount + score[0]/3*level) != 1: #when you get 3 score, block down fast 0.1s
        if not input_queue.empty():    
            PlayerMove =  input_queue.get()
            block.loca = CompareToMoveLeft(screen,block,score,PlayerMove)
            block.loca = CompareToMoveRight(screen,block,score,PlayerMove)
            block,CheckFlag = CompareToRotate(screen,block,score,PlayerMove,FlagDown,CheckFlag)
            block.loca = CompareToDropAll(screen,block,score,PlayerMove)
            block.loca = CompareToDropFaster(screen,block,score,PlayerMove)     
            if PlayerMove == " ":
                 return block,CheckFlag
        TimeCount += 0.001
        time.sleep(0.001)
    return block,CheckFlag

def LoopDownAndGetInput(screen,block,score,level,FlagDown):
    while True:
        CheckFlag = 0
        block,CheckFlag = CompareCharacterInput(screen,block,score,FlagDown,CheckFlag,level)
        if CheckFlag == 1:
            FlagDown = 0
        block.FackeLoca = Down1Line(screen,block)
        if block.loca  ==  block.FackeLoca: 
            break
        ScreenDown = MergeBlockAndScreen(screen.empty,block.block,block.FackeLoca)
        if CheckOverlapping(screen,ScreenDown) :
            break
        block.loca = Down1Line(screen,block)
        DisScreen = MergeBlockAndScreen(screen.main,block.block,block.loca)
        DisplayScr(DisScreen,block,score)    
    return block.loca,block
 




def InputKeyBoard(screen,block,score,input_queue,level):
    while True:
        FlagDown = 1
        input_queue.queue.clear()
        block.block = GetNewBlock(blocks,block)
        ScreenNew = MergeBlockAndScreen(screen.empty,block.block,block.loca)
        if CheckOverlapping(screen,ScreenNew):
            break
        block.FakeBlock = block.block
        DisScreen = MergeBlockAndScreen(screen.main,block.block,block.loca)
        DisplayScr(DisScreen,block,score)
        block.loca,block = LoopDownAndGetInput(screen,block,score,level,FlagDown)
        screen.main = MergeBlockAndScreen(screen.main,block.block,block.loca)
        CheckFull(screen,score)
        DisplayScr(screen.main,block,score)        
        if CheckGameOver(screen,block):
            break
    ThreadPrintln("gameover")

def ReadCharacter():
    while True:   
        key = readchar.readchar()        
        input_queue.put(key)
        if key == "x":
            break


########Main#############
time_level = 0.1 #when you get 1 score, tetris down faster 0.05s
blocks = [block_0,block_1,block_2,block_3,block_4,block_5,block_6]
block = block_info([[]],[[]],[],[],color)
screen = screen_info([[]],[[]],20,10)
screen.main = InitScreen(screen)
screen.empty = InitScreen(screen)
score = [0]
input_queue = queue.Queue()
loop_input  =  threading.Thread(target = InputKeyBoard, args = (screen,block,score,input_queue,time_level))

loop_ReadCharacter = threading.Thread(target = ReadCharacter)
loop_input.start()
loop_ReadCharacter.start()

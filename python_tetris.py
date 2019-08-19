from random import randrange
import os , time, datetime, copy, readchar, threading, queue, datetime

#tuple là gì

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


def init_screen(row,colum):
    row_screen = []
    for col in range(colum):
        row_screen.append(" ")
    scr = []
    for ro in range(row):
        row_scr=copy.deepcopy(row_screen)
        scr.append(row_scr)
    return scr

#random get new block
#input: blocks[[[]]]
#output: new_block[][]
#kiểm tra rồi
def get_new_block(blocks,range_of_block):
    range_of_block[0] = 0
    range_of_block[1] = 3                        #khởi tạo lại giá trị ban đầu cho range của new block
    new_block = blocks[randrange(0,len(blocks))]
    number = randrange(0,7)
    for row in range(len(new_block)):
        for colum in range(len(new_block[row])):
            if new_block[row][colum] != " ":
                new_block[row][colum] = number
    return new_block

#nhập block vào screen
#input: screen and block, range of block
#output: block_in_screen
#kiểm tra rồi
def merge_block_with_screen(empty_screen,block_x,range_of_block):
    block_in_screen = copy.deepcopy(empty_screen)
    for row in range(len(block_x)):
        block_row = block_x[row]
        for colum in range(len(block_row)):
            if block_row[colum] != " ":
                block_in_screen[row+range_of_block[0]][colum+range_of_block[1]] = block_row[colum]
    return block_in_screen

#merge screen and display
#input: screen [][]
#kiểm tra rồi
def display_screen(screen_,score,color):
    os.system("clear")
    thread_println("\nYour score:"+str(score[0]))
    line=""         # đường viền của screen
    for col in range(len(screen_[0])*2+4):
        line = line + "="
    thread_println(line)
    for row in range(len(screen_)):
        print("\r||",end = "")
        for colum in range(len(screen_[row])):
            if screen_[row][colum] != " ":
                num = screen_[row][colum]
                print(color[num],end = "")
            else:
                print(" ",end = " ")
        print("||")    #when print finish 1 row
    thread_println(line)
    thread_println("Ps: w: rotate, a: move left, s: down faster d: move right")
    thread_println("Ps: x and Ctrl + z to exit the program")
    time.sleep(0.001)
 
#dich trai:
#input: screen and block, range of block
#output: new_screen
#kiểm tra rồi
def move_left(empty_screen,block_x,range_of_block):
    new_screen = copy.deepcopy(empty_screen)
    new_screen = merge_block_with_screen(empty_screen,block_x,range_of_block)
    range_new = copy.deepcopy(range_of_block)
    for row in range(len(new_screen)):
        if new_screen[row][0]!= " ":  # when the block in the first colom, we can't move left
            return range_new
    range_new[1] = range_new[1] - 1
    return range_new
    
#dich phải:
#input: screen and block, range of block
#output: new_screen
#kiểm tra rồi
def move_right(empty_screen,block_x,range_of_block):
    new_screen = copy.deepcopy(empty_screen)
    new_screen = merge_block_with_screen(empty_screen,block_x,range_of_block)
    range_new = copy.deepcopy(range_of_block)
    for row in range(len(new_screen)):
        if new_screen[row][len(new_screen[row])-1]!= " ": #when the block in the last colum, we can't move right
            return range_new
    range_new[1]+=1
    return range_new

# xuống hàng:
#input: screen and block, range of block
#output: new_screen
#kiểm tra rồi,chưa khắc phục được vài lỗi
def down_1_line(empty_screen,block,range_of_block):
    range_new = copy.deepcopy(range_of_block)
    for row in range(len(block)):
        for colum in range(len(block[row])):
            if block[row][colum] != " ":
                last_row = row          # find the last row of block has character
    if range_of_block[0]<len(empty_screen)-last_row - 1: # this is the condition so that we can down i line
        range_new[0] += 1
        return range_new
    else:  
        return range_new   # when we can't down
 
#rotate 90 độ
######################################
#input: block
#output: new block
def rotate_block_90(screen,block,range_of_block):
    block1 = copy.deepcopy(block)
    range_rotate = copy.deepcopy(range_of_block)
    if range_rotate[1]<0:             # when we move left out of range, we have to edit range
        range_rotate[1] = 0
    if range_rotate[1]>len(screen[0])-len(block):   # when we move right out of range, we have to edit range 
        range_rotate[1] = len(screen[0])-len(block)
    # if range_rotate[0] > len(screen) - len(block):
        # range_rotate[0] = len(screen) - len(block)
    for row in range(len(block)):
        for colum in range(len(block[row])):
            block1[colum][row] = block[row][colum]
    block2 = copy.deepcopy(block)
    for row in range(len(block)):
        for colum in range(len(block[row])):
            block2[row][colum] = block1[row][len(block[row])-1-colum]
    return block2,range_rotate

#kiểm tra new-screen với screen chính có bị trùng nhau không
#input: main screen và new-screen
#output: True or False
#kiểm tra rồi
def kiem_tra_khong_trung_screen(main_screen,next_screen):
    linh_canh = 0
    for row in range(len(main_screen)):
        for colum in range(len(main_screen[row])):
            if next_screen[row][colum] != " " :
                if main_screen[row][colum] != " ":
                    linh_canh = 1
    if linh_canh == 1:   
        return False
    else:
        return True

#xóa dòng i và dịch các dòng ở trên dòng i xuống
#input: main_screen và row i
#output: main_screen
#kiểm tra rồi
def delete_row_i(main_screen,row_i):
    for row in range(row_i,0,-1):               # move all row above row i down 1 line
        for colum in range(len(main_screen[row])):
            main_screen[row][colum] = main_screen[row-1][colum]
    for colum in range(len(main_screen[0])):
        main_screen[0][colum] = " "   
    return main_screen

#kiểm tra có hàng nào đầy k
#input: main_screen
#output: main_screen được lọc hết những dòng đầy rồi 
#kiểm tra rồi
def check_full_row(main_screen,score):
    for row in range(len(main_screen)):
        linh_canh = 1
        for colum in range(len(main_screen[row])):
            if main_screen[row][colum] == " ":     # the row has any " " then it isn't full
                linh_canh = 0
        if linh_canh == 1:
            score[0] += 1
            main_screen = delete_row_i(main_screen,row)
    return main_screen

# kiểm tra gameover
#input: main screen
#output: True or False
def check_gameover(main_screen,block):
    for colum in range(3,3+len(block[0]),1):
        if main_screen[0][colum] != " ":
            return True
    return False

def check_to_change(main_screen,empty_screen ,block,range_of_block,score,range_change):
    if range_of_block != range_change:   # when we can move left
            screen_change= merge_block_with_screen(empty_screen,block,range_change)
            if kiem_tra_khong_trung_screen(main_screen,screen_change) :
                range_of_block = range_change
                dis_screen = merge_block_with_screen(main_screen,block,range_of_block)
                display_screen(dis_screen,score,color)
    return range_of_block


def compare_to_move_left(main_screen,empty_screen ,block,range_of_block,score,player_move):
    if player_move == "a":
        range_left=move_left(empty_screen,block,range_of_block)
        range_of_block = check_to_change(main_screen,empty_screen ,block,range_of_block,score,range_left)
    return range_of_block

def compare_to_move_right(main_screen,empty_screen ,block,range_of_block,score,player_move):
    if player_move == "d":
        range_right = move_right(empty_screen,block,range_of_block)
        range_of_block = check_to_change(main_screen,empty_screen ,block,range_of_block,score,range_right)
    return range_of_block

def rotate_left_right(main_screen,empty_screen,block,range_of_block,block_rotate,range_rotate,check_flag):
    index = 0
    for i in range(len(change)):
        if range_of_block[1] < len(main_screen[0]) - len(block) - change[i][1]:
            if range_of_block[1] > -change[i][1] -1:
                if range_of_block[0] + change[i][0] > -1:
                    index = i
                    range_rotate[0] = range_of_block[0] + change[i][0]
                    range_rotate[1] = range_of_block[1] + change[i][1]
                    screen_rotate = merge_block_with_screen(empty_screen ,block_rotate,range_rotate)
                    if kiem_tra_khong_trung_screen(main_screen,screen_rotate):
                        break
    screen_rotate = merge_block_with_screen(empty_screen,block_rotate,range_rotate)
    if kiem_tra_khong_trung_screen(main_screen,screen_rotate):
        block = block_rotate
        range_of_block = range_rotate
    if change[index][0] != 0:
        check_flag = 1
    return block, range_of_block,check_flag
    #  có thêm flag_down cho phép xoay khi gặp chướng ngại vật phía dưới

def  compare_to_move_rotate(main_screen,empty_screen ,block,range_of_block,score,player_move,flag_down,check_flag):
    if player_move == "w":
        block_rotate = copy.deepcopy(block)
        range_rotate = copy.deepcopy(range_of_block)
        block_rotate,range_rotate = rotate_block_90(screen,block,range_of_block)
        last_row = 0
        for row in range(len(block_rotate)):
            for colum in range(len(block_rotate[row])):
                if block_rotate[row][colum] != " ":
                    last_row = row
        if range_rotate[0] < len(main_screen) - last_row -1 : # if "==" => rotare out of range
            screen_rotate = merge_block_with_screen(empty_screen,block_rotate,range_rotate)        
            if  kiem_tra_khong_trung_screen(main_screen,screen_rotate) : 
                block = block_rotate
                range_of_block = range_rotate
                dis_screen = merge_block_with_screen(main_screen,block,range_of_block)                   
                display_screen(dis_screen,score,color) 
            #Khi gặp chướng ngại vật bên trái or phải k xoay đc
            else:
                block,range_of_block,check_flag = rotate_left_right(main_screen,empty_screen,block,range_of_block,block_rotate,range_rotate,check_flag)
                dis_screen = merge_block_with_screen(main_screen,block,range_of_block)                           
                display_screen(dis_screen,score,color)
        elif flag_down == 1:
            block = block_rotate
            range_of_block[0] = len(main_screen) - last_row - 1
            dis_screen = merge_block_with_screen(main_screen,block,range_of_block)               
            display_screen(dis_screen,score,color)
            check_flag =1
            ################################
    return block,range_of_block,check_flag

def  compare_to_drop_all(main_screen,empty_screen ,block,range_of_block,score,player_move):
    if player_move == " ":
        while True:
            range_down = down_1_line(empty_screen,block,range_of_block)
            if range_of_block  ==  range_down:  #when we can't down
                break
            screen_down = merge_block_with_screen(empty_screen,block,range_down)
            if not kiem_tra_khong_trung_screen(main_screen,screen_down) :
                break      
            range_of_block = range_down
        dis_screen = merge_block_with_screen(main_screen,block,range_of_block)
        display_screen(dis_screen,score,color)
    return range_of_block

def compare_to_drop_faster(main_screen,empty_screen ,block,range_of_block,score,player_move):
    if player_move == "s":
        range_down = down_1_line(empty_screen,block,range_of_block)
        range_of_block = check_to_change(main_screen,empty_screen ,block,range_of_block,score,range_down) 
    return range_of_block

def read_character():
    while True:   
        key = readchar.readchar()        
        input_queue.put(key)
        if key == "x":
            break
def thread_println(string):
    print('\r'+string)

def next_to_down_1_line(main_screen,block,range_of_block,score): 
    range_of_block = down_1_line(main_screen,block,range_of_block)
    dis_screen = merge_block_with_screen(main_screen,block,range_of_block)
    display_screen(dis_screen,score,color)
    return range_of_block

def compare_character_input(main_screen,block,range_of_block,score,flag_down,check_flag,level):
    time_count = 0.0
    while int(time_count + score[0]/3*level) != 1: #when you get 3 score, block down fast 0.1s
        if not input_queue.empty():    
            player_move =  input_queue.get()
            range_of_block = compare_to_move_left(main_screen,empty_screen ,block,range_of_block,score,player_move)
            range_of_block = compare_to_move_right(main_screen,empty_screen ,block,range_of_block,score,player_move)
            block,range_of_block,check_flag = compare_to_move_rotate(main_screen,empty_screen ,block,range_of_block,score,player_move,flag_down,check_flag)
            range_of_block = compare_to_drop_all(main_screen,empty_screen ,block,range_of_block,score,player_move)
            range_of_block = compare_to_drop_faster(main_screen,empty_screen ,block,range_of_block,score,player_move)     
            if player_move == " ":
                 return block,range_of_block, check_flag
        time_count += 0.001
        time.sleep(0.001)
    return block,range_of_block, check_flag


#  có thêm flag_down cho phép xoay khi gặp chướng ngại vật phía dưới
def loop_down_1_line_and_get_input(main_screen,empty_screen ,block,range_of_block,score,level,flag_down):
    while True:
        check_flag = 0
        block,range_of_block,check_flag = compare_character_input(main_screen,block,range_of_block,score,flag_down,check_flag,level)
        if check_flag == 1:
            flag_down = 0
        range_down = down_1_line(empty_screen,block,range_of_block)
        if range_of_block  ==  range_down: 
            break
        screen_down = merge_block_with_screen(empty_screen,block,range_down)
        if not kiem_tra_khong_trung_screen(main_screen,screen_down) :
            break
        range_of_block = next_to_down_1_line(main_screen,block,range_of_block,score)
    return range_of_block,block
 
#### thêm flag_down để cho phép xoay trong vòng 1 giây khi block rơi xuống đấy or chướng ngại vật phía dưới
def input_keyboard(main_screen,empty_screen ,block,range_of_block,score,input_queue,level):
    while True:
        flag_down = 1
        input_queue.queue.clear()
        block = get_new_block(blocks,range_of_block)
        dis_screen = merge_block_with_screen(main_screen,block,range_of_block)
        display_screen(dis_screen,score,color)
        range_of_block,block = loop_down_1_line_and_get_input(main_screen,empty_screen ,block,range_of_block,score,level,flag_down)
        main_screen = merge_block_with_screen(main_screen,block,range_of_block)
        check_full_row(main_screen,score)
        display_screen(main_screen,score,color)        
        if check_gameover(main_screen,block):
            break
    thread_println("gameover")

if __name__ == "__main__":    
    colum_of_scr=10
    row_of_scr=20
    time_level = 0.1 #when you get 1 score, tetris down faster 0.05s
    screen=init_screen(row_of_scr,colum_of_scr)
    blocks = [block_0,block_1,block_2,block_3,block_4,block_5,block_6]
    range_of_block = [0,0]
    score = [0]
    main_screen = copy.deepcopy(screen)
    empty_screen = copy.deepcopy(screen)
    block = get_new_block(blocks,range_of_block)
    input_queue = queue.Queue()
    loop_input  =  threading.Thread(target = input_keyboard, args = (main_screen,empty_screen ,block,range_of_block,score,input_queue,time_level))
    loop_read_character = threading.Thread(target = read_character)
    loop_input.start()
    loop_read_character.start()

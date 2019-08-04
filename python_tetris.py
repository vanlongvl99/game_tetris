from random import randrange
import os , time, datetime, copy, readchar, threading, queue, datetime

#tuple là gì

block_0 = [["$","$"],
          ["$","$"]]
          
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
    return blocks[randrange(0,len(blocks))]

#nhập block vào screen
#input: screen and block, range of block
#output: block_in_screen
#kiểm tra rồi
def merge_block_with_screen(screen_phu,block_x,range_of_block):
    block_in_screen = copy.deepcopy(screen_phu)
    for row in range(len(block_x)):
        block_row = block_x[row]
        for colum in range(len(block_row)):
            if block_row[colum] != " ":
                block_in_screen[row+range_of_block[0]][colum+range_of_block[1]] = "$"
    return block_in_screen

#merge screen and display
#input: screen [][]
#kiểm tra rồi
def display_screen(screen_,score):
    os.system("clear")
    merge_scr = []
    thread_println("\nYour score:"+str(score[0]))
    line=""         # đường viền của screen
    for col in range(len(screen_[0])*2+4):
        line = line + "="
    thread_println(line)
    for row in range(len(screen_)):
        print("\r||",end = "")
        for colum in range(len(screen_[row])):
            if screen_[row][colum] != " ":
                print("\033[0;32;42m $\033[0m",end = "")
            else:
                print(" ",end = " ")
        print("||")    #when print finish 1 row
    thread_println(line)
    thread_println("Ps: w: rotate, a: move left, s: down faster d: move right")
    thread_println("Ps: x and Ctrl + z to exit the program")
 
#dich trai:
#input: screen and block, range of block
#output: new_screen
#kiểm tra rồi
def move_left(screen_phu,block_x,range_of_block):
    new_screen = copy.deepcopy(screen_phu)
    new_screen = merge_block_with_screen(screen_phu,block_x,range_of_block)
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
def move_right(screen_phu,block_x,range_of_block):
    new_screen = copy.deepcopy(screen_phu)
    new_screen = merge_block_with_screen(screen_phu,block_x,range_of_block)
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
def down_1_line(screen_phu,block,range_of_block):
    range_new = copy.deepcopy(range_of_block)
    for row in range(len(block)):
        for colum in range(len(block[row])):
            if block[row][colum] != " ":
                last_row = row          # find the last row of block has character
    if range_of_block[0]<len(screen_phu)-last_row - 1: # this is the condition so that we can down i line
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
    if range_of_block[1]<0:             # when we move left out of range, we have to edit range
        range_of_block[1] = 0
    if range_of_block[1]>len(screen[0])-len(block):   # when we move right out of range, we have to edit range 
        range_of_block[1] = len(screen[0])-len(block)
    for row in range(len(block)):
        for colum in range(len(block[row])):
            block1[colum][row] = block[row][colum]
    block2 = copy.deepcopy(block)
    for row in range(len(block)):
        for colum in range(len(block[row])):
            block2[row][colum] = block1[row][len(block[row])-1-colum]
    return block2,range_of_block

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
    for row in range(row_i,-1,-1):               # move all row above row i down 1 line
        for colum in range(len(main_screen[row])):
            if main_screen[row][colum] != " ":
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


def compare_to_move_left(main_screen,block,range_of_block,score,player_move):
    if player_move == "a":
        range_left=move_left(screen_phu,block,range_of_block)
        if range_of_block != range_left:   # when we can move left
            screen_left= merge_block_with_screen(screen_phu,block,range_left)
            if kiem_tra_khong_trung_screen(main_screen,screen_left) :
                range_of_block = range_left
                dis_screen = merge_block_with_screen(main_screen,block,range_of_block)
                time.sleep(0.01)
                display_screen(dis_screen,score)
    return range_of_block


def compare_to_move_right(main_screen,block,range_of_block,score,player_move):
    if player_move == "d":
        range_right = move_right(screen_phu,block,range_of_block)
        if range_of_block != range_right:     # when we can move right
            screen_right = merge_block_with_screen(screen_phu,block,range_right)
            if kiem_tra_khong_trung_screen(main_screen,screen_right) :
                range_of_block = range_right
                dis_screen = merge_block_with_screen(main_screen,block,range_of_block)                
                time.sleep(0.01)
                display_screen(dis_screen,score)
    return range_of_block

def  compare_to_move_rotate(main_screen,block,range_of_block,score,player_move):
    if player_move == "w":
        block_rotate = rotate_block_90(screen,block,range_of_block)
        screen_rotate = merge_block_with_screen(screen_phu,block_rotate,range_of_block)
        if  kiem_tra_khong_trung_screen(main_screen,screen_rotate) : 
            block,range_of_block = block_rotate
            dis_screen = merge_block_with_screen(main_screen,block,range_of_block)
            time.sleep(0.01)                
            display_screen(dis_screen,score)
    return block

def  compare_to_drop_all(main_screen,block,range_of_block,score,player_move):
    if player_move == " ":
        while True:
            range_down = down_1_line(screen_phu,block,range_of_block)
            if range_of_block  ==  range_down:  #when we can't down
                break
            screen_down = merge_block_with_screen(screen_phu,block,range_down)
            if not kiem_tra_khong_trung_screen(main_screen,screen_down) :
                break      
            range_of_block = range_down
        dis_screen = merge_block_with_screen(main_screen,block,range_of_block)
        display_screen(dis_screen,score)
    return range_of_block

def compare_to_drop_faster(main_screen,block,range_of_block,score,player_move):
    if player_move == "s":
        if range_of_block  ==  down_1_line(screen_phu,block,range_of_block): 
            return range_of_block
        if not kiem_tra_khong_trung_screen(main_screen,merge_block_with_screen(screen_phu,block,down_1_line(screen_phu,block,range_of_block))) :
            return range_of_block
        range_of_block = next_to_down_1_line(main_screen,block,range_of_block,score) 
    return range_of_block


def read_character():
    while True:   
        key = readchar.readchar()        
        input_queue.put(key)
        if key == "x":
            break
def thread_println(str):
    print('\r'+str)

def next_to_down_1_line(main_screen,block,range_of_block,score): 
    range_of_block = down_1_line(main_screen,block,range_of_block)
    dis_screen = merge_block_with_screen(main_screen,block,range_of_block)
    display_screen(dis_screen,score)
    return range_of_block
def compare_character_input(main_screen,block,range_of_block,score):
    if not input_queue.empty():    
        player_move =  input_queue.get()
        range_of_block = compare_to_move_left(main_screen,block,range_of_block,score,player_move)
        range_of_block = compare_to_move_right(main_screen,block,range_of_block,score,player_move)
        block = compare_to_move_rotate(main_screen,block,range_of_block,score,player_move)
        range_of_block = compare_to_drop_all(main_screen,block,range_of_block,score,player_move)
        range_of_block = compare_to_drop_faster(main_screen,block,range_of_block,score,player_move)     
    return block,range_of_block


def loop_down_1_line_and_get_input(main_screen,block,range_of_block,score,level):
    time_count = 0.0
    while True:
        while int(time_count + score[0]*level) != 1:
            block,range_of_block = compare_character_input(main_screen,block,range_of_block,score)
            time_count += 0.01
            time.sleep(0.01)
        time_count = 0
        if range_of_block  ==  down_1_line(screen_phu,block,range_of_block): 
            break
        if not kiem_tra_khong_trung_screen(main_screen,merge_block_with_screen(screen_phu,block,down_1_line(screen_phu,block,range_of_block))) :
            break
        range_of_block = next_to_down_1_line(main_screen,block,range_of_block,score)
    return range_of_block,block


def input_keyboard(main_screen,block,range_of_block,score,input_queue,level):
    while True:
        input_queue.queue.clear()
        block = get_new_block(blocks,range_of_block)
        screen_phu = copy.deepcopy(screen)
        new_scr = merge_block_with_screen(screen_phu,block,range_of_block)
        dis_screen = merge_block_with_screen(main_screen,block,range_of_block)
        range_of_block,block = loop_down_1_line_and_get_input(main_screen,block,range_of_block,score,level)
        main_screen = merge_block_with_screen(main_screen,block,range_of_block)
        check_full_row(main_screen,score)
        display_screen(main_screen,score)        
        if check_gameover(main_screen,block):
            break
    thread_println("gameover")

if __name__  ==  "__main__":
    colum_of_scr=10
    row_of_scr=20
    time_level = 0.05 #when you get 1 score, tetris down faster 0.05s
    screen=init_screen(row_of_scr,colum_of_scr)
    blocks = [block_0,block_1,block_2,block_3,block_4,block_5,block_6]
    range_of_block = [0,0]
    score = [0]
    main_screen = copy.deepcopy(screen)
    screen_phu = copy.deepcopy(screen)
    block = get_new_block(blocks,range_of_block)
    input_queue = queue.Queue()
    loop_input  =  threading.Thread(target = input_keyboard, args = (main_screen,block,range_of_block,score,input_queue,time_level))
    loop_read_character = threading.Thread(target = read_character)
    loop_input.start()
    loop_read_character.start()
from random import randrange
import os 
import time
import datetime
import copy
import readchar
import threading
import queue


screen=[ [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "," "," "," "]]

block_0=[["*","*"],
         ["*","*"]]
          
block_1=[["*","*","*"],
         [" ","*"," "],
         [" "," "," "]]
        
block_2=[[" ","*","*"],
         ["*","*"," "],
         [" "," "," "]]

block_3=[["*"," "," "],
         ["*","*","*"],
         [" "," "," "]]

block_4=[[" "," "," "," "],
         ["*","*","*","*"],
         [" "," "," "," "],
         [" "," "," "," "],]


block_5=[[" "," ","*"],
         ["*","*","*"],
         [" "," "," "]]

block_6=[["*","*"," "],
         [" ","*","*"],
         [" "," "," "]]


blocks=[block_0,block_1,block_2,block_3,block_4,block_5,block_6]
range_of_block=[0,0]
score=[0]

#random get new block
#input: blocks[[[]]]
#output: new_block[][]
#kiểm tra rồi
def get_new_block(blocks,range_of_block):
    range_of_block[0]=0
    range_of_block[1]=3                        #khởi tạo lại giá trị ban đầu cho range của new block
    return blocks[randrange(0,len(blocks))]

#nhập block vào screen
#input: screen and block, range of block
#output: block_in_screen
#kiểm tra rồi
def merge_block_with_screen(screen_phu,block_x,range_of_block):
    block_in_screen=copy.deepcopy(screen_phu)
    for row in range(len(block_x)):
        block_row=block_x[row]
        for colum in range(len(block_row)):
            if block_row[colum]=="*":
                block_in_screen[row+range_of_block[0]][colum+range_of_block[1]]="*"
    return block_in_screen

#merge screen and display
#input: screen [][]
#kiểm tra rồi
def display_screen(screen_,score):
    time.sleep(0.5)
    os.system("clear")
    merge_scr=[]
    thread_println("######")
    thread_println("#"+str(score[0])+"#")
    thread_println("######")
    thread_println("======================\n")
    for row in range(len(screen_)):
        string_row =""
        for colum in range(len(screen_[row])):
            string_row+=screen_[row][colum]
        merge_scr.append(string_row) 
    for row in range(len(merge_scr)):
        thread_println(merge_scr[row])

#dich trai:
#input: screen and block, range of block
#output: new_screen
#kiểm tra rồi
def move_left(screen_phu,block_x,range_of_block):
    new_screen=copy.deepcopy(screen_phu)
    new_screen=merge_block_with_screen(screen_phu,block_x,range_of_block)
    range_new=copy.deepcopy(range_of_block)
    linh_canh=1
    for row in range(len(new_screen)):
        if new_screen[row][0]=="*":
            return range_new
    range_new[1]=range_new[1]-1
    return range_new
    
#dich phải:
#input: screen and block, range of block
#output: new_screen
#kiểm tra rồi
def move_right(screen_phu,block_x,range_of_block):
    new_screen=copy.deepcopy(screen_phu)
    new_screen=merge_block_with_screen(screen_phu,block_x,range_of_block)
    range_new=copy.deepcopy(range_of_block)
    linh_canh=1
    for row in range(len(new_screen)):
        if new_screen[row][9]=="*":
            return range_new
    range_new[1]+=1
    return range_new

# xuống hàng:
#input: screen and block, range of block
#output: new_screen
#kiểm tra rồi,chưa khắc phục được vài lỗi
def down_1_line(screen_phu,block,range_of_block):
    range_new=copy.deepcopy(range_of_block)
    if range_of_block[0]<len(screen_phu)-len(block):
        range_new[0]+=1
        return range_new
    else:
        return range_new
 
#xoay 90 độ
######################################
#input: block
#output: new block
def xoay_block_90(block):
    block1=copy.deepcopy(block)
    for row in range(len(block)):
        for colum in range(len(block[row])):
            block1[colum][row]=block[row][colum]
    block2=copy.deepcopy(block)
    for row in range(len(block)):
        for colum in range(len(block[row])):
            block2[row][colum]=block1[row][len(block[row])-1-colum]
    return block2

#kiểm tra new-screen với screen chính có bị trùng nhau không
#input: screen chính và new-screen
#output: True or False
#kiểm tra rồi
def kiem_tra_khong_trung_screen(main_screen,next_screen):
    for colum in range(len(next_screen[0])):
        if next_screen[len(next_screen)-1][colum]=="*":
            return False
    linh_canh=0
    for row in range(len(main_screen)):
        for colum in range(len(main_screen[row])):
            if next_screen[row][colum]=="*" :
                if main_screen[row][colum]=="*":
                    linh_canh=1
    if linh_canh==1:
        return False
    else:
        return True

#xóa dòng i và dịch các dòng ở trên dòng i xuống
#input: main_screen và i
#output: main_screen
#kiểm tra rồi
def xoa_dich_dong_i(main_screen,row_i):
    for colum in range(len(main_screen[row_i])):
        main_screen[row_i][colum]=" "
    for row in range(row_i,-1,-1):
        for colum in range(len(main_screen[row])):
            if main_screen[row][colum]=="*":
                main_screen[row+1][colum]="*"
                main_screen[row][colum]=" "
    return main_screen

#kiểm tra có hàng nào đầy k
#input: main_screen
#output: main_screen được lọc hết những dòng đầy rồi 
#kiểm tra rồi
def kiem_tra_hang_day(main_screen,score):
    for row in range(len(main_screen)):
        linh_canh=1
        for colum in range(len(main_screen[row])):
            if main_screen[row][colum]==" ":
                linh_canh=0
        if linh_canh==1:
            score[0]+=1
            main_screen=xoa_dich_dong_i(main_screen,row)
    return main_screen




# kiểm tra gameover
#input: main screen
#output: True or False
def check_gameover(main_screen,block):
    for colum in range(3,3+len(block[0]),1):
        if main_screen[0][colum]=="*":
            return True
    return False


def compare_to_move_left(main_screen,block,range_of_block,score,player_move):
    if player_move=="a":
        if range_of_block != move_left(screen_phu,block,range_of_block): 
            if kiem_tra_khong_trung_screen(main_screen,merge_block_with_screen(screen_phu,block,move_left(screen_phu,block,range_of_block))) :
                range_of_block=move_left(screen_phu,block,range_of_block)
                dis_screen=merge_block_with_screen(main_screen,block,range_of_block)
                time.sleep(1)
                display_screen(dis_screen,score)
    return range_of_block

def compare_to_move_right(main_screen,block,range_of_block,score,player_move):
    if player_move=="d":
        if range_of_block != move_right(screen_phu,block,range_of_block):  
            if kiem_tra_khong_trung_screen(main_screen,merge_block_with_screen(screen_phu,block,move_right(screen_phu,block,range_of_block))) :
                range_of_block=move_right(screen_phu,block,range_of_block)
                dis_screen=merge_block_with_screen(main_screen,block,range_of_block)                
                time.sleep(1)
                display_screen(dis_screen,score)
    return range_of_block

def  compare_to_move_xoay(main_screen,block,range_of_block,score,player_move):
    if player_move=="w":
        if  kiem_tra_khong_trung_screen(main_screen,merge_block_with_screen(screen_phu,xoay_block_90(block),range_of_block)) :
            block=xoay_block_90(block)
            dis_screen=merge_block_with_screen(main_screen,block,range_of_block)
            time.sleep(1)                
            display_screen(dis_screen,score)
    return block

def  compare_to_drop(main_screen,block,range_of_block,score,player_move):
    if player_move==" ":
        while True:
            if range_of_block == down_1_line(screen_phu,block,range_of_block) or not kiem_tra_khong_trung_screen(main_screen,merge_block_with_screen(screen_phu,block,down_1_line(screen_phu,block,range_of_block))) :
                break      
            range_of_block=down_1_line(screen_phu,block,range_of_block)
        dis_screen=merge_block_with_screen(main_screen,block,range_of_block)
        display_screen(dis_screen,score)
    return range_of_block

######test_không có tác động từ bàn phím#####


def read_character():
    while True:   
        key=readchar.readchar()        
        input_queue.put(key)
        if key=="x":
            break
def thread_println(str):
    print('\r'+str)

def loop_down_1_line(main_screen,block,range_of_block,score):
    while True:
        if not input_queue.empty():    
            player_move= input_queue.get()#phải có tác động từ bàn phím thì chương trình mới tiếp tục
            range_of_block=compare_to_move_left(main_screen,block,range_of_block,score,player_move)
            range_of_block=compare_to_move_right(main_screen,block,range_of_block,score,player_move)
            block=compare_to_move_xoay(main_screen,block,range_of_block,score,player_move)
            range_of_block=compare_to_drop(main_screen,block,range_of_block,score,player_move)        
        if range_of_block == down_1_line(screen_phu,block,range_of_block) or not kiem_tra_khong_trung_screen(main_screen,merge_block_with_screen(screen_phu,block,down_1_line(screen_phu,block,range_of_block))) :
            break  
        range_of_block=down_1_line(main_screen,block,range_of_block)
        dis_screen=merge_block_with_screen(main_screen,block,range_of_block)
        display_screen(dis_screen,score)
    return range_of_block,block


def input_keyboard(main_screen,block,range_of_block,score,input_queue):
    while True:
        block=get_new_block(blocks,range_of_block)
        screen_phu=copy.deepcopy(screen)
        new_scr=merge_block_with_screen(screen_phu,block,range_of_block)
        dis_screen=merge_block_with_screen(main_screen,block,range_of_block)
        range_of_block,block=loop_down_1_line(main_screen,block,range_of_block,score)
        main_screen=merge_block_with_screen(main_screen,block,range_of_block)
        kiem_tra_hang_day(main_screen,score)
        display_screen(main_screen,score)        
        if check_gameover(main_screen,block):
            break
    thread_println("gameover")

################3333
main_screen=copy.deepcopy(screen)
screen_phu=copy.deepcopy(screen)
block=get_new_block(blocks,range_of_block)
########
input_queue=queue.Queue()
x2 = threading.Thread(target=input_keyboard, args=(main_screen,block,range_of_block,score,input_queue))
x3=threading.Thread(target=read_character)
x2.start()
x3.start()

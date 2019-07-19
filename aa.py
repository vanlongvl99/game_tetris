from random import randrange
import os 
import time
import datetime
import copy

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
         [" "," "," "," "]]


blocks=[block_0,block_1,block_2,block_3,block_4]
range_of_block=[0,0]
score=[0]

#random get new block
#input: blocks[[[]]]
#output: new_block[][]
#kiểm tra rồi
def get_new_block(blocks,range_of_block):
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
            block_in_screen[row+range_of_block[0]][colum+range_of_block[1]]=block_row[colum]
    return block_in_screen

#merge screen and display
#input: screen [][]
#kiểm tra rồi
def display_screen(screen_):
    merge_scr=[]
    for row in range(len(screen_)):
        string_row =""
        for colum in range(len(screen_[row])):
            string_row+=screen_[row][colum]
        merge_scr.append(string_row) 
    for row in range(len(merge_scr)):
        print(merge_scr[row])



#dich trai:
#input: screen and block, range of block
#output: new_screen
#kiểm tra rồi
def move_left(screen_phu,block_x,range_of_block):
    new_screen=copy.deepcopy(screen_phu)
    for row in range(len(block_x)):
        block_row=block_x[row]
        for colum in range(len(block_row)):
            if range_of_block[1]>=1:
                new_screen[row+range_of_block[0]][colum+range_of_block[1]-1]=block_row[colum]
            else:
                new_screen[row+range_of_block[0]][colum+range_of_block[1]]=block_row[colum]
    return new_screen

#dich phải:
#input: screen and block, range of block
#output: new_screen
#kiểm tra rồi
def move_right(screen_phu,block_x,range_of_block):
    new_screen=copy.deepcopy(screen_phu)
    for row in range(len(block_x)):
        block_row=block_x[row]
        for colum in range(len(block_row)):
            if range_of_block[1]<len(new_screen[row])-1:
                new_screen[row+range_of_block[0]][colum+range_of_block[1]+1]=block_row[colum]
            else:
                new_screen[row+range_of_block[0]][colum+range_of_block[1]]=block_row[colum]
    return new_screen

# xuống hàng:
#input: screen and block, range of block
#output: new_screen
#kiểm tra rồi,chưa khắc phục được vài lỗi
def down_1_line(screen_phu,block_x,range_of_block):
    new_screen=copy.deepcopy(screen_phu)
    for row in range(len(block_x)):
        block_row=block_x[row]
        for colum in range(len(block_row)):
            if range_of_block[0]<len(new_screen)-len(block):
                new_screen[row+range_of_block[0]+1][colum+range_of_block[1]]=block_row[colum]
            else:
                new_screen[row+range_of_block[0]][colum+range_of_block[1]]=block_row[colum]
    return new_screen

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
def kiem_tra_trung_screen(main_screen,next_screen):
    for colum in range(len(next_screen[0])):
        if next_screen[len(next_screen)-4][colum]=="*":
            return True
    linh_canh=0
    for row in range(len(main_screen)):
        for colum in range(len(main_screen[row])):
            if next_screen[row][colum]=="*" :
                if main_screen[row][colum]=="*":
                    linh_canh=1
    if linh_canh==1:
        return True
    else:
        return False

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


# nhập 2 screen:
#kiểm tra rồi
def nhap_2_screen(main_screen,block_in_screen):
    new_scr=copy.deepcopy(main_screen)
    for row in range(len(new_scr)):
        for colum in range(len(new_scr[row])):
            if block_in_screen[row][colum]=="*":
                new_scr[row][colum]="*"
    return new_scr

# kiểm tra gameover
#input: main screen
#output: True or False
def check_gameover(main_screen,block):
    for colum in range(3,3+len(block[0]),1):
        if main_screen[0][colum]=="*":
            return True
    return False
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
######test_không có tác động từ bàn phím#####
pre_sec=0
main_screen=copy.deepcopy(screen)
screen_phu=copy.deepcopy(screen)
while True:
    block=get_new_block(blocks,range_of_block)
    new_scr=merge_block_with_screen(main_screen,block,range_of_block)
    display_screen(new_scr)
    time_now=datetime.datetime.now()
    while True:
        new_scr=down_1_line(screen_phu,block,range_of_block)
        range_of_block[0]+=1
        os.system("clear")
        display_screen(new_scr)
        time.sleep(1)


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

block_4=[[" "," ","*"," "],
         [" "," ","*"," "],
         [" "," ","*"," "],
         [" "," ","*"," "]]


blocks=[block_0,block_1,block_2,block_3,block_4]
range_of_block=[0,0]
score=0
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



#merge screen để chuẩn bị display
#input: screen [][]
#output: merge_scr []
#kiểm tra rồi
def merge_screen(screen_):
    merge_scr=[]
    for row in range(len(screen_)):
        string_row =""
        for i in range(len(screen_[row])):
            string_row+=screen_[row][i]
        merge_scr.append(string_row)
    return merge_scr

# hiển thị screen
#kiểm tra rồi
def display_screen(merge_scr):
    for row in range(len(merge_scr)-1):
        print(merge_scr[row])

#dich trai:
#input: screen and                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  block, range of block
#output: new_screen
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
def down_1_line(screen_phu,block_x,range_of_block):
    new_screen=copy.deepcopy(screen_phu)
    for row in range(len(block_x)):
        block_row=block_x[row]
        for colum in range(len(block_row)):
            if range_of_block[0]<len(new_screen)-1:
                new_screen[row+range_of_block[0]+1][colum+range_of_block[1]]=block_row[colum]
            else:
                new_screen[row+range_of_block[0]][colum+range_of_block[1]]=block_row[colum]
    return new_screen

#kiểm tra new-screen với screen chính có bị trùng nhau không
#input: screen chính và new-screen
#output: True or False
def kiem_tra_trung_screen(main_screen,next_screen):
    linh_canh=0
    for row in range(len(main_screen)):
        for colum in range(len(main_screen[row])):
            if next_screen[row][colum]=="*" :
                if main_screen[row][colum]=="*":
                    linh_canh=1
                    print(main_screen[row][colum])          
    if linh_canh==1:
        return True
    else:
        return False

#xóa dòng i và dịch các dòng ở trên dòng i xuống
#input: main_screen và i
#output: main_screen
def xoa_dich_dong_i(main_screen,row_i):
    for colum in range(len(main_screen[row_i])):
        main_screen[row_i][colum]=" "
    for row in range(row_i,-1,-1):
        for colum in range(main_screen[row]):
            if main_screen[row][colum]=="*":
                main_screen[row+1][colum]="*"
                main_screen[row][colum]=" "
    return main_screen

#kiểm tra có hàng nào đầy k
#input: main_screen
#output: main_screen được lọc hết những dòng đầy rồi 
def kiem_tra_hang_day(main_screen,score):
    for row in range(len(main_screen)):
        linh_canh=1
        for colum in range(len(main_screen[row])):
            if main_screen[row][colum]==" ":
                linh_canh=0
        if linh_canh==1:
            score+=1
            main_screen=xoa_dich_dong_i(main_screen,row)
    return main_screen


# nhập 2 screen:
def nhap_2_screen(main_screen,block_in_screen):
    new_scr=copy.deepcopy(main_screen)
    for row in range(len(new_scr)):
        for colum in range(len(new_scr[row])):
            if block_in_screen[row][colum]=="*":
                new_scr[row][colum]="*"
    return new_scr


######test#####
screen_phu=copy.deepcopy(screen)
block=get_new_block(blocks,range_of_block)
screen_dis=merge_block_with_screen(screen_phu,block,range_of_block)
merge=merge_screen(screen_dis)
display_screen(merge)

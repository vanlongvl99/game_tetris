

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

figuge_1=[["*","*","*"],
          [" ","*"," "]]
#nhập hình mới vào màng hình
#input: screen and figuge
#output: font_in_screen
def merge_figuge_with_screen(screen,figuge):
    for row in range(len(figuge)):
        screen_row = screen[row]
        figuge_row=figuge[row]
        for colum in range(len(figuge_row)):
            screen_row[colum+3]=figuge_row[colum]
        screen[row]=screen_row
    return screen


#merge screen để chuẩn bị display
#input: screen [][]
#output: merge_scr []
def merge_screen(screen):
    merge_scr=[]
    for row in range(len(screen)):
        string_row =""
        for i in range(len(screen[row])):
            string_row+=screen[row][i]
        merge_scr.append(string_row)
    return merge_scr

# hiển thị screen
def display_screen(merge_scr):
    for row in range(len(merge_scr)-1):
        print(merge_scr[row])

#dich trai:
#input: font_in_screen
#output: new_screen
def move_left(font_in_screen):
    for row in range(len(font_in_screen)):
        for i in range(len(font_in_screen[row])):
            if font_in_screen[row][i]=="*" :
                if i!=0:
                    font_in_screen[row][i-1]=font_in_screen[row][i]
                last_i=i
        font_in_screen[row][last_i]=" "
    return font_in_screen

# xuống 1 hàng
#input: font_in_screen
#output: new_screen
def down_1_line(font_in_screen):
    for row in range(len(font_in_screen) -1,-1,-1):
        for i in range(len(font_in_screen[row])):
            if font_in_screen[row][i]=="*" :
                if row != len(font_in_screen):
                    font_in_screen[row+1][i]=font_in_screen[row][i]
                    highest_row=row
    for i in range(len(font_in_screen[highest_row])) :
        font_in_screen[highest_row][i]=" "
    return font_in_screen

# function main:
font_in_screen=merge_figuge_with_screen(screen,figuge_1)
merge_scr_1=merge_screen(font_in_screen)
display_screen(merge_scr_1)
#font_left=move_left(font_in_screen)
#merge_scr=merge_screen(font_left)
#display_screen(merge_scr)
print("______________")
font_xuong_hang=down_1_line(font_in_screen)
merge_scr=merge_screen(font_xuong_hang)
display_screen(merge_scr)


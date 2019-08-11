package main
import(
	"fmt"
	"math/rand"
    "time"
    "os"
    "os/exec"
    "reflect"
    // "strconv"
    // "github.com/color-master"

)

var blocks = [][][]int{  // this has the pointer
	[][]int{
		[]int{1,1},
		[]int{1,1},},
	[][]int{
		[]int{1,1,1},
		[]int{0,1,0},
		[]int{0,0,0},},
	[][]int{
		[]int{0,1,1},
		[]int{1,1,0},
		[]int{0,0,0},},
	[][]int{
		[]int{1,0,0},
		[]int{1,1,1},
		[]int{0,0,0},},
	[][]int{
		[]int{0,0,1},
		[]int{1,1,1},
		[]int{0,0,0},},
	[][]int{
		[]int{1,1,0},
		[]int{0,1,1},
		[]int{0,0,0},},
	[][]int{
		[]int{0,0,0,0},
		[]int{1,1,1,1},
		[]int{0,0,0,0},
		[]int{0,0,0,0},},
		
} 

//checked and this right
func GetNewBlock(blocks [][][]int)([][]int,[]int){
	LocationOfBlock := []int{0,3}
	rand.Seed(time.Now().UnixNano())  //to random number
	NumberBlock := rand.Intn(7)
	block := blocks[NumberBlock]
	num := rand.Intn(7)
	for num == 0{
		num = rand.Intn(7)  // the number has to difference with 0
	}
	for row := range block{
		for colum := range block[row]{
			if block[row][colum] != 0{
				block[row][colum] = num  //one block has one number
			}
		}
	}
	return block, LocationOfBlock
}

func CopyNewBlock(Block [][]int)[][]int{   // to copy new block
    NewBlock := make([][]int,len(Block))
    for row := range Block{
        NewBlock[row] = make([]int,len(Block[row]))
    }
    for row := range Block{
        for colum := range Block[row]{
            NewBlock[row][colum] = Block[row][colum]
        }
    }
    return NewBlock
}

func CopyNewLoca(Locate []int)[]int{    // to copy new location
    NewLocate := make([]int,len(Locate))
    for row := range Locate{
        NewLocate[row] = Locate[row]
    }
    return NewLocate
}

// checked and this right
func MergeScreenAndBlock(screen_ [20][10]int,block [][]int,Locate []int)([20][10]int){
	BlockInScreen := screen_
	for row := range block{
		for colum := range block[row]{
			if block[row][colum] != 0{
				num := block[row][colum]
				BlockInScreen[row + Locate[0]][colum + Locate[1]] = num
			}
		}
    }
	return BlockInScreen
}

func Down1Line(EmptyScreen [20][10]int,block [][]int,Locate []int)[]int{
    LastRow :=0
    LocateDown := CopyNewLoca(Locate)
    for row := range block{
        for colum := range block[row]{
            if block[row][colum] != 0{
                LastRow = row
            }
        }
    }
    if LocateDown[0]<len(EmptyScreen) - LastRow -1{  // check the last row
        LocateDown[0] +=1                            // it can't down when it's in the last row
        return LocateDown
    }
    return LocateDown
}

func MoveLeft(EmptyScreen[20][10]int,block [][]int,Locate []int)[]int{
    LocateLeft := CopyNewLoca(Locate)
    NewScr := MergeScreenAndBlock(EmptyScreen,block,LocateLeft)
    for row := range NewScr{
        if NewScr[row][0] != 0{    // we can move it turn left when it's in the first colum
            return LocateLeft
        }
    }
    LocateLeft[1] = LocateLeft[1] - 1  
    return LocateLeft
}


func MoveRight(EmptyScreen[20][10]int,block [][]int,Locate []int)[]int{
    LocateRight := CopyNewLoca(Locate)
    NewScr := MergeScreenAndBlock(EmptyScreen,block,LocateRight)
    for row := range NewScr{
        if NewScr[row][len(NewScr[row])-1] != 0{ //we can move it right when it's in then last colum
            return LocateRight
        }
    }
    LocateRight[1] = LocateRight[1] + 1
    return LocateRight
}

// Checked and this right
func RotateBlock90(EmptyScreen[20][10]int,block [][]int,Locate []int)([][]int, []int){
    if Locate[1]<0{             // check index out of range when it rotate
        Locate[1]=0
    }
    if Locate[1]>len(EmptyScreen[0])-len(block){  // check index out of range when it rotate
        Locate[1] = len(EmptyScreen[0])-len(block)
    }
    Block1 := CopyNewBlock(block)
    for row := range block{
        for colum := range block[row]{
            num := block[row][colum]
            Block1[colum][row] = num
        }
    }
    Block2 := CopyNewBlock(block)
    for row := range block{
        for colum := range block[row]{
            Block2[row][colum] = Block1[row][len(block[row]) -1 -colum]
        }
    }
    return Block2, Locate
}

func DeleteRowI(screen_ [20][10]int, RowI int)[20][10]int {
    for row := RowI; row >0; row = row -1{
        for colum := range screen_[row]{
                screen_[row][colum] = screen_[row -1][colum]    
        }
    }
    for colum := range screen_[0]{
        screen_[0][colum] = 0
    }
    return screen_
}

func CheckFullRow(screen_ [20][10]int,score []int)[20][10]int{
    for row := range screen_{
        LinhCanh := 1
        for colum := range screen_[row]{
            if screen_[row][colum] == 0{
                LinhCanh = 0
            }
        }
        if LinhCanh == 1{
            screen_ = DeleteRowI(screen_,row)   // row full and have to delete
            score[0] += 1
        }
    }
    return screen_
}

func CheckOverlapping(MainScreen [20][10]int, NewScr [20][10]int)bool{
    LinhCanh :=0
    for row := range MainScreen{
        for colum := range MainScreen[row]{
            if NewScr[row][colum] != 0{
                if MainScreen[row][colum] != 0{
                    LinhCanh = 1
                }
            }
        }
    }
    if LinhCanh ==1{
        return true
    } else{
        return false
    }
}

// checked and this right
func DisplayScreen(screen_ [20][10]int,score []int ){
    ClearTerminal()
    fmt.Println("\nYour score:",score[0])
    fmt.Println("========================")
    for row := range screen_{
		fmt.Printf("||")
		for colum := range screen_[row]{
			if screen_[row][colum] != 0 {
				// red := color.New(color.FgRed) //make the character is red
				// RedBackground := red.Add(color.BgHiRed) //make the background is red
		     		// RedBackground.Printf("  ")
                fmt.Printf("\033[0;32;42m[]\033[m")
            }else{
				fmt.Printf("  ")
        	}
		}
		fmt.Printf("||\n")	

	}
    fmt.Println("========================")
    fmt.Println("Ps: w: rotate, a: move left, s: down faster d: move right")
    fmt.Println("Ps: x and Ctrl + z to exit the program")
} 


func ClearTerminal(){
	clear := exec.Command("clear")
	clear.Stdout = os.Stdout
	clear.Run()
}
func CheckGameOver(MainScreen [20][10]int,block [][]int)bool{
    for colum :=3; colum<3+len(block); colum++{
        if MainScreen[0][colum] != 0{
            return true
        }
    }
    return false
}

func CompareToMoveLeft(MainScreen [20][10]int,EmptyScreen [20][10]int,block [][]int,Locate []int,character string ,score []int)([]int){
    if character == "a"{
        LocateLeft := MoveLeft(EmptyScreen,block,Locate)
        if reflect.DeepEqual(Locate,LocateLeft) == false{
            ScreenLeft := MergeScreenAndBlock(EmptyScreen,block,LocateLeft)
            if CheckOverlapping(MainScreen,ScreenLeft) == false{
                DisScreen := MergeScreenAndBlock(MainScreen,block,LocateLeft)
                DisplayScreen(DisScreen,score)
                time.Sleep(time.Millisecond)
                return LocateLeft
            }
        }
    }
    return Locate
}

func CompareToDropAll(MainScreen [20][10]int,EmptyScreen [20][10]int,block [][]int,Locate []int,character string,score []int )([]int){
    if character == " "{
        for{
            LocateDown := Down1Line(EmptyScreen,block,Locate)
            if reflect.DeepEqual(Locate,LocateDown){
                break
            }
            ScreenDown := MergeScreenAndBlock(EmptyScreen,block,LocateDown)
            if CheckOverlapping(MainScreen,ScreenDown){
                break
            }
            Locate = LocateDown
        }
        DisScreen := MergeScreenAndBlock(MainScreen,block,Locate)
        DisplayScreen(DisScreen,score)
        time.Sleep(time.Millisecond)

    }
    return Locate
}

func CompareToDropFaster(MainScreen [20][10]int,EmptyScreen [20][10]int,block [][]int,Locate []int,character string,score []int )([]int){
    if character == "s"{
        LocateDown := Down1Line(EmptyScreen,block,Locate)
        if reflect.DeepEqual(Locate,LocateDown) == false{
            ScreenDown := MergeScreenAndBlock(EmptyScreen,block,LocateDown)
            if CheckOverlapping(MainScreen,ScreenDown) == false{
                Locate = LocateDown
                DisScreen := MergeScreenAndBlock(MainScreen,block,Locate)
                DisplayScreen(DisScreen,score)
                time.Sleep(time.Millisecond)
            }
        }
    }
    return Locate
}

func CompareToMoveRight(MainScreen [20][10]int,EmptyScreen [20][10]int,block [][]int,Locate []int,character string,score []int )([]int){
    if character == "d"{
        LocateRight := MoveRight(EmptyScreen,block,Locate)
        if reflect.DeepEqual(Locate,LocateRight) == false{
            ScreenRight := MergeScreenAndBlock(EmptyScreen,block,LocateRight)
            if CheckOverlapping(MainScreen,ScreenRight) == false{
                DisScreen := MergeScreenAndBlock(MainScreen,block,LocateRight)
                DisplayScreen(DisScreen,score)
                time.Sleep(time.Millisecond)
                return LocateRight
            }
        }
    }
    return Locate
}

func CompareToRotate(MainScreen [20][10]int,EmptyScreen [20][10]int,block [][]int,Locate []int,character string ,score []int)([][]int ,[]int){
    if character == "w"{
        BlockRotate,LocateRotate := RotateBlock90(EmptyScreen,block,Locate)
        LastRow := 0
        for row := range block{
            for colum := range block[row]{
                if block[row][colum] != 0{
                    LastRow = row
                }
            }
        }
        if LocateRotate[0] < len(MainScreen) - LastRow -1 {
            ScreenLocate := MergeScreenAndBlock(EmptyScreen,BlockRotate,LocateRotate)
            if CheckOverlapping(MainScreen,ScreenLocate) == false{
                block = BlockRotate
                Locate = LocateRotate
                DisScreen := MergeScreenAndBlock(MainScreen,block,Locate)
                time.Sleep(10*time.Millisecond)
                DisplayScreen(DisScreen,score)
                time.Sleep(time.Millisecond)
            }
        }
    }
    return block,Locate

}

func CompareCharacterInput(MainScreen [20][10]int,EmptyScreen [20][10]int,block [][]int,Locate []int ,score []int,CommunicateChannel chan string)([][]int ,[]int){
    level := 0.1
    TimeCount := 0.0
    for int(TimeCount + float64(score[0]/3)*level) != 1 { 
        select{
        case character,ok := <-CommunicateChannel:
            if ok{
                Locate = CompareToMoveRight(MainScreen,EmptyScreen,block,Locate,character,score)      
                Locate = CompareToMoveLeft(MainScreen,EmptyScreen,block,Locate,character,score)      
                block,Locate = CompareToRotate(MainScreen,EmptyScreen,block,Locate,character,score)   
                Locate = CompareToDropAll(MainScreen,EmptyScreen,block,Locate,character,score)      
                Locate = CompareToDropFaster(MainScreen,EmptyScreen,block,Locate,character,score)
            }else{         
            }
        default:
        }
        TimeCount += 0.001
        time.Sleep(1*time.Millisecond)
    }
    return block,Locate     
}

func LoopDown1Line(MainScreen [20][10]int,EmptyScreen [20][10]int,block [][]int,Locate []int ,CommunicateChannel chan string,score []int )([][]int,[]int){
    for{
        block,Locate = CompareCharacterInput(MainScreen,EmptyScreen,block,Locate,score,CommunicateChannel)  
        LocateDown := Down1Line(EmptyScreen,block,Locate)
        if reflect.DeepEqual(Locate,LocateDown) {
            break
        }
        ScreenDown := MergeScreenAndBlock(EmptyScreen,block,LocateDown)
        if  CheckOverlapping(MainScreen,ScreenDown) {
            break
        }
        Locate = LocateDown
        DisScreen := MergeScreenAndBlock(MainScreen,block,Locate)
        DisplayScreen(DisScreen,score)
    } 
    return block,Locate
}



// thiếu clear CommunicationChannel
func ScreenLoop(MainScreen [20][10]int,EmptyScreen [20][10]int,block [][]int,Locate []int,CommunicateChannel chan string,score []int){
    for{
        block, Locate = GetNewBlock(blocks) 
        DisScreen := MergeScreenAndBlock(MainScreen,block,Locate)
        DisplayScreen(DisScreen,score)
        block,Locate = LoopDown1Line(MainScreen,EmptyScreen,block,Locate,CommunicateChannel,score)
        MainScreen = MergeScreenAndBlock(MainScreen,block,Locate)
        MainScreen = CheckFullRow(MainScreen,score)
        DisplayScreen(MainScreen,score)
        if CheckGameOver(MainScreen,block){
            break
        }
    }   
    fmt.Println("gameover")
}


//  dùng thôi nhưng chưa hiểu
func ReadChar()string{
	// disable input buffering
    exec.Command ("stty", "-F", "/dev/tty", "cbreak", "min", "1").Run()
    // do not display entered characters on the screen
    // exec.Command("stty", "-F", "/dev/tty", "-echo").Run()

	var character []byte = make([]byte, 1)
	os.Stdin.Read(character)
    return string(character)
}


func ReadKeyboard(CommunicateChannel chan string) {  // put the keyboard into channel
    for {
        character := ReadChar()
        CommunicateChannel <- character
        if character == "x"{
            break
        }
    }
}

func main(){
	var EmptyScreen [20][10]int   // this doesn't have the pointer
    var MainScreen [20][10]int
    var score = []int{0}
    CommunicateChannel := make(chan string)
    BlockX, Locate := GetNewBlock(blocks)

    go ReadKeyboard(CommunicateChannel)
    ScreenLoop(MainScreen,EmptyScreen,BlockX,Locate,CommunicateChannel,score)
    for{
        time.Sleep(time.Millisecond)
    }
}
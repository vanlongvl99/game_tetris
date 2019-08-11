
// use struct and method


package main
import(
	"fmt"
	"math/rand"
	"time"
	"os"
    "os/exec"
    "reflect"
)


var blocks = [][][]int{
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
var color = []string{
    "",
	"\033[0;31;41m[]\033[m",    //Text: Red, Background: Red
    "\033[0;32;42m[]\033[m",    //Text: Green, Background: Green
    "\033[0;33;43m[]\033[m",    //Text: Yellow, Background: Yellow
    "\033[0;34;44m[]\033[m",    //Text: Blue, Background: Blue
    "\033[0;35;45m[]\033[m",    //Text: Purple, Background: Purple
    "\033[0;36;46m[]\033[m",    //Text: Cyan, Background: Cyan
    "\033[0;37;47m[]\033[m"}    //Text: White, Background: White
//


type InforOfBlock struct{
	Block [][]int
	FakeBlock [][]int
	Location []int
	FakeLocate []int
	Color []string
}

type TypeScreen struct{
	Main [20][10]int
	Empty [20][10]int
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


//checked and this right
func GetNewBlock(blocks [][][]int)([][]int,[]int){
	LocationOfBlock := []int{0,3}
	rand.Seed(time.Now().UnixNano())
	NumberBlock := rand.Intn(7)
	block := blocks[NumberBlock]
	num := rand.Intn(7)+1
	for row := 0; row<len(block);row++{
		for colum :=0; colum<len(block[row]); colum++{
			if block[row][colum] != 0{
				block[row][colum] = num
			}
		}
	}
	return block, LocationOfBlock
}



// checked and this right
func MergeScreenAndBlock(ScreenEmpty [20][10]int,block [][]int, locate []int)([20][10]int){
	BlockInScreen := ScreenEmpty
	for row := 0; row<len(block); row++{
		for colum :=0; colum<len(block[row]); colum++{
			if block[row][colum] != 0{
				num := block[row][colum]
				BlockInScreen[row + locate[0]][colum + locate[1]] = num
			}
		}
	}
	return BlockInScreen
}

// is checked when it move to last row of screen
// don't have new_location, we have to change the location if we can't down becase of overlapping
func (BlockInfo *InforOfBlock) Down1Line(screen TypeScreen){
	BlockInfo.FakeLocate =CopyNewLoca(BlockInfo.Location)
	LastRow := 0
	for row := range BlockInfo.Block{
		for colum := range BlockInfo.Block {
			if BlockInfo.Block[row][colum] != 0{
				LastRow = row
			}
		}
	}
	if BlockInfo.FakeLocate[0] <len(screen.Empty) - LastRow -1{
		BlockInfo.FakeLocate[0] ++
	}
}



func (BlockInfo *InforOfBlock) MoveLeft(screenscreen TypeScreen){
	BlockInfo.FakeLocate =CopyNewLoca(BlockInfo.Location)
	FistColum :=0
	for colum := len(BlockInfo.Block[0]) -1; colum >-1; colum-- {
		for row := range BlockInfo.Block{
			if BlockInfo.Block[row][colum] != 0{
				FistColum = colum
			}
		}
	}
	if BlockInfo.FakeLocate[1] + FistColum >0{
		BlockInfo.FakeLocate[1] -= 1
	}
}

func (BlockInfo *InforOfBlock) MoveRight(screen TypeScreen){
	BlockInfo.FakeLocate =CopyNewLoca(BlockInfo.Location)
	LastColum :=0
	for colum := range BlockInfo.Block[0] {
		for row := range BlockInfo.Block{
			if BlockInfo.Block[row][colum] != 0{
				LastColum = colum
			}
		}
	}
	if BlockInfo.FakeLocate[1] + LastColum < len(screen.Empty[0]) -1 {
		BlockInfo.FakeLocate[1] += 1
	}
}

func (BlockInfo *InforOfBlock) RotateBlock90(screen TypeScreen){
	BlockInfo.FakeLocate =CopyNewLoca(BlockInfo.Location)  //update 
	if BlockInfo.FakeLocate[1]<0{             // check index out of range when it rotate
        BlockInfo.FakeLocate[1]=0
    }
    if BlockInfo.FakeLocate[1]>len(screen.Empty[0])-len(BlockInfo.Block){  // check index out of range when it rotate
        BlockInfo.FakeLocate[1] = len(screen.Empty[0])-len(BlockInfo.Block)
    }
    Block1 := CopyNewBlock(BlockInfo.Block)
    for row := range BlockInfo.Block{
        for colum := range Block1[row]{
            num := BlockInfo.Block[row][colum]
            Block1[colum][row] = num
        }
    }
    Block2 := CopyNewBlock(Block1)
    for row := range Block1{
        for colum := range Block1[row]{
            Block2[row][colum] = Block1[row][len(Block1[row]) -1 -colum]
        }
	}
	BlockInfo.FakeBlock = CopyNewBlock(Block2)
}


func CheckOverlapping(screen TypeScreen, NewScr [20][10]int)bool{
    LinhCanh :=0
    for row := range screen.Main{
        for colum := range screen.Main[row]{
            if NewScr[row][colum] != 0{
                if screen.Main[row][colum] != 0{
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

func DeleteRowI(screen TypeScreen, RowI int)TypeScreen {
    for row := RowI; row >0; row = row -1{
        for colum := range screen.Main[row]{
                screen.Main[row][colum] = screen.Main[row -1][colum]    
        }
    }
    for colum := range screen.Main[0]{
        screen.Main[0][colum] = 0
    }
    return screen
}

func CheckFullRow(screen TypeScreen,score []int)TypeScreen{
    for row := range screen.Main{
        LinhCanh := 1
        for colum := range screen.Main[row]{
            if screen.Main[row][colum] == 0{
                LinhCanh = 0
            }
        }
        if LinhCanh == 1{
            screen = DeleteRowI(screen,row)   // row full and have to delete
            score[0] += 1
        }
    }
    return screen
}

func DisplayScreen(screen_ [20][10]int,BlockInfo InforOfBlock,score []int ){
    ClearTerminal()
    fmt.Println("\nYour score:",score[0])
    fmt.Println("========================")
    for row := range screen_{
		fmt.Printf("||")
		for colum := range screen_[row]{
			if screen_[row][colum] != 0 {
				num := screen_[row][colum]
				fmt.Printf(BlockInfo.Color[num])
			}else{
				fmt.Printf("  ")
        	}
		}
		fmt.Printf("||\n")	
	}
    fmt.Println("========================")
    fmt.Println("Ps: w: rotate, a: move left, s: down faster d: move right")
    fmt.Println("Ps:Ctrl + z to exit the program")
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

func (BlockInfo *InforOfBlock) CompareToMoveLeft(screen TypeScreen,character string ,score []int){
    if character == "a"{
		BlockInfo.MoveLeft(screen)
		if reflect.DeepEqual(BlockInfo.Location,BlockInfo.FakeLocate) == false{
            ScreenLeft := MergeScreenAndBlock(screen.Empty,BlockInfo.Block,BlockInfo.FakeLocate)
            if CheckOverlapping(screen,ScreenLeft) == false{
                DisScreen := MergeScreenAndBlock(screen.Main,BlockInfo.Block,BlockInfo.FakeLocate)
                DisplayScreen(DisScreen, *BlockInfo,score)
                time.Sleep(time.Millisecond)
				BlockInfo.Location = BlockInfo.FakeLocate
            }
        }
    }
}


func (BlockInfo *InforOfBlock) CompareToDropAll(screen TypeScreen,character string ,score []int){
    if character == " "{
        for{
            BlockInfo.Down1Line(screen)
            if reflect.DeepEqual(BlockInfo.Location,BlockInfo.FakeLocate){
                break
            }
            ScreenDown := MergeScreenAndBlock(screen.Empty,BlockInfo.Block,BlockInfo.FakeLocate)
            if CheckOverlapping(screen,ScreenDown){
                break
            }
            BlockInfo.Location = BlockInfo.FakeLocate
        }
        DisScreen := MergeScreenAndBlock(screen.Main,BlockInfo.Block,BlockInfo.Location)
        DisplayScreen(DisScreen,*BlockInfo,score)
        time.Sleep(time.Millisecond)
    }
}

func (BlockInfo *InforOfBlock) CompareToDropFaster(screen TypeScreen,character string ,score []int){
    if character == "s"{
		BlockInfo.Down1Line(screen)
        if reflect.DeepEqual(BlockInfo.Location,BlockInfo.FakeLocate) == false{
            ScreenDown := MergeScreenAndBlock(screen.Empty,BlockInfo.Block,BlockInfo.FakeLocate)
            if CheckOverlapping(screen,ScreenDown) == false{
                BlockInfo.Location = BlockInfo.FakeLocate
                DisScreen := MergeScreenAndBlock(screen.Main,BlockInfo.Block,BlockInfo.Location)
                DisplayScreen(DisScreen,*BlockInfo,score)
                time.Sleep(time.Millisecond)
            }
        }
    }
}

func (BlockInfo *InforOfBlock) CompareToMoveRight(screen TypeScreen,character string ,score []int ){
    if character == "d"{
		BlockInfo.MoveRight(screen)
		if reflect.DeepEqual(BlockInfo.Location,BlockInfo.FakeLocate) == false{
            ScreenRight := MergeScreenAndBlock(screen.Empty,BlockInfo.Block,BlockInfo.FakeLocate)
            if CheckOverlapping(screen,ScreenRight) == false{
                DisScreen := MergeScreenAndBlock(screen.Main,BlockInfo.Block,BlockInfo.FakeLocate)
                DisplayScreen(DisScreen,*BlockInfo,score)
                time.Sleep(time.Millisecond)
				BlockInfo.Location = BlockInfo.FakeLocate
			}
        }
    }
}

func (BlockInfo *InforOfBlock ) CompareToRotate(screen TypeScreen,character string ,score []int){
    if character == "w"{
		BlockInfo.RotateBlock90(screen)
		LastRow := 0
        for row := range BlockInfo.Block{
            for colum := range BlockInfo.Block[row]{
                if BlockInfo.Block[row][colum] != 0{
                    LastRow = row
                }
            }
        }
        if BlockInfo.FakeLocate[0] < len(screen.Main) - LastRow -1 {
            ScreenLocate := MergeScreenAndBlock(screen.Empty,BlockInfo.FakeBlock,BlockInfo.FakeLocate)
            if CheckOverlapping(screen,ScreenLocate) == false{
                BlockInfo.Block = BlockInfo.FakeBlock
                BlockInfo.Location = BlockInfo.FakeLocate
                DisScreen := MergeScreenAndBlock(screen.Main,BlockInfo.Block,BlockInfo.Location)
                time.Sleep(10*time.Millisecond)
                DisplayScreen(DisScreen,*BlockInfo,score)
                time.Sleep(time.Millisecond)
            }
        }
    }
}


func (BlockInfo *InforOfBlock) CompareCharacterInput(screen TypeScreen,score []int,CommunicateChannel chan string){
    level := 0.1
    TimeCount := 0.0
    for int(TimeCount + float64(score[0]/3)*level) != 1 { 
        select{
        case character,ok := <-CommunicateChannel:
            if ok{
				BlockInfo.CompareToMoveRight(screen,character,score)
				BlockInfo.CompareToMoveLeft(screen,character,score)
				BlockInfo.CompareToRotate(screen,character,score)
				BlockInfo.CompareToDropAll(screen,character,score)
				BlockInfo.CompareToDropFaster(screen,character,score)
            }else{         
            }
        default:
        }
        TimeCount += 0.001
        time.Sleep(1*time.Millisecond)
    }
}


func (BlockInfo *InforOfBlock) LoopDown1Line(screen TypeScreen,CommunicateChannel chan string,score []int){
    for{
		BlockInfo.CompareCharacterInput(screen,score,CommunicateChannel)
		BlockInfo.Down1Line(screen)
        if reflect.DeepEqual(BlockInfo.Location,BlockInfo.FakeLocate) {
            break
		}
        ScreenDown := MergeScreenAndBlock(screen.Empty,BlockInfo.Block,BlockInfo.FakeLocate)
        if  CheckOverlapping(screen,ScreenDown) {
            break
		}
        BlockInfo.Location = BlockInfo.FakeLocate
        DisScreen := MergeScreenAndBlock(screen.Main,BlockInfo.Block,BlockInfo.Location)
		DisplayScreen(DisScreen,*BlockInfo,score)
    } 
}


func ScreenLoop(screen TypeScreen,BlockInfo InforOfBlock,CommunicateChannel chan string,score []int,color []string){
    for{
		block, Locate := GetNewBlock(blocks) 
		BlockInfo = InforOfBlock{block,block,Locate,Locate,color}
        DisScreen := MergeScreenAndBlock(screen.Main,BlockInfo.Block,BlockInfo.Location)
		DisplayScreen(DisScreen,BlockInfo,score)
		BlockInfo.LoopDown1Line(screen,CommunicateChannel,score)
        screen.Main = MergeScreenAndBlock(screen.Main,BlockInfo.Block,BlockInfo.Location)
        screen = CheckFullRow(screen,score)
        DisplayScreen(screen.Main,BlockInfo,score)
        if CheckGameOver(screen.Main,BlockInfo.Block){
            break
        }
    }   
    fmt.Println("gameover")
}


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
    }
}

func main(){
	var screen TypeScreen
	var score = []int{0}
	var BlockInfo InforOfBlock
    CommunicateChannel := make(chan string)
    go ReadKeyboard(CommunicateChannel)
    ScreenLoop(screen,BlockInfo,CommunicateChannel,score,color)
    for{
        time.Sleep(time.Millisecond)
    }
}
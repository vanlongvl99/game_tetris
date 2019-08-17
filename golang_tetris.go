
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

var Change = [][]int{
    []int{0,1},[]int{0,-1},[]int{-1,0},
    []int{-1,1},[]int{-1,-1},
    []int{0,2},[]int{0,-2},[]int{-2,0},
    []int{-2,1},[]int{-2,-1},[]int{-1,2},[]int{-1,-2},
}


type InforOfBlock struct{
	Block [][]int
	FakeBlock [][]int
	Location []int
	FakeLocate []int
	Color []string
}

type TypeScreen struct{
	Main [][]int
    Empty [][]int
    Row int
    Colum int
}

type FlagInfo struct{
    Down int
    Check int
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

func MakeNewScreen(screen TypeScreen)[][]int{   // to copy new block
    NewScreen := make([][]int,screen.Row)
    for row := range NewScreen{
        NewScreen[row] = make([]int,screen.Colum )
    }
    return NewScreen
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



// checked and this right20
func MergeScreenAndBlock(ScreenEmpty [][]int,block [][]int, locate []int)([][]int){
	BlockInScreen := CopyNewBlock(ScreenEmpty)
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
func (block *InforOfBlock) Down1Line(screen TypeScreen){
	block.FakeLocate =CopyNewLoca(block.Location)
	LastRow := 0
	for row := range block.Block{
		for colum := range block.Block {
			if block.Block[row][colum] != 0{
				LastRow = row
			}
		}
	}
	if block.FakeLocate[0] <len(screen.Empty) - LastRow -1{
		block.FakeLocate[0] ++
	}
}



func (block *InforOfBlock) MoveLeft(screenscreen TypeScreen){
	block.FakeLocate =CopyNewLoca(block.Location)
	FistColum :=0
	for colum := len(block.Block[0]) -1; colum >-1; colum-- {
		for row := range block.Block{
			if block.Block[row][colum] != 0{
				FistColum = colum
			}
		}
	}
	if block.FakeLocate[1] + FistColum >0{
		block.FakeLocate[1] -= 1
	}
}

func (block *InforOfBlock) MoveRight(screen TypeScreen){
	block.FakeLocate =CopyNewLoca(block.Location)
	LastColum :=0
	for colum := range block.Block[0] {
		for row := range block.Block{
			if block.Block[row][colum] != 0{
				LastColum = colum
			}
		}
	}
	if block.FakeLocate[1] + LastColum < len(screen.Empty[0]) -1 {
		block.FakeLocate[1] += 1
	}
}

func (block *InforOfBlock) RotateBlock90(screen TypeScreen){
	block.FakeLocate =CopyNewLoca(block.Location)  //update 
	if block.FakeLocate[1]<0{             // check index out of range when it rotate
        block.FakeLocate[1]=0
    }
    if block.FakeLocate[1]>len(screen.Empty[0])-len(block.Block){  // check index out of range when it rotate
        block.FakeLocate[1] = len(screen.Empty[0])-len(block.Block)
    }
    Block1 := CopyNewBlock(block.Block)
    for row := range block.Block{
        for colum := range Block1[row]{
            num := block.Block[row][colum]
            Block1[colum][row] = num
        }
    }
    Block2 := CopyNewBlock(Block1)
    for row := range Block1{
        for colum := range Block1[row]{
            Block2[row][colum] = Block1[row][len(Block1[row]) -1 -colum]
        }
	}
	block.FakeBlock = CopyNewBlock(Block2)
}

func CheckOverlapping(screen TypeScreen, NewScr [][]int)bool{
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

func DisplayScreen(screen_ [][]int,block InforOfBlock,score []int ){
    ClearTerminal()
    fmt.Println("\nYour score:",score[0])
    line := ""
    for i :=0; i< 2*len(screen_[0]) + 4;i++{
        line += "="
    }
    fmt.Println(line)
    for row := range screen_{
		fmt.Printf("||")
		for colum := range screen_[row]{
			if screen_[row][colum] != 0 {
				num := screen_[row][colum]
				fmt.Printf(block.Color[num])
			}else{
				fmt.Printf("  ")
        	}
		}
		fmt.Printf("||\n")	
	}
    fmt.Println(line)
    fmt.Println("Ps: w: rotate, a: move left, s: down faster d: move right")
    fmt.Println("Ps:Ctrl + z to exit the program")
   
} 


func ClearTerminal(){
	clear := exec.Command("clear")
	clear.Stdout = os.Stdout
	clear.Run()
}

func CheckGameOver(MainScreen [][]int,block [][]int)bool{
    for colum :=3; colum<3+len(block); colum++{
        if MainScreen[0][colum] != 0{
            return true
        }
    }
    return false
}

func (block *InforOfBlock) CompareToMoveLeft(screen TypeScreen,character string ,score []int){
    if character == "a"{
		block.MoveLeft(screen)
		if reflect.DeepEqual(block.Location,block.FakeLocate) == false{
            ScreenLeft := MergeScreenAndBlock(screen.Empty,block.Block,block.FakeLocate)
            if CheckOverlapping(screen,ScreenLeft) == false{
                DisScreen := MergeScreenAndBlock(screen.Main,block.Block,block.FakeLocate)
                DisplayScreen(DisScreen, *block,score)
                time.Sleep(time.Millisecond)
				block.Location = block.FakeLocate
            }
        }
    }
}


func (block *InforOfBlock) CompareToDropAll(screen TypeScreen,character string ,score []int){
    if character == " "{
        for{
            block.Down1Line(screen)
            if reflect.DeepEqual(block.Location,block.FakeLocate){
                break
            }
            ScreenDown := MergeScreenAndBlock(screen.Empty,block.Block,block.FakeLocate)
            if CheckOverlapping(screen,ScreenDown){
                break
            }
            block.Location = block.FakeLocate
        }
        DisScreen := MergeScreenAndBlock(screen.Main,block.Block,block.Location)
        DisplayScreen(DisScreen,*block,score)
        time.Sleep(time.Millisecond)
    }
}

func (block *InforOfBlock) CompareToDropFaster(screen TypeScreen,character string ,score []int){
    if character == "s"{
		block.Down1Line(screen)
        if reflect.DeepEqual(block.Location,block.FakeLocate) == false{
            ScreenDown := MergeScreenAndBlock(screen.Empty,block.Block,block.FakeLocate)
            if CheckOverlapping(screen,ScreenDown) == false{
                block.Location = block.FakeLocate
                DisScreen := MergeScreenAndBlock(screen.Main,block.Block,block.Location)
                DisplayScreen(DisScreen,*block,score)
                time.Sleep(time.Millisecond)
            }
        }
    }
}

func (block *InforOfBlock) CompareToMoveRight(screen TypeScreen,character string ,score []int ){
    if character == "d"{
		block.MoveRight(screen)
		if reflect.DeepEqual(block.Location,block.FakeLocate) == false{
            ScreenRight := MergeScreenAndBlock(screen.Empty,block.Block,block.FakeLocate)
            if CheckOverlapping(screen,ScreenRight) == false{
                DisScreen := MergeScreenAndBlock(screen.Main,block.Block,block.FakeLocate)
                DisplayScreen(DisScreen,*block,score)
                time.Sleep(time.Millisecond)
				block.Location = block.FakeLocate
			}
        }
    }
}


func(block *InforOfBlock ) RotateLeftRight(screen TypeScreen, flag FlagInfo)int{
    index := 0
    for i := range Change{
        if block.Location[1] < len(screen.Main[0]) - len(block.Block) - Change[i][1]{
            if block.Location[1] > - Change[i][1] - 1{
                index = i
                block.FakeLocate[0] = block.Location[0] + Change[i][0]
                block.FakeLocate[1] = block.Location[1] + Change[i][1]
                ScreenLocate := MergeScreenAndBlock(screen.Empty,block.FakeBlock,block.FakeLocate)
                if CheckOverlapping(screen,ScreenLocate) == false{
                    break
                }
            }
        }
    }
    ScreenLocate := MergeScreenAndBlock(screen.Empty,block.FakeBlock,block.FakeLocate)
    if CheckOverlapping(screen,ScreenLocate) == false{
        block.Block = block.FakeBlock
        block.Location = block.FakeLocate
    }
    if Change[index][0] != 0{
        flag.Check = 1
    }
    return flag.Check
}




func (block *InforOfBlock ) CompareToRotate(screen TypeScreen,character string ,score []int,flag FlagInfo)int{
    if character == "w"{
		block.RotateBlock90(screen)
		LastRow := 0
        for row := range block.FakeBlock{
            for colum := range block.FakeBlock[row]{
                if block.FakeBlock[row][colum] != 0{
                    LastRow = row
                }
            }
        }
        if block.FakeLocate[0] < len(screen.Main) - LastRow -1 {
            ScreenLocate := MergeScreenAndBlock(screen.Empty,block.FakeBlock,block.FakeLocate)
            if CheckOverlapping(screen,ScreenLocate) == false{
                block.Block = block.FakeBlock
                block.Location = block.FakeLocate
                DisScreen := MergeScreenAndBlock(screen.Main,block.Block,block.Location)
                DisplayScreen(DisScreen,*block,score)
            }else{
                flag.Check = block.RotateLeftRight(screen,flag)
                DisScreen := MergeScreenAndBlock(screen.Main,block.Block,block.Location)
                DisplayScreen(DisScreen,*block,score)
            }
        }else if flag.Down == 1 {
            block.FakeLocate[0] = len(screen.Main) - LastRow -1
            block.Block = block.FakeBlock
            block.Location = block.FakeLocate
            DisScreen := MergeScreenAndBlock(screen.Main,block.Block,block.Location)
            DisplayScreen(DisScreen,*block,score)
            flag.Check = 1
        }
    }
    return flag.Check
}


func (block *InforOfBlock) CompareCharacterInput(screen TypeScreen,score []int,CommunicateChannel chan string,flag FlagInfo)int{
    fmt.Println(flag.Down)
    level := 0.1
    TimeCount := 0.0
    for int(TimeCount + float64(score[0]/3)*level) != 1 { 
        select{
        case character,ok := <-CommunicateChannel:
            if ok{
				block.CompareToMoveRight(screen,character,score)
				block.CompareToMoveLeft(screen,character,score)
				flag.Check = block.CompareToRotate(screen,character,score,flag)
				block.CompareToDropAll(screen,character,score)
                block.CompareToDropFaster(screen,character,score)
                if character == " "{
                    return flag.Check
                }
            }else{         
            }
        default:
        }
        TimeCount += 0.001
        time.Sleep(1*time.Millisecond)
    }
    return flag.Check
}


func (block *InforOfBlock) LoopDown1Line(screen TypeScreen,CommunicateChannel chan string,score []int,flag FlagInfo){
    for{
		flag.Check = block.CompareCharacterInput(screen,score,CommunicateChannel,flag)
        if flag.Check == 1{
            flag.Down = 0
        }
        block.Down1Line(screen)
        if reflect.DeepEqual(block.Location,block.FakeLocate) {
            break
        }
        ScreenDown := MergeScreenAndBlock(screen.Empty,block.Block,block.FakeLocate)
        if  CheckOverlapping(screen,ScreenDown) {
            break
        }
        
        block.Location = block.FakeLocate
        DisScreen := MergeScreenAndBlock(screen.Main,block.Block,block.Location)
		DisplayScreen(DisScreen,*block,score)
    } 
}


func ScreenLoop(screen TypeScreen,block InforOfBlock,CommunicateChannel chan string,score []int,color []string){
    for{
        flag := FlagInfo{1,0}
        BlockNew, Locate := GetNewBlock(blocks)
        block = InforOfBlock{BlockNew,BlockNew,Locate,Locate,color}
        ScreenNew := MergeScreenAndBlock(screen.Empty,block.Block,block.Location)
        if CheckOverlapping(screen,ScreenNew){
            break
        }
        DisScreen := MergeScreenAndBlock(screen.Main,block.Block,block.Location)
		DisplayScreen(DisScreen,block,score)
		block.LoopDown1Line(screen,CommunicateChannel,score,flag)
        screen.Main = MergeScreenAndBlock(screen.Main,block.Block,block.Location)
        screen = CheckFullRow(screen,score)
        DisplayScreen(screen.Main,block,score)
        if CheckGameOver(screen.Main,block.Block){
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

	var character []byte = make([]byte,1)
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
    rand.Seed(time.Now().UnixNano())
    var screen TypeScreen
    screen.Row = 20
    screen.Colum = 10
    screen.Main = MakeNewScreen(screen)
    screen.Empty = MakeNewScreen(screen)
	var score = []int{0}
	var block InforOfBlock
    CommunicateChannel := make(chan string)
    go ReadKeyboard(CommunicateChannel)
    ScreenLoop(screen,block,CommunicateChannel,score,color)
    for{
        time.Sleep(time.Millisecond)
    }
}
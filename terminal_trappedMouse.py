import os, time

class Cell():
    def __init__(self, x, y, cell_type):
        self.x = x
        self.y = y
        self.visited = False
        self.cell_type = cell_type

class Node():
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

class Pilha():
    def __init__(self):
        self.first = None

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.first
        self.first = new_node

    def pop(self):
        if self.first is None:
            return None
        self.first = self.first.next
        return 

    def top(self):
        if self.first is None:
            return None
        return self.first.value

class Maze():
    def __init__(self):
        self.__currentCell = None
        self.__exitCell = None
        self.__entryCell = None
        
        self.__n_rows = 0
        self.__n_columns = 0
        
        self.__passage = '0'
        self.__wall = '1'
        self.__exitMarker = 'e'
        self.__entryMarker = 'm'
        self.__visited = '.'
        
        self.__maze = []
        self.__mazeStack = Pilha()
    
    def colorCell(self, column):
        if (column == self.__currentCell):
            return f"\033[1;34;40m {self.__entryMarker} \033[m"
        if (column.visited == True):
            return f"\033[1;31;40m {self.__visited} \033[m"
        
        match column.cell_type:
            case self.__passage:
                return f"\033[0;30;40m {self.__passage} \033[m"
            case self.__wall:
                return f"\033[0;37;47m {self.__wall} \033[m"
            case self.__exitMarker:
                return f"\033[1;33;40m {self.__exitMarker} \033[m"
        return
    
    def buildMaze(self, file):
        with open(file, 'r') as file:
            lines = file.readlines()
        
        if lines:
            pilha_rows = Pilha()
            
            self.__n_columns = len(lines[0]) + 1
            self.__n_rows = 2
            
            pilha_rows.push(list('1'*self.__n_columns))
            
            for line in reversed(lines):
                line = list(line.strip())
                line.append('1')
                line.insert(0, '1')
                pilha_rows.push(line)
                self.__n_rows += 1
            
            pilha_rows.push(list('1'*self.__n_columns))
            
            for i in range(self.__n_rows):
                temp_row = []
                
                for j in range(self.__n_columns):
                    
                    newCell = Cell(int(i), int(j), pilha_rows.top()[j])
                    temp_row.append(newCell)
                    
                    if (newCell.cell_type == self.__exitMarker):
                        self.__exitCell = newCell
                    elif (newCell.cell_type == self.__entryMarker):
                        self.__entryCell = newCell
                        self.__currentCell = newCell
                    
                pilha_rows.pop()
                self.__maze.append(temp_row)
            
            return
        
    def showMaze(self, sec=0):
        os.system('cls')
        
        print('-=-'*self.__n_columns)
        print('  '*(self.__n_columns-6)  + '\033[1;34;40mLABIRINTO DO RATO\033[m')
        print('-=-'*self.__n_columns)
        
        print(f'Início: ({self.__entryCell.x}, {self.__entryCell.y})')
        print(f'Saída: ({self.__exitCell.x}, {self.__exitCell.y})')
        print(f'Dimensões: {self.__n_rows} x {self.__n_columns}')
        
        for row in self.__maze:
            line = ''
            for column in row:
                cell = self.colorCell(column)
                line = line + cell
            print(line)
        
        print(f'\033[1;34;40mCélula atual: ({self.__currentCell.x}, {self.__currentCell.y})\033[m')
        time.sleep(sec)
        return
    
    def exitMaze(self):
        while (self.__currentCell is not self.__exitCell):
            
            topCell = self.__maze[self.__currentCell.x-1][self.__currentCell.y]
            bottomCell = self.__maze[self.__currentCell.x+1][self.__currentCell.y]
            leftCell = self.__maze[self.__currentCell.x][self.__currentCell.y-1]
            rightCell = self.__maze[self.__currentCell.x][self.__currentCell.y+1]
            
            if (rightCell.cell_type != '1' and rightCell.visited == False):
                self.__mazeStack.push(rightCell)
            elif (leftCell.cell_type != '1' and leftCell.visited == False):
                self.__mazeStack.push(leftCell)
            elif (bottomCell.cell_type != '1' and bottomCell.visited == False):
                self.__mazeStack.push(bottomCell)
            elif (topCell.cell_type != '1' and topCell.visited == False):
                self.__mazeStack.push(topCell)
            else:
                self.__mazeStack.pop()
            
            self.__currentCell.visited = True
            maze.showMaze(.5)
            
            self.__currentCell = self.__mazeStack.top()
    
        maze.showMaze()
        print('-=-'*self.__n_columns)
        print('  '*(self.__n_columns-3)  + '\033[1;33;40mFIM\033[m')
        return


maze = Maze()

maze.buildMaze('labirinto.txt')
maze.exitMaze()

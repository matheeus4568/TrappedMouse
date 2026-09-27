import os, time
from tkinter import *

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
        
        self.n_rows = 0
        self.n_columns = 0
        
        self.__passage = '0'
        self.__wall = '1'
        self.__exitMarker = 'e'
        self.__entryMarker = 'm'
        self.__visited = '.'
        
        self.__maze = []
        self.__mazeStack = Pilha()

    def colorCell(self, column):
        if column == self.__currentCell:
            return "#0066ff"
        if column.visited:
            return "#d44242"
        match column.cell_type:
            case self.__passage:
                return "#ffffff"
            case self.__wall:
                return "#939393"
            case self.__exitMarker:
                return "#e1b700"
        return
    
    def buildMaze(self, file):
        with open(file, 'r') as file:
            lines = file.readlines()
        
        if lines:
            pilha_rows = Pilha()
            
            self.n_columns = len(lines[0]) + 1
            self.n_rows = 2
            
            pilha_rows.push(list('1'*self.n_columns))
            
            for line in reversed(lines):
                line = list(line.strip())
                line.append('1')
                line.insert(0, '1')
                pilha_rows.push(line)
                self.n_rows += 1
            
            pilha_rows.push(list('1'*self.n_columns))
            
            for i in range(self.n_rows):
                temp_row = []
                
                for j in range(self.n_columns):
                    
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
    
    def showMaze(self, canvas, cell_size, sec=0):
        canvas.delete("all")
        
        infos.config(text=f"Início: ({self.__entryCell.x}, {self.__entryCell.y}); Saída: ({self.__exitCell.x}, {self.__exitCell.y})")
        
        currentCell.config(text=f"Célula atual: ({self.__currentCell.x}, {self.__currentCell.y})")
                
        
        for row in self.__maze:
            for cell in row:
                x1 = cell.y * cell_size
                y1 = cell.x * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                color = self.colorCell(cell)
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        if self.__exitCell != self.__currentCell:
            ex = self.__exitCell.y * cell_size + cell_size // 2
            ey = self.__exitCell.x * cell_size + cell_size // 2
            canvas.create_text(ex, ey, text="🧀", font=("Arial", cell_size - 12), fill="#6F3900")

        rx = self.__currentCell.y * cell_size + cell_size // 2
        ry = self.__currentCell.x * cell_size + cell_size // 2
        canvas.create_text(rx, ry, text="🐀", font=("Arial", cell_size - 12), fill="#fff")

        canvas.update()
        time.sleep(sec)
        return

    def exitMaze(self, canvas, cell_size):
        while self.__currentCell is not self.__exitCell:

            self.__currentCell.visited = True

            topCell    = self.__maze[self.__currentCell.x - 1][self.__currentCell.y]
            bottomCell = self.__maze[self.__currentCell.x + 1][self.__currentCell.y]
            leftCell   = self.__maze[self.__currentCell.x][self.__currentCell.y - 1]
            rightCell  = self.__maze[self.__currentCell.x][self.__currentCell.y + 1]

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

            self.__currentCell = self.__mazeStack.top()
            
            self.showMaze(canvas, cell_size, .5)
        status.config(text="FIM", bg="#e1b700")
        return


maze = Maze()
maze.buildMaze('labirinto.txt')

root = Tk()
root.title("Labirinto do Rato")

decor = Label(root, text="-=-"*8)
decor.pack()

title = Label(root, text="LABIRINTO DO RATO", font=("Arial", 10, "bold"), fg="#0066ff")
title.pack()

decor = Label(root, text="-=-"*8)
decor.pack()

currentCell = Label(root, text="", fg="#0066ff")
currentCell.pack()

cell_size = 30
canvas = Canvas(
    root,
    width=maze.n_columns * cell_size,
    height=maze.n_rows * cell_size
)
canvas.pack()

infos = Label(root, text="")
infos.pack()

status = Label(root, text="", fg="#6F3900", font=("Arial", 8, "bold"))
status.pack()

botao = Button(root, text="Iniciar", command=lambda: maze.exitMaze(canvas, cell_size))
botao.pack()

maze.showMaze(canvas, cell_size)

root.mainloop()


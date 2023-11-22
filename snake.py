from turtle import *
import random
import time

class Snake:
    def __init__(self):
        self.squares = []
        self.globScore = 0
        self.head = Turtle()
        self.head.shape('circle')
        self.head.shapesize(1.6,1.6)
        self.head.color('red')
        self.squares.append([self.head,{'dir':'right', 'moveV':0, 'moveH':10}])
        self.block1 = Turtle()
        self.block2 = Turtle()
        self.head.penup()
        self.block1.penup()
        self.block2.penup()
        self.block1.shape('square')
        self.block1.shapesize(1.5,1.5)
        self.block1.color('yellow')
        self.block1.goto(-10,0)
        self.block2.shape('square')
        self.block2.shapesize(1.5,1.5)
        self.block2.color('yellow')
        self.block2.goto(-20,0)
        self.squares.append([self.block1,{'dir':'right', 'moveV':0, 'moveH':10, 'waitList':[]}])
        self.squares.append([self.block2,{'dir':'right', 'moveV':0, 'moveH':10, 'waitList':[]}])
        

    def updateSnake(self,check):
        for i in self.squares:
            if 'waitList' in i[1]:
                i[1]['waitList'].append(check) 

    def goUp(self):
        global moveV,moveH,check
        if self.squares[0][1]['dir'] in {'right', 'left'}:
            moveV = 10
            moveH = 0
            check = [moveV,moveH,self.squares[0][0].xcor(),self.squares[0][0].ycor()]
            self.squares[0][1]['moveV'] = moveV
            self.squares[0][1]['moveH'] = moveH
            self.updateSnake(check)
            self.squares[0][1]['dir'] = 'up'

    def goRight(self):

        global moveV,moveH,check

        if self.squares[0][1]['dir'] in {'up', 'down'}:
            moveV = 0
            moveH = 10
            check = [moveV,moveH,self.squares[0][0].xcor(),self.squares[0][0].ycor()]
            self.squares[0][1]['moveV'] = moveV
            self.squares[0][1]['moveH'] = moveH
            self.updateSnake(check)
            self.squares[0][1]['dir'] = 'right'

    def goLeft(self):

        global moveV,moveH,check
        if self.squares[0][1]['dir'] in {'up', 'down'}:
            moveV = 0
            moveH = -10
            check = [moveV,moveH,self.squares[0][0].xcor(),self.squares[0][0].ycor()]
            self.squares[0][1]['moveV'] = moveV
            self.squares[0][1]['moveH'] = moveH
            self.updateSnake(check)
            self.squares[0][1]['dir'] = 'left'

    def goDown(self):

        global moveV,moveH,check
        if self.squares[0][1]['dir'] in {'right', 'left'}:
            moveV = -10
            moveH = 0
            check = [moveV,moveH,self.squares[0][0].xcor(),self.squares[0][0].ycor()]
            self.squares[0][1]['moveV'] = moveV
            self.squares[0][1]['moveH'] = moveH
            self.updateSnake(check)
            self.squares[0][1]['dir'] = 'down'

    def init_grid(self):
        self.checkSquares = set((i[0].xcor(), i[0].ycor())for i in self.squares)
        self.empty = grid.difference(self.checkSquares)
        return list(self.empty)

    def foodEaten(self):
        tmp = self.squares[-1].copy()
        tmp[0] = tmp[0].clone()
        tmp[1] = tmp[1].copy()
        tmp[1]['waitList'] = tmp[1]['waitList'].copy()
        tmp[0].goto(tmp[0].xcor() - tmp[1]['moveH'], tmp[0].ycor() - tmp[1]['moveV'])
        self.squares.append(tmp)
        self.globScore += 1
        self.score.undo()
        self.score.write(str(self.globScore),align='center', font=("Arial",20,'bold'))

    def init_borders(self):
        border = Turtle()
        border.color('white')
        border.penup()
        border.forward(640)
        border.pendown()
        border.left(90)
        border.forward(300)
        border.left(90)
        border.forward(1280)
        border.left(90)
        border.forward(600)
        border.left(90)
        border.forward(1280)
        border.left(90)
        border.forward(300)
        border.hideturtle()
    
    def init_score(self):
        self.score = Turtle()
        self.score.hideturtle()
        self.score.color('white')
        self.score.penup()
        self.score.goto(-590,320)
        self.score.write("Score: ",align='center', font=("Arial",20,'bold'))
        self.score.goto(-520,320)
        self.score.write(str(self.globScore),align='center', font=("Arial",20,'bold'))
        
def startGame():
    global moveV,moveH,check,grid
    onkeypress(None, 'Return')
    start.undo()
    grid = {(i,j)for i in range(-480,500,10)for j in range(-290,300,10)}
    snake = Snake()
    snake.init_borders()
    snake.init_score()
    check = []
    moveH = 10
    moveV = 0
    listen()
    onkeypress(snake.goUp,'w')
    onkeypress(snake.goRight,'d')
    onkeypress(snake.goLeft,'a')
    onkeypress(snake.goDown,'s')
    ok = True
    while True:
        if ok:
            newGrid = snake.init_grid()
            foodCoord = newGrid[random.randint(0,len(newGrid) - 1)]
            food = Turtle()
            food.speed(0)
            food.penup()
            food.goto(*foodCoord)
            food.color('cyan')
            food.shape('circle')
            food.shapesize(1,1)
            
            ok = False

        for i in snake.squares:

            i[0].goto(i[0].xcor() + i[1]['moveH'], i[0].ycor() + i[1]['moveV'])
            if 'waitList' in i[1] and i[1]['waitList']:
                if i[1]['waitList'][0][2] == i[0].xcor() and i[1]['waitList'][0][3] == i[0].ycor():
                    i[1]['moveV'] = i[1]['waitList'][0][0]
                    i[1]['moveH'] = i[1]['waitList'][0][1]
                    i[1]['waitList'].pop(0)


        headCoord = snake.squares[0][0]
        mxx = max(headCoord.xcor(),foodCoord[0])
        mnx = min(headCoord.xcor(),foodCoord[0])
        mxy = max(headCoord.ycor(),foodCoord[1])
        mny = min(headCoord.ycor(),foodCoord[1])
        if mxx - mnx <= 15 and  mxy - mny <= 15 :
            ok = True
            food.hideturtle()
            snake.foodEaten()

        comp = [(i[0].xcor(),i[0].ycor())for i in snake.squares]
        if len(comp) != len(set(comp)) or (headCoord.xcor() > 640 or headCoord.xcor() < -640 or headCoord.ycor() > 300 or headCoord.ycor() < -300):
            go = Turtle()
            go.color('white')
            go.write("GAME OVER!", align="center",font=('Arial',30,'bold'))
            break

        win.update()
        time.sleep(0.03)

win = Screen()
win.screensize(bg='black')
win.tracer(0)
win.setup(1.00,1.00)
start = Turtle()
start.color('white')
start.hideturtle()
start.write("PRESS ENTER TO START\n\n USE W, S, A, D TO PLAY",align='center',font=('Arial',30,'bold'))
listen()
onkeypress(startGame, 'Return')

done()
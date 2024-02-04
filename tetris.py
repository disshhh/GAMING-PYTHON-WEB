#TETRIS

#importing modules:
import random
import pygame

#RGB color combinations:
BLACK=(4,16,54)
BLUE=(0,0,102)
RED=(252,91,122)
WHITE=(96,96,96)


#initialising the display:
pygame.init()
SWIDTH=600
SHEIGHT=880
CELLSIZE=40
ROWS=(SHEIGHT-160)//CELLSIZE
COLS=SWIDTH//CELLSIZE

clock = pygame.time.Clock()
FPS = 24

screen = pygame.display.set_mode((SWIDTH,SHEIGHT))
pygame.display.set_caption('HEY YOU ARE PLAYING TETRIS! :) ')



#tthe assests:
img1=pygame.image.load('assets/1.png')
img2=pygame.image.load('assets/2.png')
img3=pygame.image.load('assets/3.png')
img4=pygame.image.load('assets/4.png')
img5=pygame.image.load('assets/5.png')
img6=pygame.image.load('assets/6.png')

assests={
    1:img1,
    2:img2,
    3:img3,
    4:img4,
    5:img5,
    6:img6,
}
class Tetraminos:
    
    # MATRIX
    # 0  1  2  3
    # 4  5  6  7
    # 8  9  10 11
    # 12 13 14 15 

    FIGURES={
        'I':[[1,5,9,13],[4,5,6,7]],
        'Z':[[4,5,9,10],[2,6,5,9]],
        'S':[[6,7,9,10],[1,5,6,10]],
        'L':[[1,2,5,9],[0,4,5,6],[1,5,9,8],[4,5,6,10]],
        'J':[[1,2,6,10],[5,6,7,9],[2,6,10,11],[3,5,6,7]],
        'T':[[1,4,5,6],[1,4,5,9],[4,5,6,9],[1,5,6,9]],
        'O':[[1,2,5,6]]
    }
    TYPES = ['I','Z','S','L','J','T','O']

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.type=random.choice(self.TYPES)
        self.shapes=self.FIGURES[self.type]
        self.color=random.randint(1,6)
        self.rotation=0

    def image(self):
        return self.shapes[self.rotation]

    def rotate(self):
        self.rotation=(self.rotation +1 )% len(self.shapes)


class Tetris:
    def __init__(self, rows,cols):
        self.rows=rows
        self.cols=cols
        self.score=0
        self.level=1
        self.board=[[0 for j in range(cols)] for i in range(rows)]
        self.next=None
        self.gameover=False
        self.new_figure()

    def draw_grid(self):
        for i in range(self.rows+1):
            pygame.draw.line(screen,WHITE,(0,CELLSIZE*i),(SWIDTH,CELLSIZE*i),1)
        for j in range(self.cols):
            pygame.draw.line(screen,WHITE,(CELLSIZE*j,0),(CELLSIZE*j,SHEIGHT),1)
    
    def new_figure(self):
        if not self.next:
            self.next=Tetraminos(6,0)
        self.figure=self.next
        self.next=Tetraminos(6,0)


    def intersects(self):
        intersection=False
        for i in range(4):
            for j in range(4):
                if i* 4 + j in self.figure.image():
                    if  i +self.figure.y > self.rows-1 or \
                        j+ self.figure.x > self.cols-1 or \
                        j+self.figure.x < 0 or \
                        self.board[i+self.figure.y][j +self.figure.x] > 0:    
                            intersection=True




        return intersection

    def remove_line(self):
        rerun=False
        for y in range(self.rows-1,0,-1):
            is_full=True
            for x in range(0,self.cols):
                if self.board[y][x]==0:
                    is_full=False


            if is_full:
                del self.board[y]
                self.board.insert(0,[0 for i in range(self.cols)])
                self.score+=1
                if self.score % 10==0:
                    self.level+=1
                rerun=True

        if rerun:
            self.remove_line()    



    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i* 4 + j in self.figure.image():
                    self.board[i+ self.figure.y][j +self.figure.x] = self.figure.color
        self.remove_line()
        self.new_figure()
        if self.intersects():
            self.gameover=True

    def go_space(self):
        while not self.intersects():
            self.figure.y +=1
        self.figure.y -=1
        self.freeze()



    def go_down(self):
        self.figure.y +=1
        if self.intersects():
            self.figure.y -=1
            self.freeze()

    def go_side(self,dx):
        self.figure.x +=dx
        if self.intersects():
            self.figure.x -=dx


    def rotate(self):
        rotation=self.figure.rotation
        self.figure.rotate()





counter=0
move_down=False





tetris=Tetris(ROWS, COLS)


running = True   #so that screen runs infinitely
while running:
    screen.fill(BLACK)

    counter+=1
    if counter>=10000:
        counter = 0

    if counter %(FPS // (tetris.level * 2) )==0 or move_down:
        if not tetris.gameover:
            tetris.go_down()




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key==pygame.K_ESCAPE:
                running = False
            
            if event.key==pygame.K_LEFT:
                tetris.go_side(-1)

            if event.key==pygame.K_RIGHT:
                tetris.go_side(+1)

            if event.key==pygame.K_UP:
                tetris.rotate()

            if event.key==pygame.K_DOWN:
                move_down=True
            
            if event.key==pygame.K_SPACE:
                tetris.go_space()

        if event.type == pygame.KEYUP:
            if event.key==pygame.K_DOWN:
                move_down=False            
            

    tetris.draw_grid()
    #displaying the board
    for x in range (ROWS):
        for y in range(COLS):
            if tetris.board[x][y] > 0:
                val = tetris.board[x][y]
                img = assests[val]
                screen.blit(img,(y*CELLSIZE, x*CELLSIZE))


    #displaying the shape:
    for i in range(4):
        for j in range(4):
            if i * 4 + j in tetris.figure.image():
                x=CELLSIZE*(tetris.figure.x+j)
                y=CELLSIZE*(tetris.figure.y+i)
                img=assests[tetris.figure.color]
                screen.blit(img,(x,y))


    #hud
                


    


    

    pygame.draw.rect(screen,BLUE,(0,SHEIGHT-160,SWIDTH,160))
    pygame.draw.rect(screen,BLUE,(0,0,SWIDTH,SHEIGHT),2)
    pygame.display.update()

    clock.tick(FPS)
    pygame.display.update()
pygame.quit()





import pygame

from random import randint
import sys

sys.setrecursionlimit(10000)
class Cell:
    def __init__(self,row,col,mine=False):
        self.row = row
        self.col = col
        self.mine = mine
        self.neighbours = 0
        self.showed = False
        self.flag = False


class Game:
    def __init__(self,rows,cols,mines,cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.mines = mines
        self.board = [[Cell(j,i) for i in range(self.cols)] for j in range(self.rows)]
        self.started = False
        self.cells_showed = 0
        self.max_flags = mines
        self.cur_flags = 0
        self.win = False
        self.lose = False
        self.gamefont = pygame.font.Font("assets/MavenPro-VariableFont_wght.ttf", int(self.cell_size * 0.63))
        self.x_offset = int(cell_size * 0.27)
        self.y_offset = int(cell_size * 0.17)
        self.menu_height = [100,85][self.cols>=75]
        self.menu_width = self.rows * self.cell_size

    def set_flag(self,x,y):
        cell = self.board[x][y]
        if not cell.flag and self.cur_flags < self.max_flags:
            cell.flag = True
            self.cur_flags +=1
        elif cell.flag:
            cell.flag = False
            self.cur_flags -= 1

    def show(self,x,y):
        if not self.started:
            self.started = True
            self.__mining(x,y)
        cell = self.board[x][y]
        if not cell.showed:
            cell.showed = True
            self.cells_showed += 1
        if cell.mine:
            for i in range(self.rows):
                for j in range(self.cols):
                    if not self.board[i][j].showed:
                        self.board[i][j].showed = True
            game.lose = True
            #self.win_lose_screen()
        else:
           self.open_cells(cell)
           self.draw_cells()
           if self.cells_showed == self.rows * self.cols - self.mines:
               game.win = True
               #self.win_lose_screen()
           # x,y = map(int,input().split()) # КОСТЫЛЬ ДЛЯ ТЕРМИНАЛА
           # return self.show(x,y)


    def __mining(self,x,y):
        count = 0
        while count !=self.mines:
            cell = self.board[randint(0, self.rows-1)][randint(0, self.cols-1)]
            if not cell.mine and not(cell.row == x and cell.col == y):
                cell.mine = True
                count+=1
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.board[i][j]
                self.count_mines(cell)

    def count_mines(self,cell):
        for a in range(cell.row - 1, cell.row + 2):
            for b in range(cell.col - 1, cell.col + 2):
                if a < self.rows and b < self.cols and a >= 0 and b >= 0:
                    cell.neighbours += int(self.board[a][b].mine)

    def open_cells(self,cell):
        for row_shift in range(-1, 2):
            for col_shift in range(-1, 2):
                if ((row_shift== 0 or col_shift == 0) and row_shift != col_shift and cell.row + row_shift >= 0 and cell.col + col_shift >= 0
                    and cell.row + row_shift < self.rows and cell.col + col_shift < self.cols):
                    cell_to_check = self.board[cell.row + row_shift][cell.col + col_shift]
                    if not cell_to_check.showed and not cell_to_check.mine:
                        cell_to_check.showed = True
                        self.cells_showed += 1
                        if cell_to_check.flag:
                            cell_to_check.flag = False
                            self.cur_flags -=1
                        if cell_to_check.neighbours == 0:
                            self.open_cells(cell_to_check )

    def draw_cells(self):
        null= pygame.Rect(0.75*self.rows*self.cell_size, 50,45,30)
        pygame.draw.rect(screen, 'white', null)
        flags = infofont.render(str(self.cur_flags), True, "Black")
        if self.cur_flags < 100 and self.menu_height == 100:
            screen.blit(flags, (0.76*self.rows*self.cell_size, 50))
        else:
            screen.blit(flags, (0.75 * self.rows * self.cell_size, 50))
        numcolor = None
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.board[i][j]
                if cell.flag:
                    color = 'blue'
                elif not cell.showed:
                    color = 'gray'
                elif cell.mine:
                    color ='red'
                else:
                    color = 'white'
                    if cell.neighbours == 1:
                        numcolor = 'black'
                    elif cell.neighbours == 2:
                        numcolor = 'blue'
                    else:
                        numcolor = 'red'
                rect = pygame.Rect(cell.row * self.cell_size + 1, cell.col * self.cell_size + 1+self.menu_height, self.cell_size-2, self.cell_size-2)
                pygame.draw.rect(screen, color, rect)
                if numcolor != None and not cell.flag and cell.showed and not cell.mine and cell.neighbours>0:
                    self.draw_nums(cell,numcolor)

    def win_lose_screen(self):
        if game.lose or game.win:
            wlscreen_outline = pygame.Rect(0.5 * (self.rows * self.cell_size-200), 0.5 * (self.cols * self.cell_size), 200, 80)
            pygame.draw.rect(screen, ['blue','green'][game.win], wlscreen_outline)
            wlscreen = pygame.Rect(0.5 * (self.rows * self.cell_size-190), 0.5 * (self.cols * self.cell_size+10), 190, 70)
            pygame.draw.rect(screen, 'white', wlscreen)
            you_lose = winlosefont.render(['YOU LOSE','YOU WIN'][game.win], True, "Black")
            screen.blit(you_lose, (0.5 * (self.rows * self.cell_size-200)+30, 0.5 * (self.cols * self.cell_size)+20))
    def draw_nums(self,cell,numcolor):
        num = self.gamefont.render(str(cell.neighbours), True, numcolor)
        screen.blit(num, (cell.row * self.cell_size + 1 + self.x_offset, cell.col * self.cell_size + 1+self.menu_height + self.y_offset))

    def draw_board(self):
        info_board = pygame.Rect(0, 0, self.menu_width,self.menu_height)
        pygame.draw.rect(screen, 'green', info_board)
        pygame.draw.rect(screen, 'black', info_board, 4)
        text = infofont.render('SIZE', True, "Black")
        screen.blit(text, (10, 10))
        size = infofont.render(f'{self.rows}X{self.cols}', True, "Black")
        screen.blit(size, (10, 50))
        mines_text = infofont.render('MINES', True, "Black")
        screen.blit(mines_text, (0.4*self.rows*self.cell_size-15, 10))
        mines = infofont.render(str(self.mines), True, "Black")
        screen.blit(mines, (0.4*self.rows*self.cell_size, 50))
        flags_text = infofont.render('FLAGS', True, "Black")
        screen.blit(flags_text, (0.75*self.rows*self.cell_size-15, 10))
        if self.menu_height == 100:
            help_inform = helpfont.render('ESC- go to menu, R-restart', True, "Black")
            screen.blit(help_inform, (0.4*self.rows*self.cell_size-50, 77))
        else:
            help_inform = infofont.render('ESC- go to menu, R-restart', True, "Black")
            screen.blit(help_inform, (0.8*self.rows*self.cell_size-15, 40))
            hell_inform1 = deenomfont.render('YOU WILL LOSE', True, "Black")
            screen.blit(hell_inform1, (150, 5))
            hell_inform2 = deenomfont.render("DON'T EVEN TRY", True, "Black")
            screen.blit(hell_inform2, (860, 5))




        for x in range(0, self.rows*self.cell_size, self.cell_size):
            for y in range(self.menu_height, self.cols*self.cell_size+self.menu_height, self.cell_size):
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, 'black', rect, 1)

    def click(self, row, col, button):
        if button == 1 and not self.board[row][col].showed and not self.board[row][col].flag:
            self.show(row,col)
        if button == 3:
            self.set_flag(row,col)
    def restart(self):
        self.board = [[Cell(j, i) for i in range(self.cols)] for j in range(self.rows)]
        self.win = False
        self.lose = False
        self.started = False
        self.cells_showed = 0
        self.cur_flags = 0
        game.draw_board()


class Menu:
    def draw(self, screen):
        screen.fill((199,199,197))
        text = deenomfont.render('Minesweeper by Deenom',True,"darkgreen")
        screen.blit(text,(50,6.9))
        text = menufont.render('Choose difficulty',True,"black")
        screen.blit(text,(280,140))
        custom_dif = Button(230,220,450,100,"Custom","blue",0)
        custom_dif.draw(screen)
        first_dif = Button(230,350,450,100,"Beginner","green",1)
        first_dif.draw(screen)
        second_dif = Button(230,480,450,100,"Advanced","yellow",2)
        second_dif.draw(screen)
        third_dif = Button(230,610,450,100,"Expert","orange",3)
        third_dif.draw(screen)
        fourth_dif = Button(230,740,450,100,"Master","red",4)
        fourth_dif.draw(screen)
        fifth_dif = Button(230,870,450,100,"Masochist","black",5)
        fifth_dif.draw(screen)
        self.buttons = (custom_dif,first_dif,second_dif,third_dif,fourth_dif,fifth_dif)
    def draw_custom_settings(self,screen):
        screen.fill((199,199,197))
        text = deenomfont.render('Minesweeper by Deenom',True,"darkgreen")
        screen.blit(text,(50,6.9))
        text = menufont.render('Set difficulty',True,"black")
        screen.blit(text,(280,140))
        self.row_set = Button(230,220,400,100,"Rows","blue",20)
        self.row_set.draw(screen,settings_button=True)
        row_minus = Button(self.row_set.x-100,self.row_set.y,100,self.row_set.width,"-","white",action =(self.row_set,'minus'))
        row_plus = Button(self.row_set.x+self.row_set.height,self.row_set.y,100,self.row_set.width, "+", "white",action =(self.row_set,'plus'))
        row_plus.draw(screen)
        row_minus.draw(screen)
        self.col_set = Button(230,350,400,100,"Columns","blue",20)
        self.col_set.draw(screen,settings_button=True)
        col_minus = Button(self.col_set.x-100,self.col_set.y,100,self.col_set.width,"-","white",action =(self.col_set,'minus'))
        col_plus = Button(self.col_set.x+self.col_set.height,self.col_set.y,100,self.col_set.width, "+", "white",action =(self.col_set,'plus'))
        col_plus.draw(screen)
        col_minus.draw(screen)
        self.mine_set = Button(230,480,400,100,"Mines(%)","blue",15)
        self.mine_set.draw(screen,settings_button=True)
        mine_minus = Button(self.mine_set.x-100,self.mine_set.y,100,self.mine_set.width,"-","white",action =(self.mine_set,'minus'))
        mine_plus = Button(self.mine_set.x+self.mine_set.height,self.mine_set.y,100,self.mine_set.width, "+", "white",action =(self.mine_set,'plus'))
        mine_plus.draw(screen)
        mine_minus.draw(screen)
        self.parameter_buttons = [self.row_set,self.col_set,self.mine_set]
        self.settings_buttons = [row_minus,row_plus,col_minus,col_plus,mine_minus,mine_plus]
        self.create = Button(230,870,400,100,"Create","green")
        self.create.draw(screen)
        self.info()

    def action(self,button):
        param_button = button.action[0]
        action = button.action[1]
        if (action == "plus" and param_button.level<50) or (action == "minus" and ((param_button.level>10 and param_button==self.mine_set)or
(param_button.level>7 and param_button!=self.mine_set))):
            if action == "plus":
                param_button.level += 1
            else:
                param_button.level -= 1

    def info(self):
        info_set = (Button(100, 700, 666, 100, "Board", "white", f'{self.row_set.level}x{self.col_set.level}\n\nMines:'
                                                                 f'{self.row_set.level * self.col_set.level * self.mine_set.level // 100}'))
        info_set.draw(screen, settings_button=True)

    def redraw(self,screen):
        for param in self.parameter_buttons:
            param.draw(screen,settings_button=True)
        self.info()



class Button:
    def __init__(self, x, y,height, width, text,color,level=None,action=None):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text
        self.color = color
        self.level = level
        self.action = action

    def draw(self, surface,settings_button = False):
        rect = pygame.Rect(self.x, self.y, self.height,self.width)
        pygame.draw.rect(screen, self.color, rect )
        if not settings_button:
            if self.text in ('+','-'):
                text = deenomfont.render(self.text, True, 'black')
                screen.blit(text, (self.x + self.height * 0.33, self.y + self.width * 0.1))
            elif self.color != "black":
                text =menufont.render(self.text, True, 'black')
                screen.blit(text, (self.x + self.height * 0.33, self.y + self.width * 0.25))
            else:
                text = menufont.render(self.text, True, 'red')
                screen.blit(text, (self.x + self.height*0.33, self.y+self.width * 0.25))
        else:
            text =menufont.render(f'{self.text} : {self.level}', True, 'black')
            screen.blit(text, (self.x + self.height * 0.15, self.y + self.width * 0.25))






pygame.init()
screen = pygame.display.set_mode((900,1040))
pygame.display.set_caption("Minesweeper")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))
infofont = pygame.font.Font("assets/MavenPro-VariableFont_wght.ttf",23)
menufont = pygame.font.Font("assets/MavenPro-VariableFont_wght.ttf",40)
deenomfont = pygame.font.Font("assets/MavenPro-VariableFont_wght.ttf",69)
winlosefont = pygame.font.Font("assets/MavenPro-VariableFont_wght.ttf",33)
helpfont = pygame.font.Font("assets/MavenPro-VariableFont_wght.ttf",15)
menu = Menu()
game = Game(1,1,1,1)
menu.draw(screen)
menu_open = True
game_run = False
game_open = True
custom_run = False
while game_open :
    while menu_open:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_open = False
                game_open = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x,y = pygame.mouse.get_pos()
                for button in menu.buttons:
                    if x in range(button.x, button.x + button.height + 1) and y in range(button.y,
                                                                                    button.y + button.width + 1):
                        if button.level:
                            game = [Game(9, 9, 10, 30), Game(16, 16, 40, 30),
                                Game(30, 16, 100, 30), Game(50, 50, 500, 18),
                                Game(160, 80, 3200, 12)][button.level-1]
                            menu_open = False
                            game_run = True
                            screen = pygame.display.set_mode((game.rows * game.cell_size, game.cols * game.cell_size + game.menu_height))
                            game.draw_board()
                        else:
                            menu_open = False
                            custom_run = True
                            menu.draw_custom_settings(screen)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_open = False
                    game_open = False
                    pygame.quit()
    while custom_run:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                custom_run = False
                game_open = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x in range(menu.create.x, menu.create.x + menu.create.height + 1) and y in range(menu.create.y,
                menu.create.y + menu.create.width + 1):
                    game = (Game(menu.row_set.level, menu.col_set.level,menu.row_set.level*menu.col_set.level*
                menu.mine_set.level//100,min(30,950//menu.col_set.level)))
                    custom_run = False
                    game_run = True
                    screen = pygame.display.set_mode(
                        (game.rows * game.cell_size, game.cols * game.cell_size + game.menu_height))
                    game.draw_board()
                for button in menu.settings_buttons:
                    if x in range(button.x, button.x + button.height + 1) and y in range(button.y,
                    button.y + button.width + 1):
                        menu.action(button)
                        menu.redraw(screen)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((900, 1050))
                    menu.draw(screen)
                    menu_open = True
                    custom_run = False

    while game_run:
        game.draw_cells()
        game.win_lose_screen()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
                game_open = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                row,col = x//game.cell_size,(y-game.menu_height)//game.cell_size
                if -1<row < game.rows and -1<col < game.cols:
                    game.click(row,col,event.button)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((900, 1050))
                    menu.draw(screen)
                    menu_open = True
                    game_run = False
                elif event.key == pygame.K_r:
                    game.restart()

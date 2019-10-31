import pygame
import random
from tkinter import *

class GameBoard():
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rows = screen_height // 20
        self.screen = pygame.display.set_mode([screen_width,screen_height])
        self.screen.fill((0,0,0))

        self.snake = None

        pygame.display.set_caption("Snake Game")

        self.drawGrid(self.screen)



    def redraw(self, screen):
        self.screen.fill((0,0,0))
        self.drawGrid(screen)
        self.snake.draw(screen)
        snack.draw(screen)
        pygame.display.update()


    def drawGrid(self, screen):
        box_width = self.screen_width // self.rows
        x = 0
        y = 0

        for line in range(self.rows):
            x += box_width
            y += box_width

            pygame.draw.line(screen, (255,255,255), (x,0),(x,self.screen_height))
            pygame.draw.line(screen, (255,255,255), (0,y),(self.screen_width, y))

        pygame.display.update()

    def displayMessage(self, message, color):
        text = pygame.font.Font('freesansbold.ttf', 60)
        surface = text.render(message, True, color)
        rect = surface.get_rect()
        rect.center = (self.screen_width/2, self.screen_height/2)
        self.screen.blit(surface, rect)
        pygame.display.update()

    def resetGame():
        pass

class Snake():
    def __init__(self, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position
        self.body = []
        self.turns = {}
        self.head = Box((x_position, y_position))
        self.body.append(self.head)

        self.head.draw(screen)
        # pygame.draw.rect(screen, (0,255,0),[x_position * rows, y_position * rows, 20, 20])
        pygame.display.update()

    def resetSnake(self, position):
        self.body = []
        self.turns = {}
        self.head = Box((position[0], position[1]))
        self.body.append(self.head)
        self.head.draw(screen)
        pygame.display.update()

    def moveSnake(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.direction_y = -1
                self.direction_x = 0
                self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]

            elif keys[pygame.K_DOWN]:
                self.direction_y = 1
                self.direction_x = 0
                self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]

            elif keys[pygame.K_LEFT]:
                self.direction_x = -1
                self.direction_y = 0
                self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]

            elif keys[pygame.K_RIGHT]:
                self.direction_x = 1
                self.direction_y = 0
                self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]

        for index, box in enumerate(self.body):
            position = box.position[:]
            if position in self.turns:
                turn = self.turns[position]
                box.move(turn[0], turn[1])
                if index == len(self.body) - 1:
                    self.turns.pop(position)
            else:
                # else here is if the snake body is not at a turn position
                box.move(box.direction_x, box.direction_y)

    def addBox(self):
        tail = self.body[-1]
        if tail.direction_x == 1:
            self.body.append(Box((tail.position[0] - 1, tail.position[1]), tail.direction_x, tail.direction_y))
        elif tail.direction_x == -1:
            self.body.append(Box((tail.position[0] + 1, tail.position[1]), tail.direction_x, tail.direction_y))
        elif tail.direction_y == 1:
            self.body.append(Box((tail.position[0], tail.position[1] - 1), tail.direction_x, tail.direction_y))
        elif tail.direction_y == -1:
            self.body.append(Box((tail.position[0], tail.position[1] + 1), tail.direction_x, tail.direction_y))

    def draw(self, screen):
        for box in self.body:
            box.draw(screen)

class Box():
    rows = 25
    width = 500

    def __init__(self, position, direction_x = 1, direction_y = 0, color = (0,255,0)):
        self.position = position
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.color = color

    def move(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y
        if direction_x == 1 and (self.position[0] + 1 > rows - 1):
            self.position = (0, self.position[1])
        elif direction_x == -1 and (self.position[0] - 1 < 0):
            self.position = (rows - 1, self.position[1])
        elif direction_y == 1 and (self.position[1] + 1 > rows - 1):
            self.position = (self.position[0], 0)
        elif direction_y == -1 and (self.position[1] - 1 < 0):
            self.position = (self.position[0], rows - 1)
        else:
            self.position = (self.position[0] + self.direction_x, self.position[1] + self.direction_y)

    def draw(self, screen):
        distance = self.width // self.rows
        x = self.position[0]
        y = self.position[1]

        # may want to change some values to be inside the grid
        pygame.draw.rect(screen, self.color, ((x * distance) + 1, (y * distance) + 1, distance - 1, distance - 1))

class PlayAgainWindow():
    def __init__(self):
        self.window = Tk()
        self.var = IntVar(self.window)
        self.play_again = False

        self.window.title("Snake")
        Label(self.window, text = f"Score : {score}").pack(anchor = CENTER)
        Label(self.window, text = "Play Again?").pack(anchor = W)
        Radiobutton(self.window, text="Yes", variable = self.var, value=1).pack(anchor=W)
        Radiobutton(self.window, text="No", variable = self.var, value=2).pack(anchor=W)
        Button(self.window, text="Submit", width = 20, command = self.click).pack(anchor=W)
        self.window.mainloop()

    def click(self):
        var = self.var
        selection = var.get()
        self.window.destroy()
        if selection == 1:
            self.play_again = True
        else:
            self.play_again =  False


def randomSnackLocation(rows, snake):
    body_list = snake.body

    while True:
        x = random.randint(0, rows - 1)
        y = random.randint(0, rows - 1)

        if len(list(filter(lambda box:box.position == (x,y), body_list))) > 0:
            continue
        else:
            break

    return (x,y)

def startGame():
    global screen, rows, snack, score
    pygame.init()

    screen_width = 500
    screen_height = 500
    board = GameBoard(screen_width,screen_height)
    screen = board.screen
    rows = board.rows
    score = 1

    snake = Snake(12, 12)
    board.snake = snake

    snack = Box(randomSnackLocation(rows,snake), color=(255,0,0))

    running = True

    while running:
        pygame.time.delay(100)

        snake.moveSnake()

        if snake.head.position == snack.position:
            snake.addBox()
            snack = Box(randomSnackLocation(rows,snake), color=(255,0,0))

        for box in snake.body[1:]:
            if snake.head.position == box.position:
                score = len(snake.body)
                running = False

        board.redraw(screen)

        if running == False:
            close_window = PlayAgainWindow()
            if close_window.play_again:
                snake.resetSnake((12,12))

    return close_window.play_again

def main():
    play = True
    while play:
        play = startGame()

main()

'''
SNAKE

TODOS:
- Move the snake with arrow keys
- Make the snake longer
- Check it didn't eat itself
- If food eaten -> make longer
-   Spawns again.. not inside the snake.
- Dies when it hits the wall


'''
import sys
import time
import pygame
from enum import Enum
from dataclasses import dataclass
from random import randint

class CellContent(Enum):
    SNAKE = 0
    FOOD = 1
    NOTHING = 2

@dataclass
class PieceOfSnake:
    x: int
    y: int
    x_velocity: int
    y_velocity: int

'''
Draw rect:

pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))

'''
class Snake:
    '''
    Keep track of the pieces of the snake.
    '''
    MODE = "NOT MEME"
    def __init__(self, num_cells):
      
        self.num_cells = num_cells
        snake = PieceOfSnake(10, 12, -1, 0)
        self.parts = [snake]

        self.last_moved_time = 0
    
    def get_position(self):

        # update positions
        current_time = time.time()
        # TODO: Speed it up once we're done coding this thing.
        if current_time - self.last_moved_time >= .1:
            self.last_moved_time = current_time  

            for i in range(len(self.parts)):
                self.parts[i].x = self.parts[i].x + self.parts[i].x_velocity
                self.parts[i].y = self.parts[i].y + self.parts[i].y_velocity

            # [^][<-] 

            # [^]
            # [<-]
            # take the velocity of the one in front of it
            if self.MODE =="MEME":
                for i in range(len(self.parts)-1):
                    self.parts[i+1].x_velocity = self.parts[i].x_velocity
                    self.parts[i+1].y_velocity = self.parts[i].y_velocity
            else:
                for i in reversed (range(len(self.parts)-1)):
                    self.parts[i+1].x_velocity = self.parts[i].x_velocity
                    self.parts[i+1].y_velocity = self.parts[i].y_velocity


        return [(part.x, part.y) for part in self.parts]

    def turn_left(self):
        if not self.parts[0].x_velocity == 1:
            self.parts[0].x_velocity = -1
            self.parts[0].y_velocity = 0
    def turn_right(self):
        if not self.parts[0].x_velocity == -1:
            self.parts[0].x_velocity = 1
            self.parts[0].y_velocity = 0
    def go_up(self):
        if not self.parts[0].y_velocity == 1:
            self.parts[0].y_velocity = -1
            self.parts[0].x_velocity = 0
    def go_down(self):
        if not self.parts[0].y_velocity == -1:
            self.parts[0].y_velocity = 1
            self.parts[0].x_velocity = 0
 
    def grow_snake(self):
        '''
        last_snake --> x=10, y=12, x_vel=-1, y_vel=0
        new_piece -->  x=11=last_snake.x - last_snake.x_vel, y=12, x_vel=-1, y_vel=0

        last_snake --> x=10, y=12, x_vel=+1, y_vel=0
        new_piece -->  x=9=last_snake.x - last_snake.x_vel, y=12, x_vel=-1, y_vel=0

        '''
        
        last_piece = self.parts[-1]
        
        new_piece = PieceOfSnake(
            x=last_piece.x - last_piece.x_velocity, 
            y=last_piece.y - last_piece.y_velocity, 
            x_velocity=last_piece.x_velocity, 
            y_velocity=last_piece.y_velocity
        )
        self.parts.append(new_piece)


class Board:
    '''
    Draw the board and what's on it.
    '''
    def __init__(self):
        self.NUM_CELLS = 20
        self.SNAKE_COLOR = (66, 245, 72)
        self.FOOD_COLOR = (255, 45, 72)


        self.content = [[CellContent.NOTHING for i in range(self.NUM_CELLS)] for j in range(self.NUM_CELLS)]
        self.snake = Snake(self.NUM_CELLS)
        self.content[10][5] = CellContent.FOOD

    def draw_board(self, screen, height, width):

        # Step 1. : Figure out where everything is.

        # [(x1, y1), (x2, y2), . . .]
        snake_position = self.snake.get_position()
        snake_position_set = set(snake_position)
        if not len(snake_position) == len(snake_position_set):
            sys.exit(0)
        if not snake_position[0][0] >= 0 or \
            not snake_position[0][1] >= 0 or \
            not snake_position[0][0] <= self.NUM_CELLS - 1 or\
            not snake_position[0][1] <= self.NUM_CELLS -1:
            
            sys.exit(0)
        
        


        # Step 2 : Draw it.
        for i, row in enumerate(self.content):
            for j, cell in enumerate(row):
                cell_width = width / self.NUM_CELLS
                cell_height = height / self.NUM_CELLS
                cell_x_cord = j * cell_width
                cell_y_cord = i * cell_height
                pygame.draw.rect(screen, (0,0,0), pygame.Rect(cell_x_cord, cell_y_cord, cell_width, cell_height), 1)
                

                cell_is_part_of_the_snake = (j, i) in snake_position
                cell_is_food = cell == CellContent.FOOD
                if cell_is_part_of_the_snake and cell_is_food:    
                    self.snake.grow_snake()
                    self.content[i][j] = CellContent.NOTHING

                    # Pick new food location
                    new_food_x = randint(0, 19)
                    new_food_y = randint(0, 19)
                    while (new_food_y, new_food_x) in snake_position:
                        new_food_x = randint(0, 19)
                        new_food_y = randint(0, 19)

                    self.content[new_food_y][new_food_x] = CellContent.FOOD

                elif cell_is_food:
                    pygame.draw.rect(screen, self.FOOD_COLOR, pygame.Rect(cell_x_cord, cell_y_cord, cell_width, cell_height))
                if cell_is_part_of_the_snake:
                    pygame.draw.rect(screen, self.SNAKE_COLOR, pygame.Rect(cell_x_cord, cell_y_cord, cell_width, cell_height)) 
                
                if cell == CellContent.NOTHING:
                    pass
     
class GameMaster:
    '''
    Create the screen.
    Pick up events.
    Pass the events to the game.
    '''
    def __init__(self):
        pygame.init()
        self.WIN_SIZE = 700
        self.screen = pygame.display.set_mode([self.WIN_SIZE, self.WIN_SIZE])
        self.colour = (255, 255, 255)
        self.board = Board()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.board.snake.turn_left()
                    elif event.key == pygame.K_RIGHT:
                        self.board.snake.turn_right()
                    elif event.key == pygame.K_UP:
                        self.board.snake.go_up()
                    elif event.key == pygame.K_DOWN:
                        self.board.snake.go_down()
                
                if event.type == pygame.QUIT:
                    running = False
            
            self.screen.fill((255, 255, 255))
        
            self.board.draw_board(self.screen,self.WIN_SIZE,self.WIN_SIZE)

            pygame.display.flip()
            
        pygame.quit()


game = GameMaster()
game.run()


    
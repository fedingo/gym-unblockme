try:
    import pygame
    from pygame import gfxdraw
except ImportError as e:
    raise error.DependencyNotInstalled(
        "{}. (HINT: install pygame using `pip install pygame`".format(e))

import time
import numpy as np

gray =  (150, 150, 150)
white = (255, 255, 255)
black = (0,   0,   0, )
red_block = (255, 0, 0)
red_border = (76, 0, 19)
block_color = (255, 128, 0)
border_color = (165,42,42)

screen = None
SIDE = 50
BORDER = 5
MARGIN = 5
LINE = 1

h_switch = True
def __draw_horizontal_block(x,y):

    global screen, h_switch
    pygame.draw.rect(screen, border_color, pygame.Rect(MARGIN + y*SIDE,MARGIN + x*SIDE, SIDE, SIDE))
    pygame.draw.rect(screen, block_color,  pygame.Rect(MARGIN + y*SIDE + h_switch*BORDER, MARGIN + x*SIDE + BORDER,
                                                       SIDE - BORDER, SIDE - 2*BORDER))
    h_switch = not h_switch

def __draw_red_block(x,y):

    global screen, h_switch
    pygame.draw.rect(screen, red_border, pygame.Rect(MARGIN + y*SIDE,MARGIN + x*SIDE, SIDE, SIDE))
    pygame.draw.rect(screen, red_block,  pygame.Rect(MARGIN + y*SIDE + h_switch*BORDER, MARGIN + x*SIDE + BORDER,
                                                       SIDE - BORDER, SIDE - 2*BORDER))
    h_switch = not h_switch

def __draw_vertical_block(x,y):

    global screen
    pygame.draw.rect(screen, border_color, pygame.Rect(MARGIN + y*SIDE, MARGIN + x*SIDE, SIDE, 2*SIDE))
    pygame.draw.rect(screen, block_color,  pygame.Rect(MARGIN + y*SIDE + BORDER, MARGIN + x*SIDE + BORDER,
                                                       SIDE - 2*BORDER, 2*SIDE - 2*BORDER))

## Render function for the unblockme_class
def render_unblockme(game_object):

    matrix = game_object.internal_state
    k, h, _ = game_object.shape

    global screen 
    if screen is None:
        pygame.init()
        screen = pygame.display.set_mode((2*MARGIN+k*SIDE, 2*MARGIN+h*SIDE))

    screen.fill(black)

    # first we draw the background
    for x in range(0,k):
        for y in range(0,h):
            cell = matrix[x,y,:]
            selected_block = np.where(cell == 1)[0]
            if len(selected_block) != 0:
                #draw the exit on the outer border
                if selected_block[0] == 0:
                    if y == 0:
                        pygame.draw.rect(screen, white, pygame.Rect(y*SIDE,x*SIDE+MARGIN, SIDE+MARGIN, SIDE))
                    else:
                        pygame.draw.rect(screen, white, pygame.Rect(y*SIDE+MARGIN,x*SIDE+MARGIN, SIDE+MARGIN, SIDE))
            # Draw the background with the grid pattern
            pygame.draw.rect(screen, gray , pygame.Rect(MARGIN + y*SIDE,MARGIN + x*SIDE, SIDE, SIDE))
            pygame.draw.rect(screen, white, pygame.Rect(MARGIN + y*SIDE + LINE,MARGIN + x*SIDE + LINE,
                                                        SIDE - 2*LINE, SIDE - 2*LINE))
    
    # then we draw the blocks in the grid
    for x in range(0,k):
        for y in range(0,h):
            cell = matrix[x,y,1:]
            selected_block = np.where(cell == 1)[0]     
            if len(selected_block) != 0:     
                if selected_block[-1] == 1:
                    __draw_horizontal_block(x,y)
                elif selected_block[-1] == 2:
                    if (x == 0 or not (matrix[x-1,y,1:] == cell).all() ) and \
                       (x != k-1 and (matrix[x+1,y,1:] == cell).all() ):
                        __draw_vertical_block(x,y)
                elif selected_block[-1] == 0:
                    __draw_red_block(x,y)

    pygame.display.update()

if __name__ == "__main__":
    from unblockme_class import *
    matrix, goal = get_example()
    game = unblock_me(matrix, goal)
    render_unblockme(game)
import pygame
import sys
import time
import tkinter as tk

from gamefiles.source import initial_state,player,result,winner,utility,terminal
from gamefiles.minimax import minimax

X = "X"
O = "O"
EMPTY = None
root = tk.Tk()

pygame.init()
size = width, height = root.winfo_screenwidth(), root.winfo_screenheight()

# Colors
bgimage = pygame.image.load("img.jpg")

background = (255,237,190)
color_x = (0, 77, 77)
color_o = (128, 0, 64)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
board = initial_state()
ai_turn = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # screen.fill(background)
    screen.blit(bgimage,(0,0))

    # Let user choose a player.
    if user is None:

        abc = pygame.Rect((width / 2.5), (height / 12), width / 6, 50)
        ab = pygame.font.SysFont("Segoe UI", 50).render("TIC TAC TOE", True, (0,0,0))
        abd = ab.get_rect()
        abd.center = abc.center
        pygame.draw.rect(screen, (255,237,190), abc)
        screen.blit(ab, abd)
        
        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, background)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, color_x, playXButton)
        screen.blit(playX, playXRect)

        # Draw buttons

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, background)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, color_o, playOButton)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = O

    else:
        screen.fill(background)

        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (2.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, (0, 34, 102), rect, 3) #Rectagle

                if board[i][j] != EMPTY:
                    color = color_o if player(board) == O else color_x
                    if terminal(board):
                        color = (0,0,0)
                    move = moveFont.render(board[i][j], True, color)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = terminal(board)
        plr = player(board)

        # Show title
        if game_over:
            win = winner(board)
            if win is None:
                title = f"Game Over: Draw."
            else:
                title = f"Game Over: You win!." if win == user else f"AI Wins!"
        elif user == plr:
            title = f"Playing as {user}"
        else:
            title = f"AI is calculating..."
        title = largeFont.render(title, True, (0, 34, 102)) #title
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 60)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != plr and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = minimax(board)
                board = result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == plr and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 200, width / 3, 50)
            again = mediumFont.render("Play Again", True, background)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, (0, 34, 102), againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = initial_state()
                    ai_turn = False

    pygame.display.flip()

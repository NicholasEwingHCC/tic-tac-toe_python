import pygame
import numpy as np

pygame.init()

game_window = pygame.display.set_mode((400, 450))
pygame.display.set_caption("Tic-Tac-Toe")

run = True
board = pygame.image.load("assets/tic-tac-toe_board.png")
font = pygame.font.Font("assets/PSS.ttf", 14)
font2 = pygame.font.SysFont("Arial", 12)
new_text = font2.render("New Game", 1, (0,0,0))
squares = [
    pygame.Rect(45, 70, 100, 100), pygame.Rect(150, 70, 100, 100), pygame.Rect(255, 70, 100, 100),
    pygame.Rect(45, 175, 100, 100), pygame.Rect(150, 175, 100, 100), pygame.Rect(255, 175, 100, 100),
    pygame.Rect(45, 280, 100, 100), pygame.Rect(150, 280, 100, 100), pygame.Rect(255, 280, 100, 100)
]

crosses = [[((45, 70), (145, 170)), ((145, 70), (45, 170))], [((150, 70), (250, 170)), ((250, 70), (150, 170))], [((255, 70), (355, 170)), ((355, 70), (255, 170))], [((45, 175), (145, 275)), ((145, 175), (45, 275))], [((150, 175), (250, 275)), ((250, 175), (150, 275))], [((255, 175), (355, 275)), ((355, 175), (255, 275))], [((45, 280), (145, 380)), ((145, 280), (45, 380))], [((150, 280), (250, 380)), ((250, 280), (150, 380))], [((255, 280), (355, 380)), ((355, 280), (255, 380))]]

circles = [(95, 120), (200, 120), (305, 120), (95, 225), (200, 225), (305, 225), (95, 330), (200, 330), (305, 330)]

# 1 is X, 2 is O, 3 is game won
winner = 0
current_turn = 1
moves = 0
cat = False

# 0 is Open, 1 is X, 2 is O
clicked = [0, 0, 0, 0, 0, 0, 0, 0, 0]

def getGameBoard(positions: list):
    game_board = [[], [], []]
    c = 0
    for item in positions:
        if c < 3:
            game_board[0].append(item)
        elif c < 6:
            game_board[1].append(item)
        else:
            game_board[2].append(item)
        c += 1
    return game_board

def checkRows(gameboard: list):
    for row in gameboard:
        if len(set(row)) == 1:
            return row[0]
    return 0

def checkDiagonals(gameboard: list):
    if len(set([gameboard[i][i] for i in range(len(gameboard))])) == 1:
        return gameboard[0][0]
    if len(set([gameboard[i][len(gameboard)-i-1] for i in range(len(gameboard))])) == 1:
        return gameboard[0][len(gameboard) - 1]
    return 0

def checkWin(gameboard: list):
    for item in [gameboard, np.transpose(gameboard)]:
        result = checkRows(item)
        if result:
            return result
    return checkDiagonals(gameboard)

def draw():
    game_window.fill((255, 255, 255))
    game_window.blit(board, (30, 55))

    draw_counter = 0
    for item in clicked:
        if item == 1:
            cross = crosses[draw_counter]
            pygame.draw.line(game_window, (255,0,0), cross[0][0], cross[0][1], 2)
            pygame.draw.line(game_window, (255,0,0), cross[1][0], cross[1][1], 2)
        elif item == 2:
            circle = circles[draw_counter]
            pygame.draw.circle(game_window, (255,0,0), circle, 48, 2)
        draw_counter += 1

    if current_turn == 1:
        text = font.render("Player 1's Turn", 1, (0,0,0))
    elif current_turn == 2:
        text = font.render("Player 2's Turn", 1, (0,0,0))
    elif winner != 0 and current_turn == 3:
        text = font.render(f"Player {winner} wins!", 1, (0,0,0))
        game_window.blit(new_text, (300, 15))
    elif cat == True:
        text = font.render("Cat!", 1, (0,0,0))
        game_window.blit(new_text, (300, 15))
    game_window.blit(text, (110, 5))
    
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.MOUSEBUTTONUP:
            mpos = pygame.mouse.get_pos()
            new_game_rect = pygame.Rect(300, 15, 75, 25)
            for square in squares:
                if square.collidepoint(mpos[0], mpos[1]):
                    click = squares.index(square)
                    if current_turn == 1:
                        if clicked[click] == 0:
                            clicked[click] = 1
                            current_turn = 2
                            moves += 1
                    else:
                        if clicked[click] == 0:
                            clicked[click] = 2
                            current_turn = 1
                            moves += 1
                    if moves > 4:
                        win_state = checkWin(getGameBoard(clicked))
                        if win_state != 0:
                            winner = win_state
                            current_turn = 3
                        else:
                            c = 0
                            for item in clicked:
                                if item != 0:
                                    c += 1
                            if c == 9:
                                cat = True
                                current_turn = 3
                elif new_game_rect.collidepoint(mpos[0], mpos[1]) and (winner != 0 or cat == True):
                    cat = False
                    winner = 0
                    win_state = 0
                    current_turn = 1
                    c = 0
                    moves = 0
                    clicked = [0, 0, 0, 0, 0, 0, 0, 0, 0]  

    draw()
    pygame.display.update()
    
pygame.quit()
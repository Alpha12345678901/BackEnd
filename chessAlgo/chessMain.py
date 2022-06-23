"""driver file, receive user input, and display msg"""
import pygame as p
import chessEngine

WIDTH = HEIGHT = 400
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGE = {}

'''
initialize a global dict of images
    usage: IMAGE["bQ"]
'''
def load_Image():
    pieces = ["bQ", "bK", "bB", "bN", "bR", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        IMAGE[piece] = p.transform.scale(p.image.load("img/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

'''
draw squares and pieces on the board
'''
def drawGameState(screen, gs):
    drawBoard(screen)       # draw square on the board
    drawPieces(screen, gs.board)

'''
draw the squares on the board: light square be even; dark square be odd
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw peices on the board using GameState.board
'''
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGE[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

''' driver code '''
if __name__ == "__main__":
    p.init()

    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    ValidMoves = gs.getValidMoves()
    moveMade = False                            

    load_Image()    
    running = True
    sqSelected = ()                             # keep track of the lask click (row, col)
    playerClick = []                            # keep track of user clicks [(1, 1) --> (3, 1)]
    while running:
        for e in p.event.get():
            if (e.type == p.QUIT):
                running = False
            
            # move piece, by clicking mouse
            elif (e.type == p.MOUSEBUTTONDOWN):
                location = p.mouse.get_pos()    # (x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                # select the same square twice, undo
                if (sqSelected == (row, col)):  
                    sqSelected = ()
                    playerClick = []
                else:
                    sqSelected = (row, col)
                    playerClick.append(sqSelected)
                    # if there is 2 clicks
                    if (len(playerClick) == 2): 
                        move = chessEngine.Move(playerClick[0], playerClick[1], gs.board)

                        for i in range(len(ValidMoves)):
                            if (move == ValidMoves[i]):
                                gs.makeMove(ValidMoves[i])
                                print(move.getChessNotation())
                                moveMade = True
                                sqSelected = ()
                                playerClick = []
                        
                        if (not moveMade):
                            playerClick = [sqSelected]

            elif (e.type == p.KEYDOWN):
                # undo, when 'z' is pressed
                if (e.key == p.K_z):            
                    gs.undoMove()
                    moveMade = True

        if (moveMade):
            ValidMoves = gs.getValidMoves()
            moveMade = False

        clock.tick(MAX_FPS)
        p.display.flip()
        drawGameState(screen,gs)
#Responsible for user input and displaying current game board object
from numpy import squeeze
import pygame as p
import chess_engine

p.init()

WIDTH = HEIGHT = 512
dims = 8
SQ_size = HEIGHT // dims
max_fps = 15
images = {}
pieces = ['wP', "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]

#Adding images to global dictionary and transforming the images to square size slightly under the size of a square for aesthetic
def load_imgs():
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (0.98 * SQ_size, 0.98 * SQ_size))

def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    #initialize gamestate
    gs = chess_engine.game_board()

    #Finding valid moves
    current_valid_moves = gs.valid_moves()
    move_made = False
    load_imgs() #only do this once so that they're in memory
    running = True
    selected_sq = () #keeps track of the last click
    player_clicks = [] #keeps track of player clicks (two tuples: [(6, 4), (4, 4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Mouse Handler
            elif e.type == p.MOUSEBUTTONDOWN:
                # (x, y) location of mouse
                location = p.mouse.get_pos()
                #since board is entire screen, there is no need to reset based off origin
                col = location[0] // SQ_size
                row = location[1] // SQ_size
                #check to see if piece is moved to a different square
                if selected_sq == (row, col):
                    selected_sq = ()
                    player_clicks = []
                else:
                    selected_sq = (row, col)
                    player_clicks.append(selected_sq)
                #check to see if the click was the second click indicating piece has been moved
                if len(player_clicks) == 2:
                    #determine how the board plays the move as well as retain the move log
                    move = chess_engine.move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.convert_notation())
                    print(gs.move_log)
                    #checking validity
                    if move in current_valid_moves:
                        gs.make_move(move)
                        move_made = True
                    selected_sq = ()
                    player_clicks = []
            #Key Handlers
            elif e.type == p.KEYDOWN:
                #Undo button when z is pressed
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True

        #Regenerate current valid moves
        if move_made:
            current_valid_moves = gs.valid_moves()
            move_made = False

        draw_game_board(screen, gs)
        clock.tick(max_fps)
        p.display.flip()

    


#Responsible for all graphics within a current game state.
def draw_game_board(screen, gs):
    draw_squares(screen) #draws squares on board
    #can add in piece highlighting or move suggestions through these later
    draw_pieces(screen, gs.board) #draws pieces on top of squares

#Draws squares on the board
def draw_squares(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(dims):
        for col in range(dims):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col*SQ_size, row*SQ_size, SQ_size, SQ_size))

#Draws pieces on top of the squares on the board using current gs.board variable
#could move this to draw_squares function to do within a single nested loop but
#keeping separate may make it easier to highlight pieces, potential moves, etc (under piece, over square)
def draw_pieces(screen, board):
    for row in range(dims):
        for col in range(dims):
            piece = board[row, col]
            if piece != "--":
                screen.blit(images[piece], p.Rect(col*SQ_size, row*SQ_size, SQ_size, SQ_size))

if __name__ == "__main__":
    main()

    


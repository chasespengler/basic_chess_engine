#Responsible for user input and displaying current game board object
from operator import invert
from re import S
from matplotlib.pyplot import text
from numpy import squeeze
import pygame as p
import chess_engine
import chess_ai

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
    #Animation toggle, Undo toggle taken as user input (needs to be implemented)
    enable_animation = True
    enable_undo = True

    #Loading screen flag
    loading_screen = True

    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    p.display.set_caption("Chase's Chess")

    loading_screen, p1, p2 = title_screen(screen, clock)
    player_one = True if p1 != "bot" else False
    player_two = True if p2 != "bot" else False

    if not loading_screen:
        play_game(screen, player_one, player_two, clock, enable_undo, enable_animation)

#Loading screen function
def title_screen(screen, clock):
    running = True
    loading_screen = True
    #width of title screen
    w = WIDTH // 2 + 10
    #height of title screen
    h = HEIGHT // 2 + 10
    #left side distance from left
    x_loc = (WIDTH - w) // 2
    #right side distance from left
    x_end = x_loc + w
    #top distance from top
    y_loc = (HEIGHT - h) // 2
    #bottom distance from top
    y_end = y_loc + h
    #Whether each player will be played by a human
    player_1 = True
    player_2 = True
    #The color each player will be playing
    color_1 = "white"
    color_2 = "black"
    #Printing screen
    draw_squares(screen)
    p.draw.rect(screen, p.Color("dark blue"), p.Rect(x_loc - 2, y_loc - 2, w, h), w, 25)
    p.draw.rect(screen, p.Color("light blue"), p.Rect(x_loc, y_loc, w, h), w, 25)
    #Creating and printing buttons
    play_as1 = button(screen, "Player 1", "Play as white", x_loc + 30, y_loc + 40, 100, 30, True, False)
    play_as1.draw_button()
    play_as2 = button(screen, "Player 2", "Play as black", x_end - 130, y_loc + 40, 100, 30, True, True)
    play_as2.draw_button()
    start_button = button(screen, "", "START GAME", x_loc + 29, y_end - 65, w - 58, 40, True, False)
    start_button.draw_button()


    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Mouse Handler
            elif e.type == p.MOUSEBUTTONDOWN:
                # (x, y) location of mouse
                location = p.mouse.get_pos()
                if play_as1.is_clicked(location):
                    play_as1.change_button()
                    play_as1.draw_button()
                    play_as1.update_player()
                #current_color = play_as1.
                elif play_as2.is_clicked(location):
                    play_as2.change_button()
                    play_as2.draw_button()
                    play_as2.update_player()
                elif start_button.is_clicked(location):
                    p1, p2, playable = check_players(play_as1.player, play_as2.player)
                    if playable:
                        loading_screen = False
                        running = False
                    else:
                        start_button.title = "Select valid matchup"
                        start_button.draw_button()

            clock.tick(max_fps)
            p.display.flip()


    return loading_screen, p1, p2

#Checks for player assignments, returns player 1's color, player 2's color, and if the matchup is playable i.e. not white vs white or black vs black
def check_players(p1, p2):
    if p1 != p2 or p1 == "bot":
        return p1, p2, True
    else:
        return p1, p2, False


#Main game function
def play_game(screen, player_one, player_two, clock, enable_undo, enable_animation, bot_level = 0):
    #Initialize gamestate
    screen.fill(p.Color("white"))
    gs = chess_engine.game_board()

    #Finding valid moves
    current_valid_moves = gs.valid_moves()
    move_made = False
    load_imgs() #only do this once so that they're in memory
    running = True
    selected_sq = () #keeps track of the last click
    player_clicks = [] #keeps track of player clicks (two tuples: [(6, 4), (4, 4)])

    #Used to determine when game is over
    playing = True
    reset = False

    while running:
        for e in p.event.get():
            humans_turn = (gs.white_turn and player_one) or (gs.black_turn and player_two)
            if e.type == p.QUIT:
                running = False
            #Mouse Handler
            elif e.type == p.MOUSEBUTTONDOWN:
                # (x, y) location of mouse
                location = p.mouse.get_pos()

                if playing and humans_turn:
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
                        #checking validity
                        for i in range(len(current_valid_moves)):
                            if move == current_valid_moves[i]:
                                gs.make_move(current_valid_moves[i])
                                undo = False
                                move_made = True
                                selected_sq = ()
                                player_clicks = []
                        #added to minimize number of clicks when trying to make move
                        #player can now change selected piece without needing to deselect current piece
                        if not move_made:
                            player_clicks = [selected_sq]

            #Key Handlers
            elif e.type == p.KEYDOWN:
                #Undo button when z is pressed
                if e.key == p.K_z and enable_undo:
                    gs.undo_move()
                    undo = True
                    move_made = True
                #Resets board when r is pressed
                elif e.key == p.K_r:
                    gs = chess_engine.game_board()
                    current_valid_moves = gs.valid_moves()
                    selected_sq = ()
                    player_clicks = []
                    move_made = False
                    reset = True

            #AI Moves
            if playing and not humans_turn:
                #if (gs.white_turn and not player_one) or (gs.black_turn and not player_two):
                bot_move = chess_ai.random_move(current_valid_moves)
                gs.make_move(bot_move)
                move_made = True
                undo = False

            #Regenerate current valid moves and animate
            if move_made:
                if enable_animation and not undo:
                    animate(screen, gs.move_log[-1], gs.board, clock)
                current_valid_moves = gs.valid_moves()
                move_made = False

            draw_game_board(screen, gs, current_valid_moves, selected_sq)

            #Checking for stalemate and checkmate
            if gs.stalemate:
                draw_text(screen, "Stalemate", 0)
                playing = False
            elif gs.white_checkmate:
                draw_text(screen, "Black wins by checkmate", 0)
                playing = False
            elif gs.black_checkmate:
                draw_text(screen, "White wins by checkmate", 0)
                playing = False

            '''
            #Posts "RESET" to the screen and fades out
            if reset:
                reset = False
                for i in range(255, 0, -5):
                    p.event.post(draw_text(screen, "RESET", i))
            '''
            clock.tick(max_fps)
            p.display.flip()

#Responsible for all graphics within a current game state.
def draw_game_board(screen, gs, valid_moves, selected_sq):
    draw_squares(screen) #draws squares on board
    highlight_sq(screen, gs, valid_moves, selected_sq) #highlights pieces and their moves as well as last move
    draw_pieces(screen, gs.board) #draws pieces on top of squares

#Draws squares on the board
def draw_squares(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(dims):
        for col in range(dims):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col*SQ_size, row*SQ_size, SQ_size, SQ_size))

#Draws text on screen
def draw_text(screen, text, opacity):
    font = p.font.SysFont("Helvitca", 45, True, False)
    text_object = font.render(text, opacity, p.Color("Red"))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2, HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, opacity, p.Color("Blue"))
    screen.blit(text_object, text_location.move(2, 2))

#Draws pieces on top of the squares on the board using current gs.board variable
#could move this to draw_squares function to do within a single nested loop but
#keeping separate may make it easier to highlight pieces, potential moves, etc (under piece, over square)
def draw_pieces(screen, board):
    for row in range(dims):
        for col in range(dims):
            piece = board[row, col]
            if piece != "--":
                screen.blit(images[piece], p.Rect(col*SQ_size, row*SQ_size, SQ_size, SQ_size))

#Highlights user's selected piece and its moves
def highlight_sq(screen, gs, valid_moves, selected_sq):
    #Shading last move
    if gs.move_log:
        s = p.Surface((SQ_size, SQ_size))
        s.set_alpha(65)
        s.fill(p.Color('blue'))
        e = p.Surface((SQ_size, SQ_size))
        e.set_alpha(65)
        e.fill(p.Color('red'))
        last_move = gs.move_log[-1]
        screen.blit(s, (last_move.start_col * SQ_size, last_move.start_row * SQ_size))
        screen.blit(e, (last_move.end_col * SQ_size, last_move.end_row * SQ_size))
    
    if selected_sq != ():
        r, c = selected_sq
        if gs.board[r][c][0] == ("w" if gs.white_turn else "b"):
            #Creating a "highlight" square
            s = p.Surface((SQ_size, SQ_size))
            #Setting transparency (0-255)
            s.set_alpha(85)
            #Setting color
            s.fill(p.Color('green'))
            #Placing square
            screen.blit(s, (c * SQ_size, r * SQ_size))
            #Highlighting moves
            m = s
            m.fill(p.Color('gold'))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    if move.is_castle:
                        m.fill(p.Color('purple'))
                    screen.blit(m, (move.end_col * SQ_size, move.end_row * SQ_size))

#Move animation
#Could make more efficient by redrawing only the squares covered by the move rather than whole board
def animate(screen, move, board, clock):
    global colors
    delta_r = move.end_row - move.start_row
    delta_c = move.end_col - move.start_col
    fpsquare = 10
    total_frames = int(((abs(delta_c) ** 2 + abs(delta_r) ** 2) ** 0.5) * fpsquare // 1)
    for frame in range(total_frames + 1):
        r, c = (move.start_row + delta_r * frame / total_frames, move.start_col + delta_c * frame / total_frames)
        draw_squares(screen)
        draw_pieces(screen, board)
        #Piece drawn on end square in draw pieces, needs to be erased
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQ_size, move.end_row * SQ_size, SQ_size, SQ_size)
        p.draw.rect(screen, color, end_square)
        #Replacing any captured piece that was removed in the move
        if move.piece_captured != "--":
            screen.blit(images[move.piece_captured], end_square)
        #Drawing moving piece
        screen.blit(images[move.piece_moved], p.Rect(c * SQ_size, r * SQ_size, SQ_size, SQ_size))
        clock.tick(60)
        p.display.flip()

#Creates buttons for title screen
class button():
    def __init__(self, screen, title, text, x, y, w, h, is_default, invert_colors):
        self.text = text
        self.title = title
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.id = x * 1000 + y * 100 + w * 10 + h
        self.partners = []
        self.is_default = is_default
        self.screen = screen
        self.invert_colors = invert_colors
        self.player = "black" if self.invert_colors else "white"
        self.colors = [p.Color("black"), p.Color("white"), p.Color("dark gray")] if self.invert_colors else [p.Color("white"), p.Color("black"), p.Color("dark gray")]
        self.background_color = self.colors[1]
        self.current_color = self.colors[0]


    #For comparison
    def __eq__(self, other):
        if isinstance(other, button):
            return self.id == other.id

    #Adds partner buttons for radio
    def add_partner(self, button_id):
        self.partners.append(button_id)

    #Draws the button
    def draw_button(self):
        size = 60
        font = p.font.SysFont("Helvitca", size, True, False)
        text_object = font.render(self.text, 0, self.background_color)
        #Adjusting sizing
        while text_object.get_width() > self.w - 5:
            size -= 1
            font = p.font.SysFont("Helvitca", size, True, False)
            text_object = font.render(self.text, 0, self.background_color)
        
        title_font = p.font.SysFont("Helvitca", 20, True, False)
        title_object = title_font.render(self.title, 0, p.Color('black'))
        center_x = self.x + text_object.get_width() // 2
        center_y = self.y + text_object.get_height() // 2
        text_location = p.Rect(self.x + 5, self.y + 5, self.w - 10, self.y - 10)
        title_location = p.Rect(self.x + 5, self.y - 15, self.w - 10, self.y - 10)
        p.draw.rect(self.screen, self.background_color, p.Rect(self.x - 1, self.y - 1, self.w, self.h))
        p.draw.rect(self.screen, self.current_color, p.Rect(self.x, self.y, self.w, self.h))
        self.screen.blit(text_object, text_location)
        self.screen.blit(title_object, title_location)

    #Determines if a button is clicked
    def is_clicked(self, location):
        if self.x < location[0] < self.x + self.w and self.y < location[1] < self.y + self.h:
            return True
        else:
            return False

    def change_button(self):
        self.rotate_colors()
        self.current_color = self.colors[0]
        if self.current_color == p.Color("white"):
            self.text = "Play as white"
            self.background_color = p.Color("black")
        elif self.current_color == p.Color("dark gray"):
            self.text = "Play as bot"
            self.background_color = p.Color("black")
        else:
            self.text = "Play as black"
            self.background_color = p.Color("white")

    def rotate_colors(self):
        self.colors = self.colors[1:] + self.colors[:1]
    
    def update_player(self):
        if self.current_color == p.Color("white"):
            self.player = "white"
        elif self.current_color == p.Color("black"):
            self.player = "black"
        else:
            self.player = "bot"

        
if __name__ == "__main__":
    main()

    


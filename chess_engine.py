#Responsible for storing all info about current state of game and current valid moves and move log
from re import L
import numpy as np

class game_board():
    def __init__(self):
        #8x8 2d np array of two char string where first indicates color piece and second indicates piece type
        #where -- is empty space
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])

        self.white_turn = True
        self.black_turn = False
        self.white_qs_castleability = True
        self.white_ks_castleability = True
        self.black_qs_castleability = True
        self.black_ks_castleability = True
        self.white_in_check = False
        self.black_in_check = False
        self.white_king_loc = (7, 4)
        self.black_king_loc = (0, 4)
        self.white_checks = []
        self.black_checks = []
        self.white_pins = []
        self.black_pins = []
        self.move_log = []
        #Maps letters of piece type to a function that calls the piece's moves
        self.move_function = {"P": self.pawn_moves, "R": self.rook_moves, "N": self.knight_moves, "B": self.bishop_moves, "Q": self.queen_moves, "K": self.king_moves}

    #Basic move function (will not work for castling, en passant, or pawn promotion)
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_turn = not self.white_turn
        self.black_turn = not self.black_turn
        self.black_checks = []
        self.black_pins = []
        self.white_checks = []
        self.white_pins = []
        self.white_in_check = False
        self.black_in_check = False
        #Adjusting ability to castle
        if self.white_ks_castleability or self.white_qs_castleability:
            if move.piece_moved == "wK":
                self.white_ks_castleability = False
                self.white_qs_castleability = False
            elif move.start_row == 7 and move.start_col == 0:
                self.white_ks_castleability = False
            elif move.start_row == 7 and move.start_col == 7:
                self.white_qs_castleability = False
        if self.black_ks_castleability or self.black_qs_castleability:
            if move.piece_moved == "bK":
                self.black_ks_castleability = False
                self.black_qs_castleability = False
            elif move.start_row == 0 and move.start_col == 0:
                self.black_ks_castleability = False
            elif move.start_row == 0 and move.start_col == 7:
                self.black_qs_castleability = False
        #Updating king location
        if move.piece_moved == "wK":
            self.white_king_loc = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_loc = (move.end_row, move.end_col)

        

    def undo_move(self):
        if len(self.move_log) > 0:
            last_move = self.move_log.pop()
            self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
            self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
            self.white_turn = not self.white_turn
            self.black_turn = not self.black_turn
            #Updating king location
            if last_move.piece_moved == "wK":
                self.white_king_loc = (last_move.start_row, last_move.start_col)
            elif last_move.piece_moved == "bK":
                self.black_king_loc = (last_move.start_row, last_move.start_col)
            self.black_checks = []
            self.black_pins = []
            self.white_checks = []
            self.white_pins = []

    #Adds possible moves for the pawn at passed location to moves list
    def pawn_moves(self, r, c, moves):
        if self.board[r][c][0] == "w":
            if self.board[r-1][c] == "--":
                moves.append(move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c]:
                    moves.append(move((r, c), (r-2, c), self.board))
            #Ensuring diagonal move is within space of board
            if (c + 1) < 8 and (c - 1) >= 0:
                #Ensuring that there is a piece diagonal to capture and that it is a black piece
                if self.board[r-1][c+1][0] == "b":
                    moves.append(move((r, c), (r-1, c+1), self.board))
                if self.board[r-1][c-1][0] == "b":
                    moves.append(move((r, c), (r-1, c-1), self.board))
        elif self.board[r][c][0] == "b":
            if self.board[r+1][c] == "--":
                moves.append(move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c]:
                    moves.append(move((r, c), (r+2, c), self.board))
            #Ensuring diagonal move is within space of board
            if (c + 1) < 8 and (c - 1) >= 0:
                #Ensuring that there is a piece diagonal to capture and that it is a white piece
                if self.board[r+1][c+1][0] == "w":
                    moves.append(move((r, c), (r+1, c+1), self.board))
                if self.board[r+1][c-1][0] == "w":
                    moves.append(move((r, c), (r+1, c-1), self.board))      

    #Adds possible moves for the rook at passed location to moves list
    #could definitely be made more efficient, same with bishop function (loop through a tuple of vectors like with knight logic)
    def rook_moves(self, r, c, moves):
        #Vertical up
        i = 1
        #Check to ensure that rook isn't already on the top rank
        if r > 0:
            while i < 8:
                #Check to ensure move is within the board dims
                if r - i < 0:
                    break
                #Open space move
                elif self.board[r-i][c] == "--":
                    moves.append(move((r, c), (r-i, c), self.board))
                #White capture move
                elif self.board[r-i][c][0] == "b" and self.white_turn:
                    moves.append(move((r, c), (r-i, c), self.board))
                    break
                #Black capture move
                elif self.board[r-i][c][0] == "w" and self.black_turn:
                    moves.append(move((r, c), (r-i, c), self.board))
                    break
                #Check for own piece (only other alternative at this point)
                else:
                    break
                i += 1

        #Vertical down
        i = 1
        #Check to ensure that rook isn't already on the bottom rank
        if r < 7:
            while i < 8:
                #Check to ensure move is within the board dims
                if r + i > 7:
                    break
                #Open space move
                elif self.board[r+i][c] == "--":
                    moves.append(move((r, c), (r+i, c), self.board))
                #White capture move
                elif self.board[r+i][c][0] == "b" and self.white_turn:
                    moves.append(move((r, c), (r+i, c), self.board))
                    break
                #Black capture move
                elif self.board[r+i][c][0] == "w" and self.black_turn:
                    moves.append(move((r, c), (r+i, c), self.board))
                    break
                #Check for own piece (only other alternative at this point)
                else:
                    break
                i += 1
        #Horizontal right
        i = 1
        #Check to ensure that rook isn't already on the furthest right file
        if c < 7:
            while i < 8:
                #Check to ensure move is within the board dims
                if c + i > 7:
                    break
                #Open space move
                elif self.board[r][c+i] == "--":
                    moves.append(move((r, c), (r, c+i), self.board))
                #White capture move
                elif self.board[r][c+i][0] == "b" and self.white_turn:
                    moves.append(move((r, c), (r, c+i), self.board))
                    break
                #Black capture move
                elif self.board[r][c+i][0] == "w" and self.black_turn:
                    moves.append(move((r, c), (r, c+i), self.board))
                    break
                #Check for own piece (only other alternative at this point)
                else:
                    break
                i += 1
        #Horizontal left
        i = 1
        #Check to ensure that rook isn't already on the furthest left file
        if c > 0:
            while i < 8:
                #Check to ensure move is within the board dims
                if c - i < 0:
                    break
                #Open space move
                elif self.board[r][c-i] == "--":
                    moves.append(move((r, c), (r, c-i), self.board))
                #White capture move
                elif self.board[r][c-i][0] == "b" and self.white_turn:
                    moves.append(move((r, c), (r, c-i), self.board))
                    break
                #Black capture move
                elif self.board[r][c-i][0] == "w" and self.black_turn:
                    moves.append(move((r, c), (r, c-i), self.board))
                    break
                #Check for own piece (only other alternative at this point)
                else:
                    break
                i += 1    
            

    #Adds possible moves for the knight at passed location to moves list
    def knight_moves(self, r, c, moves):
        #Potential knight move vectors
        vectors = ((2, -1), (2, 1), (-2, 1), (-2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2))
        #Looping through potential moves
        for vect in vectors:
            #Assigning ending position location to variable
            end_pos = (r + vect[0], c + vect[1])
            #Ensuring ending position is still on the board
            if end_pos[0] < 0 or end_pos[0] > 7 or end_pos[1] > 7 or end_pos[1] < 0:
                continue
            #Checking that ending position is not white's own piece
            elif self.board[end_pos[0], end_pos[1]][0] == "w" and self.white_turn:
                continue
            #Checking that ending position is not black's own piece
            elif self.board[end_pos[0], end_pos[1]][0] == "b" and self.black_turn:
                continue
            else:
                moves.append(move((r, c), (end_pos[0], end_pos[1]), self.board))

    #Adds possible moves for the bishop at passed location to moves list
    def bishop_moves(self, r, c, moves):
        #Up and to the right
        i = 1
        while i < 8:
            #Checking for column and row viability
            if c + i > 7:
                break
            elif r - i < 0:
                break
            else:
                #Blank space
                if self.board[r-i][c+i] == "--":
                    moves.append(move((r, c), (r-i, c+i), self.board))
                #White capture move
                elif self.board[r-i][c+i][0] == "b" and self.white_turn:
                    moves.append(move((r, c), (r-i, c+i), self.board))
                #Black capture move
                elif self.board[r-i][c+i][0] == "w" and self.black_turn:
                    moves.append(move((r, c), (r-i, c+i), self.board))
                else:
                    break
            i += 1

        #Up and to the left
        i = 1
        while i < 8:
            if c - i < 0:
                break
            elif r - i < 0:
                break
            else:
                #Blank space
                if self.board[r-i][c-i] == "--":
                    moves.append(move((r, c), (r-i, c-i), self.board))
                #White capture move
                elif self.board[r-i][c-i][0] == "b" and self.white_turn:
                    moves.append(move((r, c), (r-i, c-i), self.board))
                #Black capture move
                elif self.board[r-i][c-i][0] == "w" and self.black_turn:
                    moves.append(move((r, c), (r-i, c-i), self.board))
                else:
                    break
            i += 1

        #Down and to the left
        i = 1
        while i < 8:
            if c - i < 0:
                break
            elif r + i > 7:
                break
            else:
                #Blank space
                if self.board[r+i][c-i] == "--":
                    moves.append(move((r, c), (r+i, c-i), self.board))
                elif self.board[r+i][c-i][0] == "b" and self.white_turn:
                    moves.append(move((r, c), (r+i, c-i), self.board))
                #Black capture move
                elif self.board[r+i][c-i][0] == "w" and self.black_turn:
                    moves.append(move((r, c), (r+i, c-i), self.board))
                else:
                    break
            i += 1

        #Down and to the right
        i = 1
        while i < 8:
            if c + i > 7:
                break
            elif r + i > 7:
                break
            else:
                #Blank space
                if self.board[r+i][c+i] == "--":
                    moves.append(move((r, c), (r+i, c+i), self.board))
                elif self.board[r+i][c+i][0] == "b" and self.white_turn:
                    moves.append(move((r, c), (r+i, c+i), self.board))
                #Black capture move
                elif self.board[r+i][c+i][0] == "w" and self.black_turn:
                    moves.append(move((r, c), (r+i, c+i), self.board))
                else:
                    break
            i += 1              
    
    #Adds possible moves for the queen at passed location to moves list
    def queen_moves(self, r, c, moves):
        self.rook_moves(r, c, moves)
        self.bishop_moves(r, c, moves)

    #Adds possible moves for the king at passed location to moves list
    def king_moves(self, r, c, moves):
        vectors = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1))
        #Looping through potential moves
        for vect in vectors:
            #Assigning ending position location to variable
            end_pos = (r + vect[0], c + vect[1])
            #Ensuring ending position is still on the board
            if end_pos[0] < 0 or end_pos[0] > 7 or end_pos[1] > 7 or end_pos[1] < 0:
                continue
            #Checking that ending position is not white's own piece
            elif self.board[end_pos[0], end_pos[1]][0] == "w" and self.white_turn:
                continue
            #Checking that ending position is not black's own piece
            elif self.board[end_pos[0], end_pos[1]][0] == "b" and self.black_turn:
                continue
            else:
                moves.append(move((r, c), (end_pos[0], end_pos[1]), self.board))

    #Checks for checks and pins and then adds the location of any piece threatening check or any pinned piece to the appropriate list
    def check_for_checks(self):
        vectors = ((1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1))
        if self.white_turn:
            r = self.white_king_loc[0]
            c = self.white_king_loc[1]
        else:
            r = self.black_king_loc[0]
            c = self.black_king_loc[1]
        
        for vect in vectors:
            #Variables used to help determine pins
            #If there's a single white piece beyond the king in a given direction there may be a pin
            #If there's two then there are no pins in that direction
            first_piece = True
            for i in range(1, 8):
                end_pos = (r + vect[0] * i, c + vect[1] * i)
                #Checking to ensure end position is within the board
                if 0 <= end_pos[0] <= 7 and 0 <= end_pos[1] <= 7:
                    occupant = self.board[end_pos[0], end_pos[1]]
                    if occupant == "--":
                        continue
                    elif occupant[0] == "w" and self.white_turn:
                        if first_piece:
                            first_piece = False
                            pin_pos = end_pos
                            continue
                        else:
                            break
                    elif occupant[0] == "b" and self.black_turn:
                        if first_piece:
                            first_piece = False
                            pin_pos = end_pos
                            continue
                        else:
                            break
                    #White's turn
                    elif self.white_turn:
                        #Checking for horizontal and vertical attacking pieces
                        if r == end_pos[0] or c == end_pos[1]:
                            if occupant == "bR" or occupant == "bQ":
                                if first_piece:
                                    self.white_checks.append(end_pos)
                                    self.white_in_check = True
                                    break
                                else:
                                    self.white_pins.append(pin_pos)
                                    break
                        #Checking for attacking pawns
                        elif i == 1 and occupant == "bP" and r == end_pos[0] + 1:
                            if c - 1 == end_pos[1] or c + 1 == end_pos[1]:
                                self.white_checks.append(end_pos)
                                self.white_in_check = True
                                break
                        #Diagonal attacking pieces
                        else:
                            if occupant == "bB" or occupant == "bQ":
                                if first_piece:
                                    self.white_checks.append(end_pos)
                                    self.white_in_check = True
                                    break
                                else:
                                    self.white_pins.append(pin_pos)
                                    break
                    #Black's turn
                    else:
                        #Horizontals and verticals
                        if r == end_pos[0] or c == end_pos[1]:
                            if occupant == "wR" or occupant == "wQ":
                                if first_piece:
                                    self.black_checks.append(end_pos)
                                    self.black_in_check = True
                                    break
                                else:
                                    self.black_pins.append(pin_pos)
                                    break
                        #Attacking pawns
                        elif i == 1 and occupant == "wP" and r == end_pos[0] - 1:
                            if c - 1 == end_pos[1] or c + 1 == end_pos[1]:
                                self.black_checks.append(end_pos)
                                self.black_in_check = True
                                break
                        #Diagonals
                        else:
                            if occupant == "wB" or occupant == "wQ":
                                if first_piece:
                                    self.black_checks.append(end_pos)
                                    self.black_in_check = True
                                    break
                                else:
                                    self.black_pins.append(pin_pos)
                                    break
        
        #Knight checks
        vectors = ((2, -1), (2, 1), (-2, 1), (-2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2))
        for vect in vectors:
            end_pos = (r + vect[0], c + vect[1])
            if 0 <= end_pos[0] <= 7 and 0 <= end_pos[1] <= 7:
                occupant = self.board[end_pos[0], end_pos[1]]
                if self.white_turn and occupant == "bN":
                    self.white_in_check = True
                    self.white_checks.append(end_pos)
                elif self.black_turn and occupant == "wN":
                    self.black_in_check = True
                    self.black_checks.append(end_pos)

    #Function to check if a given square is underattack on a given color's turn
    def under_attack(self, r, c):
        vectors = ((-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
        for j in range(0, len(vectors)):
            vect = vectors[j]
            for i in range(1, 8):
                end_pos = (r + vect[0] * i, c + vect[1] * i)
                if 0 <= end_pos[0] <=7 and 0 <= end_pos[1] <= 7:
                    piece = self.board[end_pos[0], end_pos[1]]
                    if piece == "--":
                        continue
                    elif self.white_turn and piece[0] == "w":
                        break
                    elif self.black_turn and piece[0] == "b":
                        break
                    elif self.white_turn and j < 4:
                        if piece == "bQ" or piece == "bR":
                            return True
                    elif self.white_turn and j >= 4:
                        if piece == "bQ" or piece == "bB":
                            return True
                        elif piece == "bP" and j >= 6 and i == 1:
                            return True
                    elif self.black_turn and j < 4:
                        if piece == "wQ" or piece == "wR":
                            return True   
                    elif self.black_turn and j >= 4:
                        if piece == "wQ" or piece == "wB":
                            return True
                        elif piece == "wP" and j < 6 and i == 1:
                            return True
                else:
                    break

        vectors = ((2, -1), (2, 1), (-2, 1), (-2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2))
        for vect in vectors:
            end_pos = (r + vect[0], c + vect[1])
            if 0 <= end_pos[0] <= 7 and 0 <= end_pos[1] <= 7:
                piece = self.board[end_pos[0], end_pos[1]]
                if self.white_turn and piece == "bN":
                    return True
                elif self.black_turn and piece == "wN":
                    return True

        return False
            


    #Takes all possible moves and then checks to ensure that any that result
    #in the player being in check are removed
    def valid_moves(self):
        self.check_for_checks()
        current_moves = self.possible_moves()   
        if self.white_in_check:
            #Ensure that all moves resulting in white still being in check are removed
            i = len(current_moves) - 1
            while i >= 0:
                current_move = current_moves[i]
                self.make_move(current_move)
                self.white_turn = not self.white_turn
                self.black_turn = not self.black_turn
                self.check_for_checks()
                if self.white_in_check:
                    z = current_moves.pop(i)
                self.white_turn = not self.white_turn
                self.black_turn = not self.black_turn
                self.undo_move()
                self.check_for_checks()
                i -= 1
                
        elif self.black_in_check:
            #Ensure that all moves resulting in black still being in check are removed
            i = len(current_moves) - 1
            while i >= 0:
                current_move = current_moves[i]
                self.make_move(current_move)
                self.white_turn = not self.white_turn
                self.black_turn = not self.black_turn
                self.check_for_checks()
                if self.white_in_check:
                    z = current_moves.pop(i)
                self.white_turn = not self.white_turn
                self.black_turn = not self.black_turn
                self.undo_move()
                self.check_for_checks()
                i -= 1

        if len(self.white_pins) and self.white_turn > 0:
            #Remove all moves made by the pinned piece
            i = len(current_moves) - 1
            for pin in self.white_pins:
                while i >= 0:
                    if pin[0] == current_moves[i].start_row and pin[1] == current_moves[i].start_col:
                        z = current_moves.pop(i)
                    i -= 1

        elif len(self.black_pins) and self.black_turn > 0:
            #Remvoe all moves made by the pinned piece
            i = len(current_moves) - 1
            for pin in self.black_pins:
                while i >= 0:
                    if pin[0] == current_moves[i].start_row and pin[1] == current_moves[i].start_col:
                        z = current_moves.pop(i)
                    i -= 1

        #Add Castling
        if self.white_ks_castleability:
            pass

        #Add en passant

        #Add pawn promotion...somewhere...but not here

        #Pass this logic to main to end game
        #Checking for stalemate
        if len(current_moves) == 0 and (not self.white_in_check or not self.black_in_check):
            print("stalemate")
        #Checkmate
        elif len(current_moves) == 0 and (self.white_in_check or self.black_in_check):
            print("checkmate")
            if self.white_in_check:
                print("Black wins")
            else:
                print("White wins")
        

        return current_moves

    def possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.white_turn and self.board[r][c][0] == "w":
                    piece = self.board[r][c][1]
                    self.move_function[piece](r, c, moves)
                            
                elif self.black_turn and self.board[r][c][0] == "b":
                    piece = self.board[r][c][1]
                    self.move_function[piece](r, c, moves)
        #unfucking code
        all_moves = []
        for val in moves:
            all_moves.append(("Piece: ", val.piece_moved, " Start: ", val.start_row, val.start_col, " End: ", val.end_row, val.end_col))
        print(all_moves)
        return moves


                    


class move():
    #Adding dictionaries for ease of logging moves/positions in chess notation
    ranks_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_ranks = {v: k for k, v in ranks_rows.items()}
    files_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_files = {v: k for k, v in files_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    #To enable comparison between objects (like checking for valid moves)
    def __eq__(self, other):
        if isinstance(other, move):
            return self.move_id == other.move_id

    #Converts the row and column pair to chess notation
    def convert_notation(self):
        return self.get_rankfile(self.start_row, self.start_col) + self.get_rankfile(self.end_row, self.end_col)

    #Accesses the dictionary and returns the rank and file based on row and column values
    def get_rankfile(self, r, c):
        return self.cols_files[c] + self.rows_ranks[r]
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
        self.white_castlability = True
        self.black_castleability = True
        self.move_log = []
        #maps letters of piece type to a function that calls the piece's moves
        self.move_function = {"P": self.pawn_moves, "R": self.rook_moves, "N": self.knight_moves, "B": self.bishop_moves, "Q": self.queen_moves, "K": self.king_moves}

    #basic move function (will not work for castling, en passant, or pawn promotion)
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_turn = not self.white_turn
        self.black_turn = not self.black_turn

    def undo_move(self):
        if len(self.move_log) > 0:
            last_move = self.move_log.pop()
            self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
            self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
            self.white_turn = not self.white_turn
            self.black_turn = not self.black_turn

    #adds possible moves for the pawn at passed location to moves list
    def pawn_moves(self, r, c, moves):
        if self.board[r][c][0] == "w":
            if self.board[r-1][c] == "--":
                moves.append(move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c]:
                    moves.append(move((r, c), (r-2, c), self.board))
            #ensuring diagonal move is within space of board
            if (c + 1) < 8 and (c - 1) >= 0:
                #ensuring that there is a piece diagonal to capture and that it is a black piece
                if self.board[r-1][c+1][0] == "b":
                    moves.append(move((r, c), (r-1, c+1), self.board))
                if self.board[r-1][c-1][0] == "b":
                    moves.append(move((r, c), (r-1, c-1), self.board))
        elif self.board[r][c][0] == "b":
            if self.board[r+1][c] == "--":
                moves.append(move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c]:
                    moves.append(move((r, c), (r+2, c), self.board))
            #ensuring diagonal move is within space of board
            if (c + 1) < 8 and (c - 1) >= 0:
                #ensuring that there is a piece diagonal to capture and that it is a white piece
                if self.board[r+1][c+1][0] == "w":
                    moves.append(move((r, c), (r+1, c+1), self.board))
                if self.board[r+1][c-1][0] == "w":
                    moves.append(move((r, c), (r+1, c-1), self.board))      

    #adds possible moves for the rook at passed location to moves list
    #could definitely be made more efficient, same with bishop function (loop through an array of vectors?)
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

        '''
        #First attempt at rook logic, inefficient but works
        if r > 0:
            if self.board[r-i][c][0] == "b" and self.white_turn:
                moves.append(move((r, c), (r-i, c), self.board))
            elif self.board[r-i][c][0] =="w" and self.black_turn:
                moves.append(move((r, c), (r-i, c), self.board))           
            while self.board[r-i][c] == "--":
                moves.append(move((r, c), (r-i, c), self.board))
                i += 1
                if r - i == 0:
                    break
                elif self.board[r-i][c][0] == "b" and self.white_turn:
                    moves.append(move((r, c), (r-i, c), self.board))
                elif self.board[r-i][c][0] =="w" and self.black_turn:
                    moves.append(move((r, c), (r-i, c), self.board))
        '''

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
            

    #adds possible moves for the knight at passed location to moves list
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
            elif self.board[end_pos[0], end_pos[1]][0] == "b" and self.black_turn:
                continue
            else:
                moves.append(move((r, c), (end_pos[0], end_pos[1]), self.board))

    #adds possible moves for the bishop at passed location to moves list
    def bishop_moves(self, r, c, moves):
        #Up and to the right
        i = 1
        while i < 8:
            #checking for column and row viability
            if c + i > 7:
                break
            elif r - i < 0:
                break
            else:
                #Blank space
                if self.board[r-i][c+i] == "--":
                    moves.append(move((r, c), (r-i, c+i), self.board))
                #White caputre move
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
    
    #adds possible moves for the queen at passed location to moves list
    def queen_moves(self, r, c, moves):
        self.rook_moves(r, c, moves)
        self.bishop_moves(r, c, moves)

    #adds possible moves for the king at passed location to moves list
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
            elif self.board[end_pos[0], end_pos[1]][0] == "b" and self.black_turn:
                continue
            else:
                moves.append(move((r, c), (end_pos[0], end_pos[1]), self.board))

                
    #Takes all possible moves and then checks to ensure that any that result
    #in the player being in check are removed
    def valid_moves(self):
        return self.possible_moves()

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
        for val in moves:
            print("Piece: ", val.piece_moved)
            print("Start: ", val.start_row, val.start_col)
            print("End: ", val.end_row, val.end_col)
        return moves


   


class move():
    #adding dictionaries for ease of logging moves/positions in chess notation
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

    #converts the row and column pair to chess notation
    def convert_notation(self):
        return self.get_rankfile(self.start_row, self.start_col) + self.get_rankfile(self.end_row, self.end_col)

    #accesses the dictionary and returns the rank and file based on row and column values
    def get_rankfile(self, r, c):
        return self.cols_files[c] + self.rows_ranks[r]
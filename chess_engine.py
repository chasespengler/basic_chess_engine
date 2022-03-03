#Responsible for storing all info about current state of game and current valid moves and move log
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

        self.whiteTurn = True
        self.blackTurn = False
        self.whiteCastlability = True
        self.blackCastleability = False
        self.moveLog = np.array([])
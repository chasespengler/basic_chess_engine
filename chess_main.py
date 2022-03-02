#Responsible for user input and displaying current game board object
import pygame as p
import chess_engine

p.init()

WIDTH = HEIGHT = 512
dims = 8
SQ_size = HEIGHT // WIDTH
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
    gs = chess_engine.game_board()
    print(gs.board)

main()
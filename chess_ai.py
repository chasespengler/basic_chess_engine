import random

def random_move(valid_moves):
    if valid_moves:
        ind = random.randint(0, len(valid_moves) - 1)
        move = valid_moves[ind]
        return move
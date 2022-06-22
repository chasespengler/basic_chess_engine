'''
AI Module housing the various bots and their logic along with
scoring systems to keep track of intragame advantages
'''
import chess_engine
import random

#Dictionary of values assigned to each piece, checkmate value, and stalemate value
piece_vals = {"R": 5, "B": 3, "N": 3, "Q": 9, "P": 1, "K": 100}
CM = 1000
SM = 0

def random_move(gs, valid_moves):
    '''
    Random move generator for all possible moves
    Bot Level 1
    '''
    if valid_moves:
        ind = random.randint(0, len(valid_moves) - 1)
        move = valid_moves[ind]
        return move
    return None

def greedy_1(gs, valid_moves):
    '''
    Algorithm to decide a move based on immediate point advantage
    Bot Level 2
    '''
    turn = 1 if gs.white_turn else -1
    max_score = -CM
    best_moves = []
    for move in valid_moves:
        gs.make_move(move)
        if gs.white_checkmate or gs.black_checkmate:
            score = CM
        elif gs.stalemate:
            score = SM
        else:
            score = turn * material_score(gs.board)
        if score > max_score:
            best_moves = []
            max_score = score
            best_moves.append(move)
        elif score == max_score:
            best_moves.append(move)
        gs.undo_move()

    best_move = random_move(gs, best_moves)
    return best_move

def greedy_multi(gs, valid_moves):
    '''
    Algorithm to decide a move based on point advantage projected out several moves
    Bot Level 3
    '''
    turn = 1 if gs.white_turn else -1
    max_score = -CM
    best_moves = []
    for move in valid_moves:
        gs.make_move(move)
        if gs.white_checkmate or gs.black_checkmate:
            score = CM
        elif gs.stalemate:
            score = SM
        else:
            score = turn * material_score(gs.board)
        if score > max_score:
            best_moves = []
            max_score = score
            best_moves.append(move)
        elif score == max_score:
            best_moves.append(move)
        gs.undo_move()

    best_move = random_move(gs, best_moves)
    return best_move

def min_max_move(gs, valid_moves):
    '''
    Min max algorithm for bot play
    Bot Level 3
    '''
    if valid_moves:
        ind = random.randint(0, len(valid_moves) - 1)
        move = valid_moves[ind]
        return move
    return None

def material_score(board):
    '''
    Scores the board based on material on each side alone
    '''
    score = 0
    for row in board:
        for sq in row:
            if sq[0] == 'w':
                score += piece_vals[sq[1]]
            elif sq[0] == 'b':
                score -= piece_vals[sq[1]]

    return score

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
    return "No valid moves"

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
        #Bot move 1
        gs.make_move(move)
        #If move results in opponent checkmate then return move immediately
        if gs.white_checkmate or gs.black_checkmate:
            #Undo bot move 1
            gs.undo_move()
            return move
        elif gs.stalemate:
            score = SM
        else:
            opponent_moves = gs.valid_moves()
            best_opp = greedy_1(gs, opponent_moves)
            #Opponent move 1
            gs.make_move(best_opp)
            if gs.white_checkmate or gs.black_checkmate or gs.stalemate:
                #Undo opponent move
                gs.undo_move()
                #Undo bot move 1
                gs.undo_move()
                return greedy_1(gs, valid_moves)
            ahead_moves = gs.valid_moves()
            best_ahead_move = greedy_1(gs, ahead_moves)
            #Bot move 2
            gs.make_move(best_ahead_move)
            score = turn * material_score(gs.board)
            #Undo bot move 2
            gs.undo_move()
            #Undo opponent move
            gs.undo_move()
        #Determining the score logic
        if score > max_score:
            best_moves = []
            max_score = score
            best_moves.append(move)
        elif score == max_score:
            best_moves.append(move)
        #Undo bot move 1
        gs.undo_move()

    best_move = random_move(gs, best_moves)
    return best_move

def min_max_move(gs, valid_moves):
    '''
    Min max algorithm for bot play
    Bot Level 4
    '''
    turn = 1 if gs.white_turn else -1
    opp_min_max_score = CM
    best_moves = []
    opp_min_max_moves = []
    for move in valid_moves:
        gs.make_move(move)
        if gs.white_checkmate or gs.black_checkmate:
            return move
        elif gs.stalemate:
            #Make a stalemate move if alternative ends in checkmate? Maybe it doesn't need to be that smart
            st_move = move
            continue
        opp_moves = gs.valid_moves()
        opp_max_score = -CM
        for opp_move in opp_moves:
            gs.make_move(opp_move)
            if gs.white_checkmate or gs.black_checkmate:
                score = CM
            elif gs.stalemate:
                score = SM
            else:
                score = -turn * material_score(gs.board)
            if score > opp_max_score:
                opp_max_score = score
                opp_best_move = opp_move
                if opp_max_score < opp_min_max_score:
                    best_moves = []
                    opp_min_max_moves = []
                    opp_min_max_score = opp_max_score
                    opp_min_max_move = opp_best_move
                    best_moves.append(move)
                    opp_min_max_moves.append(opp_min_max_move)
                elif opp_max_score == opp_min_max_score:
                    best_moves.append(move)
                    opp_min_max_moves.append(opp_min_max_move)
            gs.undo_move()
        gs.undo_move()

    best_move = random_move(gs, best_moves)
    opp_best_move = random_move(gs, opp_min_max_moves)
    return best_move

def min_max_multi(gs, valid_moves):
    turn = 1 if gs.white_turn else -1
    opp_min_max_score = CM
    best_moves = []
    opp_min_max_moves = []
    for move in valid_moves:
        gs.make_move(move)
        #Need stalemate logic
        if gs.white_checkmate or gs.black_checkmate:
            return move
        elif gs.stalemate:
            pass
        opp_moves = gs.valid_moves()
        opp_max_score = -CM
        for opp_move in opp_moves:
            gs.make_move(opp_move)
            #Need to find a break logic here
            if gs.white_checkmate or gs.black_checkmate:
                pass
            elif gs.stalemate:
                pass
            my_moves = gs.valid_moves()
            for my_move in my_moves:
                gs.make_move(my_move)
                #Need stalemate logic
                if gs.white_checkmate or gs.black_checkmate:
                    return move
                elif gs.stalemate:
                    pass
                new_opp_moves = gs.valid_moves()
                for opp in new_opp_moves:
                    gs.make_move(opp)
                    if gs.white_checkmate or gs.black_checkmate:
                        score = CM
                    elif gs.stalemate:
                        score = SM
                    else:
                        score = -turn * material_score(gs.board)
                    if score > opp_max_score:
                        opp_max_score = score
                        opp_best_move = opp_move
                        if opp_max_score < opp_min_max_score:
                            best_moves = []
                            opp_min_max_moves = []
                            opp_min_max_score = opp_max_score
                            opp_min_max_move = opp_best_move
                            best_moves.append(move)
                            opp_min_max_moves.append(opp_min_max_move)
                        elif opp_max_score == opp_min_max_score:
                            best_moves.append(move)
                            opp_min_max_moves.append(opp_min_max_move)
                    gs.undo_move()
                gs.undo_move()
            gs.undo_move()
        gs.undo_move()

    best_move = random_move(gs, best_moves)
    opp_best_move = random_move(gs, opp_min_max_moves)
    return best_move
        

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

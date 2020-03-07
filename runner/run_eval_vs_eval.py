import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import copy

from core import board
from core import eval_func
from core.player import player

def _test_play(n_times):
    my_board = board.board()
    my_board.verbose = False
    fin_moves = []
    wins = {}
    wins[my_board.mark_player_1] = 0
    wins[my_board.mark_player_2] = 0

    last_finished_board = None

    for trial in range(n_times):
        my_board.reset()

        evaluators1 = [
            {'fn': eval_func.own_bingo,          'weight': 5.0},
            {'fn': eval_func.opp_bingo,          'weight': 5.0},
            {'fn': eval_func.own_almost_bingo,   'weight': 2.0},
            {'fn': eval_func.opp_almost_bingo,   'weight': 2.0},
            #{'fn': eval_func.freedom,            'weight': 1.0},
            {'fn': eval_func.center,             'weight': 1.0},
        ]
        p1 = player(my_board, my_board.player_1, my_board.mark_player_1, evaluators1)

        evaluators2 = [
            {'fn': eval_func.own_bingo,          'weight': 5.0},
            {'fn': eval_func.opp_bingo,          'weight': 5.0},
            {'fn': eval_func.own_almost_bingo,   'weight': 2.0},
            {'fn': eval_func.opp_almost_bingo,   'weight': 2.0},
            #{'fn': eval_func.freedom,            'weight': 1.0},
            {'fn': eval_func.center,             'weight': 1.0},
        ]

        p2 = player(my_board, my_board.player_2, my_board.mark_player_2, evaluators2)

        # interesting fact: this monte carlo shows first player have an edge
        players = [p1, p2]
        
        winner = " "
        num_moves = -1
        for i in range(my_board.board_size() ** 2):
            p = players[i % 2]
            p.move()
            if my_board.finished():
                #board.print_board()
                fin_moves.append(i)
                wins[p.mark()] += 1
                last_finished_board = copy.deepcopy(my_board)
                winner = p.mark()
                num_moves = i
                break
        print("{} === PLAYER {} WINS === # moves [{}]".format(trial, winner, num_moves))

    if last_finished_board is None:
        my_board.print_board()
    else:
        last_finished_board.print_board()

    avg_moves = 0
    if len(fin_moves) > 0:
        avg_moves = sum(fin_moves) / float(len(fin_moves))
    
    print("avg moves: {:.3f}, wins: {}".format(avg_moves, wins))


###################
## RUN
###################
_test_play(100)
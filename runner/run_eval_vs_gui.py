import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import copy

from core import board
from core import eval_func
from core.player import player

from gui.go_board import go_board

def _test_play():

    # as we use go_board, we need to use its size 19x19
    my_board = board.board(size=19)
    my_board.verbose = False
    fin_moves = []
    wins = {}
    wins[my_board.mark_player_1] = 0
    wins[my_board.mark_player_2] = 0

    last_finished_board = None

    n_times = 1
    for trial in range(n_times):
        my_board.reset()
        gui_board = go_board(None)

        # wire gui click to board
        #   player 1: auto_player, white
        #   player 2: gui, black

        evaluators1 = [
            {'fn': eval_func.own_bingo,          'weight': 5.0},
            {'fn': eval_func.opp_bingo,          'weight': 5.0},
            {'fn': eval_func.own_almost_bingo,   'weight': 2.0},
            {'fn': eval_func.opp_almost_bingo,   'weight': 2.0},
            #{'fn': eval_func.freedom,            'weight': 1.0},
            {'fn': eval_func.center,             'weight': 1.0},
        ]
        auto_player = player(my_board, my_board.player_1, my_board.mark_player_1, evaluators1)

        def on_gui_move(board, move, gui_board):
            # register gui move to board
            col, row = move
            board.player_2((row, col))

            if board.finished() is False:
                # let the other player move, and update GUI if move succeeds
                if auto_player.move():
                    player, (row, col) = board.get_last_move()
                    print(player, col, row)
                    gui_board.put_stone(row, col, "white")
                    board.print_board()
            
            # stop futher gui updates
            if board.finished() is True:
                gui_board.set_move_allowed(False)

        # on put stone, call my_board's player 2
        put_stone_fn = lambda event: gui_board.put_black_on_click(event,
            callback_fn=lambda col, row: on_gui_move(my_board, (col, row), gui_board))
        gui_board.set_on_click_callback(put_stone_fn)

        gui_board.pack()
        gui_board.mainloop()

###################
## RUN
###################
_test_play()
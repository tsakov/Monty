import pickle
from board import *


def save(file_name, board):
    with open('saved games/{0}.mps'.format(file_name), 'wb') as f:
        pickle.dump(board, f)


def load(file_name):
    try:
        with open('saved games/{0}.mps'.format(file_name), 'rb') as f:
            board = pickle.load(f)
    except Exception:
        return

    return board

import chess
import pygame

material_values = {
    'p': 1,
    'n': 3,
    'b': 3.25,
    'r': 5,
    'q': 9,
    'k': 0
}

def evaluate_material(board):
    total = 0
    for piece in board.piece_map().values():
        if piece.color == chess.WHITE:
            total += material_values[piece.symbol().lower()]
        else:
            total -= material_values[piece.symbol().lower()]
    return total

def maxmin(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_material(board)

    if maximizing_player:
        best_value = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            value = maxmin(board, depth - 1, alpha, beta, False)
            board.pop()
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value
    else:
        best_value = float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = maxmin(board, depth - 1, alpha, beta, True)
            board.pop()
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value

def make_worst_move(board):
    best_move = None
    best_value = float('inf')

    for move in board.legal_moves:
        board.push(move)
        value = maxmin(board, 3, float('-inf'), float('inf'), True)
        board.pop()

        if value < best_value:
            best_value = value
            best_move = move

    board.push(best_move)
    return best_move

def play_worst_move_chess():
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            move = input("Your move: ")
            board.push_san(move)
        else:
            worst_move = make_worst_move(board)
            print("Worst move:", board.san(worst_move))

        print("Current position:")
        print(board)
        print("---------------------")

    print("Game Over")
    print("Result:", board.result())

play_worst_move_chess()

import chess
import random

class Minimax:
    def __init__(self, board, aiColor):
        self.board = board
        self.legal_moves = []
        self.aiColor = aiColor

    def updateBoard(self, move):
        self.board.push_san(move)

    def aiMove(self):
        self.legal_moves.clear()

        for move in self.board.legal_moves:
            self.legal_moves.append(move)

        aiMove = chess.from_uci(random.choice(move))

        aiMoveSan = chess.san(aiMove)

        self.updateBoard(aiMoveSan)

        return aiMoveSan



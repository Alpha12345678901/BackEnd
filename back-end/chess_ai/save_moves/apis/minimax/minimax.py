import chess
import random

class Minimax:
    def __init__(self, aiColor):
        self.board = chess.Board()
        self.legal_moves = []
        self.aiColor = aiColor

    def updateBoard(self, move, notation='san'):
        if notation == 'uci':
            self.board.push(move)
        else:
            self.board.push_san(move)

    def aiMove(self):
        self.legal_moves.clear()

        for move in self.board.legal_moves:
            self.legal_moves.append(move)

        aiMoveUCI = random.choice(self.legal_moves)

        self.updateBoard(aiMoveUCI, 'uci')

        aiMoveUCI = chess.Move.uci(aiMoveUCI)

        return aiMoveUCI

    def displayBoard(self):
        print(self.board)


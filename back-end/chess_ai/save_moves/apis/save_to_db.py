import chess

from ..models import ChessGameLog
from .minimax.minimax import Minimax
from .reinforcement.reinforcement import Reinforcement

minimaxWhiteAI = Minimax('white')
minimaxBlackAI = Minimax('black')
reinforcementWhiteAI = Reinforcement('white')
reinforcementBlackAI = Reinforcement('black')

def insert_db(requestDict):
    chessGameCurrent = ChessGameLog.objects.filter(token=requestDict['token'])

    if not chessGameCurrent:

        print("trying to create a new game")

        minimaxWhiteAI.reset()
        minimaxBlackAI.reset()
        reinforcementWhiteAI.reset()
        reinforcementBlackAI.reset()

        if requestDict['whiteAgentName'] == 'minimax' and requestDict['turn'] == 'white':
            requestDict['whiteMoveLast'] = minimaxWhiteAI.aiMove()
        elif requestDict['blackAgentName'] == 'minimax' and requestDict['turn'] == 'black':
            minimaxBlackAI.updateBoard(requestDict['whiteMoveLast'])
            requestDict['blackMoveLast'] = minimaxBlackAI.aiMove()
        elif requestDict['whiteAgentName'] == 'reinforcement' and requestDict['turn'] == 'white':
            requestDict['whiteMoveLast'] = reinforcementWhiteAI.aiMove()
        elif requestDict['blackAgentName'] == 'reinforcement' and requestDict['turn'] == 'black':
            reinforcementBlackAI.updateBoard(requestDict['whiteMoveLast'])
            requestDict['blackMoveLast'] = reinforcementBlackAI.aiMove()

        new_user_input = ChessGameLog.objects.create(**requestDict)
        new_user_input.save()

        print("saved new chess game data to postgres database")

    else:

        print("trying to update a current game")

        if requestDict['whiteAgentName'] == 'minimax' and requestDict['turn'] == 'white':
            minimaxWhiteAI.updateBoard(requestDict['blackMoveLast'])
            requestDict['whiteMoveLast'] = minimaxWhiteAI.aiMove()
        elif requestDict['blackAgentName'] == 'minimax' and requestDict['turn'] == 'black':
            minimaxBlackAI.updateBoard(requestDict['whiteMoveLast'])
            requestDict['blackMoveLast'] = minimaxBlackAI.aiMove()
        elif requestDict['whiteAgentName'] == 'reinforcement' and requestDict['turn'] == 'white':
            reinforcementWhiteAI.updateBoard(requestDict['blackMoveLast'])
            requestDict['whiteMoveLast'] = reinforcementWhiteAI.aiMove()
        elif requestDict['blackAgentName'] == 'reinforcement' and requestDict['turn'] == 'black':
            reinforcementBlackAI.updateBoard(requestDict['whiteMoveLast'])
            requestDict['blackMoveLast'] = reinforcementBlackAI.aiMove()

        ChessGameLog.objects.update(**requestDict)

        print("updated existing chess game data in postgres database")
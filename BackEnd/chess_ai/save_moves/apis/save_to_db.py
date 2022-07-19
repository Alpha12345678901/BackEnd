import chess

from ..models import ChessGameLog
from .minimax.minimax import Minimax
from .reinforcement.reinforcement import Reinforcement


def insert_db(requestDict):
    id = requestDict['id']

    chessGameCurrent = ChessGameLog.objects.filter(id=id)

    board = chess.Board()

    minimaxWhiteAI = Minimax(board, 'white')
    minimaxBlackAI = Minimax(board, 'black')
    reinforcementWhiteAI = Reinforcement(board, 'white')
    reinforcementBlackAI = Reinforcement(board, 'black')

    if not chessGameCurrent:

        '''
        whiteAgentName = requestDict['whiteAgentName']
        blackAgentName = requestDict['blackAgentName']
        timeControl = requestDict['timeControl']
        moves = requestDict['moves']
        timeTracker = requestDict['timeTracker']
        result = requestDict['result']
        numberOfMoves = requestDict['numberOfMoves']
        whiteMaterialLeftCurrent = requestDict['whiteMaterialLeftCurrent']
        blackMaterialLeftCurrent = requestDict['blackMaterialLeftCurrent']
        whiteTimeLeftCurrent = requestDict['whiteTimeLeftCurrent']
        blackTimeLeftCurrent = requestDict['blackTimeLeftCurrent']
        whiteMoveLast = requestDict['whiteMoveLast']
        blackMoveLast = requestDict['blackMoveLast']
        '''
        board = chess.Board()

        if requestDict['whiteAgentName'] == 'minimax':
            requestDict['whiteMoveLast'] = minimaxWhiteAI.aiMove()
        elif requestDict['blackAgentName'] == 'minimax':
            minimaxBlackAI.updateBoard(requestDict['whiteMoveLast'])
            requestDict['blackMoveLast'] = minimaxBlackAI.aiMove()
        elif requestDict['whiteAgentName'] == 'reinforcement':
            requestDict['whiteMoveLast'] = reinforcementWhiteAI.aiMove()
        elif requestDict['blackAgentName'] == 'reinforcement':
            reinforcementBlackAI.updateBoard(requestDict['whiteMoveLast'])
            requestDict['blackMoveLast'] = reinforcementBlackAI.aiMove()

        new_user_input = ChessGameLog.objects.create(**requestDict)
        new_user_input.save()

        print("saved new chess game data to postgres database")

    else:

        if requestDict['whiteAgentName'] == 'minimax':
            minimaxWhiteAI.updateBoard(requestDict['blackMoveLast'])
            requestDict['whiteMoveLast'] = minimaxWhiteAI.aiMove()
        elif requestDict['blackAgentName'] == 'minimax':
            minimaxBlackAI.updateBoard(requestDict['whiteMoveLast'])
            requestDict['blackMoveLast'] = minimaxBlackAI.aiMove()
        elif requestDict['whiteAgentName'] == 'reinforcement':
            reinforcementWhiteAI.updateBoard(requestDict['blackMoveLast'])
            requestDict['whiteMoveLast'] = reinforcementWhiteAI.aiMove()
        elif requestDict['blackAgentName'] == 'reinforcement':
            reinforcementBlackAI.updateBoard(requestDict['whiteMoveLast'])
            requestDict['blackMoveLast'] = reinforcementBlackAI.aiMove()

        new_user_input = ChessGameLog.objects.update(**requestDict)
        new_user_input.save()

        print("updated existing chess game data in postgres database")
""" 
store data, determine valid move 
"""
import copy

class GameState():
    def __init__(self):
        # 8 * 8 board, each element of board has 2 char
        # "b" / "w": black/ white
        # "--": black space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.moveFunc = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                         'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.wKing = (7, 4)
        self.bKing = (0, 4)
        # checkMate: no valid moves & inCheck
        self.checkMate = False
        # staleMate: no valid Moves & not inCheck
        self.staleMate = False
        self.enpassantPossible = () 
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                    self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    '''
    move the step & update
    ''' 
    def makeMove(self, move):
        if self.board[move.startRow][move.startcol] != '--':
            self.board[move.startRow][move.startcol] = "--"
            self.board[move.endRow][move.endcol] = move.pieceMoved
            self.moveLog.append(move)               # log the move
            self.whiteToMove = not self.whiteToMove # switch player
            # update king location
            if (move.pieceMoved == "wK"):
                self.wKing = (move.endRow, move.endcol)
            elif (move.pieceMoved == "bK"):
                self.bKing = (move.endRow, move.endcol)

            # pawn promotionn
            if (move.isPawnPromotion):
                self.board[move.endRow][move.endcol] = move.pieceMoved[0] + 'Q'

            # pawn en passant
            if (move.isEnpassantMove):
                # capture pawn
                self.board[move.startRow][move.endcol] = "--"

            # update enPassantPossible, only on 2 square pawn advances
            if ((move.pieceMoved[1] == 'P') and (abs(move.startRow - move.endRow) == 2)):
                self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.endcol)
            else:
                self.enpassantPossible = ()

            # castle move
            if (move.isCastleMove):
                # king side castle move, moved 2 square, erase old rook
                if ((move.endcol - move.startcol) == 2):
                    # move rook to new square
                    self.board[move.endRow][move.endcol - 1] = self.board[move.endRow][move.endcol + 1]
                    self.board[move.endRow][move.endcol + 1] = "--"
                # queen side castle move
                else:
                    self.board[move.endRow][move.endcol + 1] = self.board[move.endRow][move.endcol - 2]
                    self.board[move.endRow][move.endcol - 2] = "--"

            # update castling Rights --> whenever king/rook moves
            self.updateCastleRights(move)
            self.castleRightLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                    self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))


    '''
    undo last move
    '''
    def undoMove(self):
        # moveLog not 0
        if (len(self.moveLog) != 0):
            move = self.moveLog.pop()
            self.board[move.startRow][move.startcol] = move.pieceMoved
            self.board[move.endRow][move.endcol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # switch player
            # update king location
            if (move.pieceMoved == "wK"):
                self.wKing = (move.startRow, move.startcol)
            elif (move.pieceMoved == "bK"):
                self.bKing = (move.startRow, move.startcol)

        # undo en passant move
        if (move.isEnpassantMove):
            self.board[move.endRow][move.endcol] = "--"
            self.board[move.startRow][move.endcol] = move.pieceCaptured
            self.enpassantPossible = (move.endRow, move.endcol)
        # undo 2 square pawn advance
        if ((move.pieceMoved[1] == 'P') and (abs(move.startRow - move.endRow) == 2)):
            self.enpassantPossible = ()

        # undo Castling Rights
        #self.castleRightLog.pop()
        #self.currentCastlingRight = self.castleRightLog[-1]
        self.castleRightLog.pop()
        castle_rights = copy.deepcopy(self.castleRightLog[-1])
        self.current_castling_rights = castle_rights

        # undo castle move
        if (move.isCastleMove):
            if((move.endcol - move.startcol) == 2):
                self.board[move.endRow][move.endcol + 1] = self.board[move.endRow][move.endcol - 1]
                self.board[move.endRow][move.endcol - 1] = "--"

            else:
                self.board[move.endRow][move.endcol - 2] = self.board[move.endRow][move.endcol + 1]
                self.board[move.endRow][move.endcol + 1] = "--"


    '''
    update castle Rights given the move
    '''
    def updateCastleRights(self, move):
        if (move.pieceMoved == "wK"):
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif (move.pieceMoved == "bK"):
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif (move.pieceMoved == "wR"):
            if (move.startRow == 7):
                if (move.startcol == 0):    # left
                    self.currentCastlingRight.wqs = False
                elif (move.startcol == 7):  # right
                    self.currentCastlingRight.wks = False

        elif (move.pieceMoved == "bR"):
            if (move.startRow == 0):
                if (move.startcol == 0):    # left
                    self.currentCastlingRight.bqs = False
                elif (move.startcol == 7):  # right
                    self.currentCastlingRight.bks = False

    '''
    All moves considering checks
        Remember to fix this!!!!!!!!!!!!!!!!!!!!
    '''
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRight = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)

        # other sol:
        # 1) check if any piece is in check
        # 2) see if piece are pined by other pieces (move then checkMate/staleMate)
        # 3) see if there are double check (two pieces that can check the king)

        #########################################
        #1) generate all possible moves
        moves = self.getAllPossibleMoves()
        if (self.whiteToMove):
            self.castleMove(self.wKing[0], self.wKing[1], moves)
        else:
            self.castleMove(self.bKing[0], self.bKing[1], moves)

        #2) for each move, make the move
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            #3) generate all oponent's moves
            #4) for each opponent's moves, check if they attack ur king

            # switch turn here, since make move switches turn: 
            #   want check bking --> makemove (check wking)
            self.whiteToMove = not self.whiteToMove
            #4) if oponents attacks king, remove that move
            if (self.inCheck()):
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
            
        # checkMate/ staleMate
        if (len(moves) == 0):
            if (self.inCheck()):
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False  

        if (self.whiteToMove):
            self.castleMove(self.wKing[0], self.wKing[1], moves)
        else:
            self.castleMove(self.bKing[0], self.bKing[1], moves)

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRight

        return moves

    '''
    Determine if the current player is in check
    '''
    def inCheck(self):
        if (self.whiteToMove):
            return self.squareUnderAttack(self.wKing[0], self.wKing[1])
        else:
            return self.squareUnderAttack(self.bKing[0], self.bKing[1])

    '''
    Determine if the enemy can attack the square (r, c)
    '''
    def squareUnderAttack(self, r, c):
        # switch to opponent's view
        self.whiteToMove = not self.whiteToMove
        opponMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in opponMoves:
            # square under attack
            if ((move.endRow == r) and (move.endcol == c)):
                return True
        
        return False

    '''
    All moves w/out considering checks
    '''
    def getAllPossibleMoves(self):
        move = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                # white turn & white turn to move     ||      black turn & black turn to move
                if ((turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove)):
                    piece = self.board[r][c][1]

                    # use dict to call appropriate chess function base on piece type
                    self.moveFunc[piece](r, c, move)

        return move
    
    '''
    get all the pawn move located at (r, c) and add these moves to the list
        are able to move up 1/2 squares; if upper left/right have opposite color, can be captured.
    '''
    def getPawnMoves(self, r, c, move):
        # white's turn
        if (self.whiteToMove):             
            if (((r - 1) >= 0) and (self.board[r - 1][c] == "--")):
                move.append(Move((r, c), (r - 1, c), self.board))
                if ((r == 6) and (self.board[r - 2][c] == "--")):
                    move.append(Move((r, c), (r - 2, c), self.board))

            if ((r - 1) >= 0):
                # if left is not Out of Boundary
                if (c - 1 >= 0):
                    # upper left be black chess --> save move
                    if (self.board[r - 1][c - 1][0] == 'b'):
                        move.append(Move((r, c), (r - 1, c - 1), self.board))
                    elif ((r - 1, c - 1) == self.enpassantPossible):
                        move.append(Move((r, c), (r - 1, c - 1), self.board, enpassantPossible=True))
                if (c + 1 <= 7):
                    if (self.board[r - 1][c + 1][0] == 'b'):
                        move.append(Move((r, c), (r - 1, c + 1), self.board))                
                    elif ((r - 1, c + 1) == self.enpassantPossible):
                        move.append(Move((r, c), (r - 1, c + 1), self.board, enpassantPossible=True))

        # black's turn
        else:
            if (((r + 1) <= 7) and (self.board[r + 1][c] == "--")):
                move.append(Move((r, c), (r + 1, c), self.board))
                if ((r == 1) and (self.board[r + 2][c] == "--")):
                    move.append(Move((r, c), (r + 2, c), self.board))

            if ((r + 1) <= 7):
                # if left is not Out of Boundary
                if (c - 1 >= 0):
                    # upper left be black chess --> save move
                    if (self.board[r + 1][c - 1][0] == 'w'):
                        move.append(Move((r, c), (r + 1, c - 1), self.board))
                    elif ((r + 1, c - 1) == self.enpassantPossible):
                        move.append(Move((r, c), (r + 1, c - 1), self.board, enpassantPossible=True))
                if (c + 1 <= 7):
                    if (self.board[r + 1][c + 1][0] == 'w'):
                        move.append(Move((r, c), (r + 1, c + 1), self.board))                
                    elif ((r + 1, c + 1) == self.enpassantPossible):
                        move.append(Move((r, c), (r + 1, c + 1), self.board, enpassantPossible=True))

    '''
    save move for rook & bishop & queen
    '''
    def saveMove(self, r, c, move, Direction):
        oppositeColor = 'b' if self.whiteToMove else 'w'
        sameColor = 'w' if self.whiteToMove else 'b'
        for d in Direction:
            for i in range(1, 8):
                new_r = r + (i * d[0])
                new_c = c + (i * d[1])
                if ((new_r <= 7) and (new_r >= 0) and (new_c <= 7) and (new_r >= 0)):
                    if (self.board[new_r][new_c][0] == sameColor):
                        break

                    elif (self.board[new_r][new_c][0] == oppositeColor):
                        move.append(Move((r, c), (new_r, new_c), self.board))
                        break

                    elif (self.board[new_r][new_c] == "--"):
                        move.append(Move((r, c), (new_r, new_c), self.board))        

    '''
    get all the rook move located at (r, c) and add these moves to the list
        can move "+" shape, cannot jump chess, can eat opposite chess in the direction.
    '''
    def getRookMoves(self, r, c, move):
        Direction = ((1, 0), (-1, 0), (0, 1), (0, -1))
        self.saveMove(r, c, move, Direction)

    '''
    get all the knight move located at (r, c) and add these moves to the list
    '''   
    def getKnightMoves(self, r, c, move):
        Direction = ((2, 1), (1, 2), (2, -1), (1, -2), (-2, 1), (-1, 2), (-2, -1), (-1, -2))
        oppositeColor = 'b' if self.whiteToMove else 'w'
        for d in Direction:
            new_r = r + d[0]
            new_c = c + d[1]
            if ((new_r <= 7) and (new_r >= 0) and (new_c <= 7) and (new_r >= 0)):
                if (self.board[new_r][new_c][0] == oppositeColor):
                    move.append(Move((r, c), (new_r, new_c), self.board))

                elif (self.board[new_r][new_c] == "--"):
                    move.append(Move((r, c), (new_r, new_c), self.board))     

    '''
    generate all valid castle moves for king at (r, c) & add to possible move list
    '''
    def castleMove(self, r, c, move):
        if (self.squareUnderAttack(r, c)):
            return

        if ((self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks)):
            self.getKingsideCastleMoves(r, c, move)  

        if ((self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs)):
            self.getQueensideCastleMoves(r, c, move)

    '''
    HELPER FUNCT: generate all valid castle moves for king's right side
    '''
    def getKingsideCastleMoves(self, r, c, move):
        if (self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--"):
            if ((not self.squareUnderAttack(r, c + 1)) and (not self.squareUnderAttack(r, c + 2))):
                move.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))
        
    '''
    HELPER FUNCT: generate all valid castle moves for king's left side
    '''
    def getQueensideCastleMoves(self, r, c, move):
        if (self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--"):
            # no squareUnderAttack(r, c - 3)  --> king is not going to pass there
            if ((not self.squareUnderAttack(r, c - 1)) and (not self.squareUnderAttack(r, c - 2))):
                move.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

    '''
    get all the bishop move located at (r, c) and add these moves to the list
    '''    
    def getBishopMoves(self, r, c, move):
        Direction = ((1, 1), (-1, -1), (1, -1), (-1, 1))
        self.saveMove(r, c, move, Direction)

    '''
    get all the queen move located at (r, c) and add these moves to the list
    '''
    def getQueenMoves(self, r, c, move):
        Direction = ((1, 1), (-1, -1), (1, -1), (-1, 1), (1, 0), (-1, 0), (0, 1), (0, -1))
        self.saveMove(r, c, move, Direction)

    '''
    get all the king move located at (r, c) and add these moves to the list
    ''' 
    def getKingMoves(self, r, c, move):
        Direction = ((1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1))
        oppositeColor = 'b' if self.whiteToMove else 'w'
        for d in Direction:
            new_r = r + d[0]
            new_c = c + d[1]
            if ((new_r <= 7) and (new_r >= 0) and (new_c <= 7) and (new_r >= 0)):
                if (self.board[new_r][new_c][0] == oppositeColor):
                    move.append(Move((r, c), (new_r, new_c), self.board))

                elif (self.board[new_r][new_c] == "--"):
                    move.append(Move((r, c), (new_r, new_c), self.board))  


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs

    


class Move():
    ranksToRows = {"1":7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    fileToCol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colToFile = {v: k for k, v in fileToCol.items()}

    def __init__(self, startSQ, endSQ, board, enpassantPossible=False, isCastleMove=False):
                                                # ^^ possible param (default value: empty)
        self.startRow = startSQ[0]
        self.startcol = startSQ[1]
        self.endRow = endSQ[0]
        self.endcol = endSQ[1]
        self.pieceMoved = board[self.startRow][self.startcol]
        self.pieceCaptured = board[self.endRow][self.endcol]
        self.moveID = self.startRow * 1000 + self.startcol * 100 + self.endRow * 10 + self.endcol

        # pawn promotion
        self.isPawnPromotion =  (((self.pieceMoved == "wP") and (self.endRow) == 0) or ((self.pieceMoved == "bP") and (self.endRow == 7)))

        # en passant
        self.isEnpassantMove = enpassantPossible
        if (self.isEnpassantMove):
            self.pieceCaptured = "wP" if self.pieceMoved == "bP" else "bP"

        # castle move
        self.isCastleMove = isCastleMove

    '''
    overwrite = method
    '''
    def __eq__(self, other):
        if (isinstance(other, Move)):
            return self.moveID == other.moveID

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startcol) + self.getRankFile(self.endRow, self.endcol)

    def getRankFile(self, r, c):
        return self.colToFile[c] + self.rowsToRanks[r]



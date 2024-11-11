"""
Name: python-chess-coverage

Abstract: Expose the potential energy of chess ply.

Description: This library constructs a dictionary of chess piece threat
and protection statuses, keyed by "rank and file" board positions.

Example fragment:

  "e4": {
    "color": true,
    "index": 28,
    "is_protected_by": [],
    "is_threatened_by": ["d5"],
    "moves": ["d5", "e5"],
    "occupant": "white pawn",
    "position": "e4",
    "protects": [],
    "symbol": "P",
    "threatens": ["d5"],
    "black_can_move_here": [],
    "white_can_move_here": []
  }
"""

import chess

class Coverage:
    def __init__(self, board):
        self.board = board

    def get_piece(self, board, string):
        square = chess.parse_square(string)
        piece = board.piece_at(square)
        return piece

    def fetch_moves(self, board, posn):
        moves = []
        for m in board.pseudo_legal_moves:
            string = str(m)
            # print(string)
            from_sq = string[0:2]
            to_sq = string[2:4]
            # print(f"F: {from_sq}, T: {to_sq}")
            if from_sq == posn:
                moves.append(to_sq)
        return moves

    def fetch_threatens(self, board, moves):
        threatens = []
        for m in moves:
            string = str(m)
            piece = self.get_piece(board, string)
            if piece:
                threatens.append(string)
        return threatens

    def is_king(self, posn):
        piece = self.get_piece(self.board, posn)
        if piece.symbol().lower() == 'k':
            return True
        return False

    def fetch_protects(self, posn, square):
        protects = []
        fen = self.board.fen()
        parts = fen.split(" ")
        flipped_fen = parts[0].swapcase()
        flipped_board = chess.Board(fen=flipped_fen)
        piece = flipped_board.piece_at(square)
        color = piece.color
        piece.color = not color
        flipped_board.set_piece_at(square, piece)
        flipped_board.turn = not color
        moves = self.fetch_moves(flipped_board, posn)
        protects = self.fetch_threatens(flipped_board, moves)
        for i in protects.copy():
            if self.is_king(i):
                protects.remove(i)
                break
        return protects

    def can_move_here(self, coverage, posn, color_name, moves):
        for m in moves:
            string = str(m)
            piece = self.get_piece(self.board, string)
            if not piece:
                key = color_name + "_can_move_here"
                if not key in coverage[string]:
                    coverage[string][key] = []
                coverage[string][key].append(posn)

    def cover(self):
        coverage = {}
        for square in chess.SQUARES:
            posn = chess.square_name(square)
            coverage[posn] = {}
        for square in chess.SQUARES:
            posn = chess.square_name(square)
            color = self.board.color_at(square)
            piece = self.board.piece_at(square)
            pieces = {
                "p": 1,
                "n": 2,
                "b": 3,
                "r": 4,
                "q": 5,
                "k": 6,
            }
            name = '-'
            if piece:
                lower = str(piece).lower()
                index = pieces[lower]
                name = chess.piece_name(index)
                self.board.turn = color
                if color:
                    color_name = 'white'
                else:
                    color_name = 'black'
                moves = self.fetch_moves(self.board, posn)
                threatens = self.fetch_threatens(self.board, moves)
                protects = self.fetch_protects(posn, square)
                coverage[posn]["index"] = square
                coverage[posn]["position"] = posn
                coverage[posn]["color"] = color
                coverage[posn]["occupant"] = f"{color_name} {name}"
                coverage[posn]["symbol"] = str(piece)
                coverage[posn]["moves"] = moves
                coverage[posn]["threatens"] = threatens
                coverage[posn]["protects"] = protects
                self.can_move_here(coverage, posn, color_name, moves)
        for posn in coverage:
            pc = coverage[posn]
            piece = self.get_piece(self.board, posn)
            if piece:
                if not "is_threatened_by" in pc:
                    pc["is_threatened_by"] = []
                if not "is_protected_by" in pc:
                    pc["is_protected_by"] = []
                for i in coverage:
                    ic = coverage[i]
                    if i == posn:
                        continue
                    if ('threatens' in ic) and (posn in ic['threatens']):
                        pc["is_threatened_by"].append(i)
                    if ('protects' in ic) and (posn in ic['protects']):
                        pc["is_protected_by"].append(i)
        return coverage

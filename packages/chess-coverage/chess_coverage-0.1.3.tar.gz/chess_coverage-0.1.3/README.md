# python-chess-coverage
Expose the potential energy of chess ply

This library constructs a dictionary of chess piece threat and protection statuses, keyed by "rank and file" board positions.

Usage:

```python
import chess
import json

from chess_coverage import Coverage

board = chess.Board()
board.push_san("e4")
board.push_san("d5")

c = Coverage(board)
cover = c.cover()

print(json.dumps(cover, indent=2, sort_keys=True))
```

Example result fragment:

```json
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
```


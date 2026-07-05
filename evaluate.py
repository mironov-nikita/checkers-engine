def evaluate_position(wp, bp, wk, bk):
    def calculate_score(pawns, kings, mirror=True) -> int: # mirror=True for white
        result = 0
        for idx in get_idx(pawns):
            pos = (31 - idx) if mirror else idx
            result += 100
            result += POSITION_BONUS[pos]
            if pos in CENTER_BONUS:
                result += 10
            if pos in (0, 1, 2, 3):
                result += BACKRANK_BONUS

        for pos in get_idx(kings):
            result += 300
            if pos in CENTER_BONUS:
                result += 15  
    
        return result
    
    if not (bp | bk): 
        return 100000000
    if not (wp | wk):
        return -100000000
    white_score = calculate_score(wp, wk, mirror=True) 
    black_score = calculate_score(bp, bk, mirror=False)
    return white_score - black_score

def get_idx(pieces):
    while pieces:
        idx = (pieces & -pieces)
        yield idx.bit_length() - 1
        pieces ^= idx

BACKRANK_BONUS = 20
CENTER_BONUS = {13, 14, 17, 18}  
POSITION_BONUS = [
    0, 0, 0, 0,
    5, 5, 5, 5,
    10,10,10,10,
    15,15,15,15,
    25,25,25,25,
    35,35,35,35,
    50,50,50,50,
    0,0,0,0
]

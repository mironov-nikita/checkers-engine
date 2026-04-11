import random

def get_rand_hash(seed=None):
    if seed:
        random.seed(seed)
    table = {
        'wp': {},
        'bp': {},
        'wk': {},
        'bk': {},
        'white_to_move': random.getrandbits(64)  
    }

    for i in range(32):
        table['wp'][i] = random.getrandbits(64)
        table['bp'][i] = random.getrandbits(64)
        table['wk'][i] = random.getrandbits(64)
        table['bk'][i] = random.getrandbits(64)
    return table 
        
def update_hash(move, wp, bp, is_white_turn, pieces_hash, pos_hash):
    if len(move) == 4:
        fr, to, captures, promoted = move 
    elif len(move) == 3:
        fr, to, captures = move 
        promoted = False
    else:
        fr, to = move 
        captures = []
        promoted = False 
        
    if is_white_turn:
        if wp >> fr & 1:
            pos_hash ^= pieces_hash["wp"][fr]
            if promoted or to in (0, 1, 2, 3):
                pos_hash ^= pieces_hash["wk"][to]
            else:
                pos_hash ^= pieces_hash["wp"][to] 
        else:
            pos_hash ^= pieces_hash["wk"][fr]
            pos_hash ^= pieces_hash["wk"][to]
        for capture in captures:
            if bp >> capture & 1:
                pos_hash ^= pieces_hash["bp"][capture]
            else:
                pos_hash ^= pieces_hash["bk"][capture]

    else:
        if bp >> fr & 1:
            pos_hash ^= pieces_hash["bp"][fr]
            if promoted or to in (28, 29, 30, 31):
                pos_hash ^= pieces_hash["bk"][to]
            else:
                pos_hash ^= pieces_hash["bp"][to] 
        else:
            pos_hash ^= pieces_hash["bk"][to]
            pos_hash ^= pieces_hash["bk"][fr]

        for capture in captures:
            if wp >> capture & 1:
                pos_hash ^= pieces_hash["wp"][capture]
            else:
                pos_hash ^= pieces_hash["wk"][capture]
    
    return pos_hash



def hash_position(wp, bp, wk, bk, pieces_hash, is_white_turn):
    result_hash = 0
    
    for i in range(32):
        if 1 & (wp>>i):
            result_hash ^= pieces_hash['wp'][i]
        elif 1 & (bp>>i):
            result_hash ^= pieces_hash['bp'][i]
        elif 1 & (wk>>i):
            result_hash ^= pieces_hash['wk'][i]
        elif 1 & (bk>>i):
            result_hash ^= pieces_hash['bk'][i]
    return result_hash 

def get_from_table(TABLE, position):
    return TABLE[position]

def update_table(TABLE, position, depth, value):
    if position in TABLE:
        old_depth, old_value = TABLE[position]
        if depth > old_depth:
            TABLE[position] = [depth, value]
    else:
        TABLE[position] = [depth, value]

def in_table(TABLE, position):
    return True if position in TABLE else False


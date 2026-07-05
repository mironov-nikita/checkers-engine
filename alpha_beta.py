from move_generation import generate_moves, get_squares
from evaluate import evaluate_position, POSITION_BONUS, CENTER_BONUS
from zobrist_hash import *

def new_state(fr, to, is_white_turn, wp, bp, wk, bk, promoted=False, captures=[]):

    def mirror_new_state(pawns, kings, opponent_pawns, opponent_kings, BACKRANK): 
        if (pawns >> fr & 1):
            pawns ^= (1<<fr)
            if to in BACKRANK or promoted:
                kings ^= (1<<to)
            else:
                pawns ^= (1<<to)
        else:
            kings ^= (1<<fr)
            kings ^= (1<<to)

        for idx in captures:
            if (opponent_pawns >> idx & 1):
                opponent_pawns ^= (1<<idx)
            else:
                opponent_kings ^= (1<<idx)
            
        return (pawns, kings, opponent_pawns, opponent_kings)
    
    if is_white_turn:
        new_wp, new_wk, new_bp, new_bk = mirror_new_state(wp, wk, bp, bk, BACKRANK=(0, 1, 2, 3))
    else:
        new_bp, new_bk, new_wp, new_wk = mirror_new_state(bp, bk, wp, wk, BACKRANK=(28, 29, 30, 31))
    return (new_wp, new_bp, new_wk, new_bk)


def move_priority(move, wk, bk, is_white_turn):
    prioriy = 0
    if len(move) == 4:
        fr, to, captures, promoted = move 
    elif len(move) == 3:
        fr, to, captures = move 
    else:
        fr, to = move 
        captures = []

    if captures:
        prioriy += 10*len(captures)
        if is_white_turn:
            for capture in captures:
                if 1<<capture & bk:
                    prioriy += 10
        else:
            for capture in captures:
                if 1<<capture & wk:
                    prioriy += 10
    
    if is_white_turn and (to in (0, 1, 2, 3)): prioriy += 15
    elif (not is_white_turn) and (to in (31, 30, 29, 28)): prioriy += 15 
    if to in CENTER_BONUS:
        prioriy += 5
    
    return prioriy

PIECES_HASH = get_rand_hash(42)
HASH_TABLE = {}
nodes_visited = 0 

def minimax_alphabeta(wp, bp, wk, bk, is_white_turn, pos_hash, depth=0, max_depth=6, alpha=-float('inf'), beta=float('inf')):
    global nodes_visited
    nodes_visited += 1
    global HASH_TABLE
    if in_table(HASH_TABLE, pos_hash):
        old_depth, old_value = get_from_table(HASH_TABLE, pos_hash)
        if old_depth >= depth:
            return old_value
        
    
    if (bp | bk) == 0: return 100000000 - depth
    if (wp | wk) == 0: return -100000000 + depth
    if depth >= max_depth:
        return evaluate_position(wp, bp, wk, bk)

    moves_list = list(generate_moves(wp, bp, wk, bk, is_white_turn))
    if not moves_list:
        return -100000000 + depth if is_white_turn else 100000000 - depth
    moves_list.sort(key=lambda move: move_priority(move, wk, bk, is_white_turn), reverse=True)

    if is_white_turn:
        max_score = -float('inf')
        for move in moves_list:
            if len(move) == 4:
                fr, to, captures, promoted = move 
            elif len(move) == 3:
                fr, to, captures = move 
                promoted = False
            else:
                fr, to = move 
                captures = []
                promoted = False 
        
            new_wp, new_bp, new_wk, new_bk = new_state(fr, to, is_white_turn, wp, bp, wk, bk, promoted, captures)
            new_pos_hash = update_hash(move, new_wp, new_bp, False, PIECES_HASH, pos_hash)
            score = minimax_alphabeta(new_wp, new_bp, new_wk, new_bk, False, new_pos_hash, depth+1, max_depth, alpha, beta)
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            
            if beta <= alpha:
                break
        update_table(HASH_TABLE, new_pos_hash, depth, score)
        return max_score
    else:
        min_score = float('inf')
        for move in moves_list:
            if len(move) == 4:
                fr, to, captures, promoted = move 
            elif len(move) == 3:
                fr, to, captures = move 
                promoted = False
            else:
                fr, to = move 
                captures = []
                promoted = False 
        
            new_wp, new_bp, new_wk, new_bk = new_state(fr, to, is_white_turn, wp, bp, wk, bk, promoted, captures)
            new_pos_hash = update_hash(move, new_wp, new_bp, True, PIECES_HASH, pos_hash)
            score = minimax_alphabeta(new_wp, new_bp, new_wk, new_bk, True, new_pos_hash, depth+1, max_depth, alpha, beta)
            min_score = min(min_score, score)
            beta = min(beta, score)
            
            if beta <= alpha:
                break
        update_table(HASH_TABLE, new_pos_hash, depth, score)
        return min_score


def get_best_move(wp, bp, wk, bk, is_white_turn, chosen_depth=6):
    global nodes_visited
    nodes_visited = 0
    import time
    start = time.time()
    
    best_move = None
    best_score = -float('inf') if is_white_turn else float('inf')
    alpha = -float('inf')
    beta = float('inf')
    global PIECES_HASH
    pos_hash = hash_position(wp, bp, wk, bk, PIECES_HASH, is_white_turn)


    moves_list = generate_moves(wp, bp, wk, bk, is_white_turn)
    if not moves_list:
        return 
    for move in generate_moves(wp, bp, wk, bk, is_white_turn):
        if len(move) == 4:
            fr, to, captures, promoted = move 
        elif len(move) == 3:
            fr, to, captures = move 
            promoted = False
        else:
            fr, to = move 
            captures = []
            promoted = False 
        
        new_wp, new_bp, new_wk, new_bk = new_state(fr, to, is_white_turn, wp, bp, wk, bk, promoted, captures)
        score = minimax_alphabeta(new_wp, new_bp, new_wk, new_bk, not is_white_turn, pos_hash, depth=1, max_depth=chosen_depth, alpha=alpha, beta=beta)
        
        if is_white_turn:
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
        else:
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)
    
    time_for_move = time.time() - start
    if time_for_move  < 0.01:
        print(f"Time: {time_for_move:.2f}s, Nodes: {nodes_visited:,}, NPS: {int(nodes_visited*100):,}")
    else:
        print(f"Time: {time_for_move:.2f}s, Nodes: {nodes_visited:,}, NPS: {int(nodes_visited/time_for_move):,}")
    
    return best_move

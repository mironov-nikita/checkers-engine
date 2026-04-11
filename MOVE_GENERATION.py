from BOARD import PAWNS_CAPTURES, BLACK_PAWNS_MOVES, WHITE_PAWNS_MOVES, DIAGONALS


def generate_moves(wp, bp, wk, bk, is_white_turn): 

    def generate_quiet_moves(wp, bp, wk, bk, is_white_turn):
        moves_table = WHITE_PAWNS_MOVES if is_white_turn else BLACK_PAWNS_MOVES
        pawns = wp if is_white_turn else bp 
        kings = wk if is_white_turn else bk 
        all_pieces = wp | bp | wk | bk 

        def quiet_pawn_moves(pawns, all_pieces, moves_table):
            moves = []
            for i in get_squares(pawns):
                for posible_move in moves_table[i]:
                    if not (all_pieces >> posible_move & 1):
                        moves.append((i, posible_move))
            return moves
        
        def quiet_king_moves(kings, all_pieces):
            moves = []
            for i in get_squares(kings):
                for diagonal in DIAGONALS[i]:
                    for posible_move in diagonal:
                        if (all_pieces >> posible_move & 1):
                            break 
                        moves.append((i, posible_move))
            return moves
        
        all_quite_moves = []
        all_quite_moves.extend(quiet_pawn_moves(pawns, all_pieces, moves_table))
        all_quite_moves.extend(quiet_king_moves(kings, all_pieces))
        return all_quite_moves
    
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
    def generate_captures(wp, bp, wk, bk, is_white_turn):
        opponent_pieces = (bp | bk) if is_white_turn else (wp | wk) 
        all_pieces = wp | bp | wk | bk 
        our_pieces = (wp | wk) if is_white_turn else (bp | bk) 
        
        def capture_pawn_dfs(start, current, captured, is_white_turn):
            results = []
            
            for posible_capture in PAWNS_CAPTURES[current]:
                taken_piece, landing_spot = posible_capture
                if taken_piece in captured:
                    continue

                if (opponent_pieces >> taken_piece & 1) and (not all_pieces >> landing_spot & 1):
                    new_captured = captured + [taken_piece]
                    
                    UPRANK = (0, 1, 2, 3) if is_white_turn else (28, 29, 30, 31)
                    if landing_spot in UPRANK:
                        local_result = capture_king_dfs(start, landing_spot, new_captured)
                        promoted = True
                    else:
                        local_result = capture_pawn_dfs(start, landing_spot, new_captured, is_white_turn)
                        promoted = False
                    if local_result:
                        results.extend(local_result)
    
                    else:
                        results.append((start, landing_spot, new_captured, promoted))
            return results

        
        def capture_king_dfs(start, current, captured):
            results = []

            for diag in DIAGONALS[current]:
                for i, move in enumerate(diag):
                    if (our_pieces >> move & 1):
                        break
            
                    if (opponent_pieces >> move & 1) and move not in captured:
                        new_captured = captured + [move]
                        landings_with_continuation = []
                        landings_without_continuation = []
                
                        for j in range(i + 1, len(diag)):
                            if (all_pieces >> diag[j] & 1):
                                break
                    
                            local_result = capture_king_dfs(start, diag[j], new_captured)
                            if local_result:
                                landings_with_continuation.extend(local_result)
                            else:
                                landings_without_continuation.append((start, diag[j], new_captured, True))
                
                        if landings_with_continuation:
                            results.extend(landings_with_continuation)
                        else:
                            results.extend(landings_without_continuation)
                
                        break
    
            return results
# -------------------------------------------------------------------------------------------------------------------------------------------------
        all_captures = []
        
        kings = wk if is_white_turn else bk
        for i in get_squares(kings):
            all_captures.extend(capture_king_dfs(i, i, []))

        pawns = wp if is_white_turn else bp 
        for i in get_squares(pawns):
            all_captures.extend(capture_pawn_dfs(i, i, [], is_white_turn))

        return all_captures
    
    forced_moves = generate_captures(wp, bp, wk, bk, is_white_turn)
    if forced_moves:
        return forced_moves

    common_moves = generate_quiet_moves(wp, bp, wk, bk, is_white_turn)
    return common_moves 

def get_squares(pieces):
    while pieces:
        idx = (pieces & -pieces)
        yield idx.bit_length() - 1
        pieces ^= idx

from ALPHA_BETA import get_best_move, new_state, generate_moves
import time

def translate(board):
    wp = 0b00000000000000000000000000000000
    bp = 0b00000000000000000000000000000000
    wk = 0b00000000000000000000000000000000
    bk = 0b00000000000000000000000000000000

    for i in range(8):
        for j in range(4):
            if board[i][j] == 'wk':
                wk ^= 1<<((8-i-1) * 4 + j)
            elif board[i][j] == 'wp':
                wp ^= 1<<((8-i-1) * 4 + j)
            elif board[i][j] == 'bp':
                bp ^= 1<<((8-i-1) * 4 + j)
            elif board[i][j] == 'bk':
                bk ^= 1<<((8-i-1) * 4 + j)
    return (wp, bp, wk, bk)

def fill_the_board():
    
    board = [
        ['_', '_', '_', '_'],
        ['_', '_', '_', '_'],
        ['_', '_', '_', '_'],
        ['_', '_', '_', '_'],
        ['_', '_', '_', '_'],
        ['_', '_', '_', '_'],
        ['_', '_', '_', '_'],
        ['_', '_', '_', '_'],
    ]
    while True:
        for i in range(8):
            for j in range(4):
                if not (i & 1):
                    print(" ", board[i][j], end='')
                else:
                    print(board[i][j], ' ', end='')
            print('\n')
        new_piece = input("Input piece's type (wp, wk, bp, bk) or EXIT to stop: ").strip()
        if new_piece == 'EXIT':
            break 
        position = input("Input position. example: 7 4 (its means 7th row and 4th col): ").strip()
        row = 8 - int(position[0])
        col = int(position[2]) - 1
        

        if new_piece == 'wk':
            board[row][col] = 'wk'
        elif new_piece == 'bk':
            board[row][col] = 'bk'
        elif new_piece == 'bp':
            board[row][col] = 'bp'
        elif new_piece == 'wp':
            board[row][col] = 'wp'
        else:
            print("Incorrect input")
            continue            
        
    return board 
def input_my_board():
    board = fill_the_board()
    wp, bp, wk, bk = translate(board=board)
    print("white pawns: ", '0b' + bin(wp)[2:].zfill(32))
    print("black pawns: ", '0b' + bin(bp)[2:].zfill(32))
    print("white kings: ", '0b' + bin(wk)[2:].zfill(32))
    print("black kings: ", '0b' + bin(bk)[2:].zfill(32))
    return (wp, bp, wk, bk)



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def game(level=6):
    x = input("Play from chosen position? Y/n: ").strip()
    if x == 'Y':
        wp, bp, wk, bk = input_my_board()
    else:
        wp = 0b11111111111100000000000000000000
        bp = 0b00000000000000000000111111111111 
        wk = 0b00000000000000000000000000000000
        bk = 0b00000000000000000000000000000000
    for _ in range(100):
        if _ % 2 == 1:
            is_white_turn = True
            moves = generate_moves(wp, bp, wk, bk, True)
            if not moves:
                print("BLACK WON!!!!" if not is_white_turn else "WHITE WON!!!!")
                exit()

            for i, posible_move in enumerate(moves):
                print(f'{i+1}:  {posible_move}')
            try:
                choice = int(input("Input idx of move: "))
                if choice > len(moves) or choice <= 0:
                    print("ERROR: incorrect input.")
                    raise ValueError
            except ValueError:
                print(f"ERROR: VALUE ERROR.")
                return
            player_move = moves[choice-1]
            if len(player_move) == 4:
                fr, to, captures, promoted = player_move
            elif len(player_move) == 3:
                fr, to, captures = player_move
                promoted = False
            else:
                fr, to = player_move 
                captures = []
                promoted = False
            wp, bp, wk, bk = new_state(fr, to, is_white_turn, wp, bp, wk, bk, promoted, captures)

        else:
            is_white_turn = False
            move = get_best_move(wp, bp, wk, bk, is_white_turn, chosen_depth=level)
            if not move:
                print("WHITE WON!!!!" if not is_white_turn else "BLACK WON!!!!")
                exit()
            if len(move) == 4:
                fr, to, captures, promoted = move
            elif len(move) == 3:
                fr, to, captures = move
                promoted = False
            else:
                fr, to = move 
                captures = []
                promoted = False
            wp, bp, wk, bk = new_state(fr, to, is_white_turn, wp, bp, wk, bk, promoted, captures)
            print(move)

if __name__ == '__main__':  
    levels = {
        1: 4,
        2: 8,
        3: 10,
        4: 12,
    }
    print("Hi, input 1/2/3/4")
    print("1: EASY\n2: NORMAL\n3: HARD\n4: IMPOSSIBLE\n5: CUSTOM")
    try:
        player_choice = int(input(""))
        if player_choice == 5:
            custom_depth = int(input("Input depth: "))
            if custom_depth > 20:
                print("Sorry, depth too deep.")
                exit()
            elif custom_depth > 12:
                ans = input("Searching too deeply can put a heavy computation load on the computer. Are you sure Y/n:\n")
                if ans == "Y":
                    game(custom_depth)
                exit()
        elif not (player_choice in (1, 2, 3, 4)):
            raise ValueError
    except ValueError as e:
        print(f"ERROR: {e}")
        exit()

    game(levels[player_choice])

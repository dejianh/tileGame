import columns_game

def run()->None:
    try:
        board_row,board_col = ask_user_for_board_size()

        game_state = columns_game.GameState()

        game_state.initiate_game_board_to_empty(board_row,board_col)

        game_faller = None
        
        third_line = input()
        
        if third_line == 'EMPTY':
            display_board(game_state)
            pass

        elif third_line == 'CONTENTS':
            set_up_board(game_state)

            game_state.check_match_and_change_status()

            display_board(game_state)

        while True:
            user_input = input()

            if user_input == '':
                game_state.time_tick(game_faller,game_state)

                display_board(game_state)

            if user_input == 'R':
                game_faller.rotate(game_state)

                display_board(game_state)
                
            if user_input == 'Q': 
                return None

            if user_input.startswith('F'):
                command_list = user_input.split()

                check_row = len(game_state.get_board()[0])-1
                
                col = int(command_list[1])-1
                color1 = command_list[2]
                color2 = command_list[3]
                color3 = command_list[4]
                    
                game_state.check_game_over_when_set_up_faller(check_row,col)

                game_faller = columns_game.set_up_faller(game_state,col,
                                                         color1,color2,color3)
                display_board(game_state)           


            if user_input == '<':
                game_faller.check_if_faller_could_move_left_and_move_left(game_state)
                
                display_board(game_state)

            if user_input == '>':
                game_faller.check_if_faller_could_move_right_and_move_right(game_state)

                display_board(game_state)

                
    except columns_game.InvalidSizeError:
        print('The size is invalid')

    except columns_game.InvalidPositionError:
        print('The column of the faller is invalid')

    except columns_game.GameOverError :
        display_board(game_state)
        print('GAME OVER')
    

        

def ask_user_for_board_size()->tuple:
    user_input_row = int(input())
    user_input_col = int(input())

    row_number = user_input_row
    col_number = user_input_col

    return row_number,col_number



def display_board(game_state:'GameState')->None:
        board = game_state.get_board()
        for row_number in reversed(range(0,len(board[0]))):
            if row_number != len(board[0])-1:
                print()
            print('|',end = '')
            for col_number in range(0,len(board)):
                if board[col_number][row_number] == None:
                    print('   ',end = '')
                if board[col_number][row_number] != None:
                    if board[col_number][row_number].get_status() == 'freeze':
                        print(' ' +board[col_number][row_number].get_color()+ ' ',end = '')
                    if board[col_number][row_number].get_status() == 'faller':
                        print('[' +board[col_number][row_number].get_color()+ ']',end = '')
                    if board[col_number][row_number].get_status() == 'faller_land':
                        print('|' +board[col_number][row_number].get_color()+ '|',end = '')
                    if board[col_number][row_number].get_status() == 'matched':
                        print('*' +board[col_number][row_number].get_color()+ '*',end = '')
            print('|',end = '')
        print()
        print(' '+ '---'* len(board)+' ')


def set_up_board(game_state:columns_game.GameState)->None:
    for row_number in reversed(range(0,len(game_state.get_board()[0]))):
            user_input = input()
            for col_number in range(0,len(game_state.get_board())):
                if user_input[col_number] != ' ':
                    jewel = columns_game.Jewel(row_number,col_number,
                                               user_input[col_number],'freeze')
                    
                    game_state.add_jewel(jewel,row_number,col_number)
    
if __name__ == '__main__':
    run()
    

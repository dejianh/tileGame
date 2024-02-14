import random

class InvalidSizeError(Exception):
    pass
class InvalidPositionError(Exception):
    pass
class GameOverError(Exception):
    pass

def check_if_add_random_faller(game_state:'GameState')->bool:
    board = game_state.get_board()

    for jewel_list in board:
        for jewel in jewel_list:
            if jewel != None:
                if jewel.get_status() != 'freeze':
                    return False

    return True



def check_if_faller_is_freezed(game_faller:'Faller')->'Faller':
    if game_faller == None:
        return False
    
    for jewel in game_faller.get_jewel_in_faller():
        if jewel.get_status() != 'freeze':
            return False
        
    return True


def change_number_to_color(number:int)->str:
    if number == 0:
        return 'R'
    elif number == 1:
        return 'O'
    elif number == 2:
        return 'Y'
    elif number == 3:
        return 'G'
    elif number == 4:
        return 'B'
    elif number == 5:
        return 'P'
    elif number == 6:
        return 'D'

def create_random_faller(game_state:'GameState')->'Faller':
    random_number_for_col = random.randint(0,5)
    flag = True
    while True:
        if random_number_for_col == 6:
            raise GameOverError
        
        if game_state.get_board()[random_number_for_col][10] != None:
            if flag == True:
                random_number_for_col = -1
                flag = False
            random_number_for_col +=1

        elif game_state.get_board()[random_number_for_col][10] == None:
            break
        
    jewel1_color = change_number_to_color(random.randint(0,6))
    jewel2_color = change_number_to_color(random.randint(0,6))
    jewel3_color = change_number_to_color(random.randint(0,6))
    
    game_faller = set_up_faller(game_state,random_number_for_col,jewel1_color,jewel2_color,jewel3_color)

    return game_faller
    
def change_jewel_list_status(jewel_list:['Jewel'],status:str)->None:
    for jewel in jewel_list:
        if jewel != None:
            jewel.change_status(status)

        
def set_up_faller(game_state:'GameState',col:int,color1:str,color2:str,color3:str)->'Faller':
    if col < 0 or col >= len(game_state.get_board()):
        raise InvalidPositionError


    board = game_state.get_board()

    start_row = len(board[0])+1

    jewel1 = Jewel(start_row , col,color1,'faller')
    jewel2 = Jewel(start_row-1,col,color2,'faller')
    jewel3 = Jewel(start_row-2,col,color3,'faller')

    game_state.add_jewel(jewel3,start_row-2,col)
                
    game_faller = Faller(jewel1,jewel2,jewel3)

    check_jewel = game_faller.get_jewel_in_faller()[2]

    if check_jewel.check_if_jewel_could_move_down(game_state) == False:
        for jewel in game_faller.get_jewel_in_faller():
            jewel.change_status('faller_land')

    return game_faller

    


class GameState:
    def __init__(self):
        self._board = []
 
    def check_game_over_when_time_tick(self,game_faller:'Faller'):
        if game_faller != None:
            if game_faller.get_jewel_in_faller()[2].get_status() == 'freeze':
                for jewel in game_faller.get_jewel_in_faller():
                    if jewel.check_if_jewel_on_board(self) == False:
                        raise GameOverError
        

    def check_game_over_when_set_up_faller(self,row:int,col:int):
        if self.get_board()[col][row] != None:            
            raise GameOverError

 
        
        
    def time_tick(self,game_faller:'Faller',game_state:'GameState')->None:
        match_list = game_state.append_matched_jewel_in_a_list()

        count = len(match_list)

        if count > 0:
            game_state.del_jewel_in_matched_list_from_game_state(match_list)

            for times in range(0,count):
                game_state.all_jewel_move_down()

        if count == 0:
            if game_faller == None:
                return

            if game_faller.get_jewel_in_faller()[2].get_status() == 'faller_land':
                game_faller.change_jewel_status_in_faller('freeze')

            
            elif game_faller.get_jewel_in_faller()[2].get_status() != 'faller_land':
                if game_faller.check_if_faller_could_move_down(game_state) == True:
                    game_faller.faller_move_down(game_state)
                    if game_faller.get_jewel_in_faller()[2].check_if_jewel_could_move_down(game_state) == False:
                        game_faller.change_jewel_status_in_faller('faller_land')

        check_matched_list = game_state.check_match()

        change_jewel_list_status(check_matched_list,'matched')

        self.check_game_over_when_time_tick(game_faller)
                    
                

    def del_jewel_in_matched_list_from_game_state(self,jewel_list:['Jewel']):
        for jewel in jewel_list:
            row = jewel.get_row()
            col = jewel.get_col()

            self.del_jewel(row,col)

    def check_match_and_change_status(self):
        row = len(self.get_board()[0])

        for num in range(0,row):
            self.all_jewel_move_down()

        match_list = self.check_match()

        change_jewel_list_status(match_list,'matched')


    def append_matched_jewel_in_a_list(self)->list:
        match_list = []
        
        for jewel_list in self._board:
            for jewel in jewel_list:
                if jewel != None:
                    if jewel.get_status() == 'matched':
                        match_list.append(jewel)
                    
        return match_list

    
    def get_board(self):
        return self._board

    def initiate_game_board_to_empty(self,row:int,col:int)->None:
        board = []

        if row < 4 or col < 3:
            raise InvalidSizeError
        
        for col_number in range(0,col):
            board_sublist = []
            for row_number in range(0,row):
                board_sublist.append(None)
            board.append(board_sublist)

        self._board = board

        
    def del_jewel(self,row:int,col:int)->None:
        self._board[col][row] = None

        
    def add_jewel(self,jewel:'Jewel',row:int,col:int)->None:
        self._board[col][row] = jewel

        
    def all_jewel_move_down(self):
        for jewel_list in self.get_board():
            for jewel in jewel_list:
                if jewel != None:
                    if jewel.check_if_jewel_could_move_down(self) == True:
                        jewel.move_down(self)

    def check_horizontal_match(self)->['Jewel']:
        row_number = len(self._board[0])
        col_number = len(self._board)
        board = self.get_board()
        match_list = []

        for i in range(0,col_number):
            for j in range(0,row_number):
                color = None
                jewel = board[i][j]
                if jewel != None and jewel.get_status() == 'freeze':
                    color = jewel.get_color()
                    count = 1
                    col = i
                    row = j
                    while True:
                        if col >= col_number-1:
                            break
                        if board[col+1][row]!= None:
                            if board[col+1][row].get_color() == color  and board[col+1][row].get_status() == 'freeze':
                                count += 1
                            if board[col+1][row].get_color() != color:
                                break
                        col +=1
                    if count >=3:
                        for col_num in range(i,i+count):
                            match_list.append(board[col_num][j])

        return match_list


    def check_diagonal_down_match(self)->['Jewel']:
        row_number = len(self._board[0])
        col_number = len(self._board)
        board = self.get_board()
        match_list = []
        for i in range(0,col_number):
            for j in range(0,row_number):
                color = None
                jewel = board[i][j]
                if jewel != None and jewel.get_status() == 'freeze':
                    color = jewel.get_color()
                    count = 1
                    col = i
                    row = j
                    while True:
                        if row < 1 or col >= col_number - 1:
                            break
                        if board[col+1][row-1] != None:
                            if board[col+1][row-1].get_color() == color and board[col+1][row-1].get_status() == 'freeze':
                                count += 1
                            if board[col+1][row-1].get_color() != color:
                                break
                        row -= 1
                        col += 1
                    if count >=3:
                        for count_num in range(0,count):
                            match_list.append(board[i+count_num][j-count_num])

        return match_list


    def check_vertical_match(self)->['Jewel']:
        row_number = len(self._board[0])
        col_number = len(self._board)
        board = self.get_board()
        match_list = []
        for i in range(0,col_number):
            for j in range(0,row_number):
                color = None
                jewel = board[i][j]
                if jewel != None and jewel.get_status() == 'freeze':
                    color = jewel.get_color()
                    count = 1
                    col = i
                    row = j
                    while True:
                        if row >= row_number-1:
                            break
                        if board[col][row+1]!= None:
                            if board[col][row+1].get_color() == color and board[col][row+1].get_status() == 'freeze':
                                count += 1
                            if board[col][row+1].get_color() != color:
                                break
                        row +=1
                    if count >=3:
                        for row_num in range(j,j+count):
                            match_list.append(board[i][row_num])

        return match_list


    
    def check_diagonal_up_match(self)->['Jewel']:
        row_number = len(self._board[0])
        col_number = len(self._board)
        board = self.get_board()
        match_list = []
        for i in range(0,col_number):
            for j in range(0,row_number):
                color = None
                jewel = board[i][j]
                if jewel != None and jewel.get_status() == 'freeze':
                    color = jewel.get_color()
                    count = 1
                    col = i
                    row = j
                    while True:
                        if row >= row_number-1 or col >= col_number - 1:
                            break
                        if board[col+1][row+1]!= None:
                            if board[col+1][row+1].get_color() == color and board[col+1][row+1].get_status() == 'freeze':
                                count += 1
                            if board[col+1][row+1].get_color() != color:
                                break
                        row +=1
                        col += 1
                        
                    if count >=3:
                        for count_num in range(0,count):
                            match_list.append(board[i+count_num][j+count_num])

        return match_list
    

    def check_match(self)->['Jewel']:
        match_list = []

        horizontal_match_list = self.check_horizontal_match()
        vertical_match_list = self.check_vertical_match()
        diagonal_up_match_list = self.check_diagonal_up_match()
        diagonal_down_match_list = self.check_diagonal_down_match()
        
        for jewel in horizontal_match_list:
            if jewel not in match_list:
                match_list.append(jewel)
        for jewel in vertical_match_list:
            if jewel not in match_list:
                match_list.append(jewel)
        for jewel in diagonal_up_match_list:
            if jewel not in match_list:
                match_list.append(jewel)
        for jewel in diagonal_down_match_list:
            if jewel not in match_list:
                match_list.append(jewel)
        
     
        return match_list
    
    
class Jewel:
    def __init__(self,row_position:int,col_position:int,color_information:str,
                 status:str):
        self._col_position = col_position
        self._row_position = row_position
        self._color_information = color_information
        self._status = status


    def change_jewel_position(self,row:int,col:int)->None:
        self._row_position = row
        self._col_position = col

    def position_move_down(self):
        row = self._row_position
        col = self._col_position

        self.change_jewel_position(row-1,col)

    def position_move_left(self):
        row = self._row_position
        col = self._col_position

        self.change_jewel_position(row,col-1)


    def position_move_right(self):
        row = self._row_position
        col = self._col_position

        self.change_jewel_position(row,col+1)

        
    def change_status(self,status:str)->None:
        self._status = status

            
    def get_color(self)->str:
        return self._color_information


    def get_col(self)->int:
        return self._col_position


    def get_row(self)->int:
        return self._row_position

    
    def get_status(self)->str:
        return self._status

    
    def move(self,game_state:GameState,row:int,col:int)->None:
        game_state.add_jewel(self,row,col)



    def move_right(self,game_state:GameState):
        row = self._row_position
        col = self._col_position

        self.move(game_state,row,col+1)
        self.change_jewel_position(row,col+1)
        game_state.del_jewel(row,col)

    def move_left(self,game_state:GameState):
        row = self._row_position
        col = self._col_position

        self.move(game_state,row,col-1)
        self.change_jewel_position(row,col-1)
        game_state.del_jewel(row,col)

        
    def move_down(self,game_state:GameState)->None:
        row = self._row_position
        col = self._col_position
        
        self.move(game_state,row-1,col)
        self.change_jewel_position(row-1,col)

        game_state.del_jewel(row,col)



    def check_if_jewel_could_move_left(self,game_state:GameState):
        board = game_state.get_board()
        
        jewel_row_position = self._row_position
        jewel_col_position = self._col_position
        if self.check_if_jewel_on_board(game_state) == False:
            return True

        if jewel_col_position < 1:
            return False
        
        if board[jewel_col_position-1][jewel_row_position] == None:
            return True

        return False


    def check_if_jewel_could_move_right(self,game_state:GameState):
        board = game_state.get_board()
        
        jewel_row_position = self._row_position
        jewel_col_position = self._col_position

        if self.check_if_jewel_on_board(game_state) == False:
            return True

        if jewel_col_position >= len(board)-1:
            return False
        
        if board[jewel_col_position+1][jewel_row_position] == None:
            return True

        return False

        
    def check_if_jewel_could_move_down(self,game_state:'GameState')->bool:

        board = game_state.get_board()
        
        jewel_row_position = self._row_position
        jewel_col_position = self._col_position

        if jewel_row_position > len(board[0]):
            return True
        
        if jewel_row_position < 1:
            return False
        
        if board[jewel_col_position][jewel_row_position-1] == None:
            return True

        return False


    def check_if_jewel_on_board_after_move_down(self,game_state:'GameState'):
        row = self.get_row()-1
        col = self.get_col()

        if row >= 0 and row < len(game_state.get_board()[0])\
        and col >= 0 and col < len(game_state.get_board()) :
            return True

        return False

    def check_if_jewel_on_board(self,game_state:GameState):
        row_position = self._row_position
        col_position = self._col_position

        board = game_state.get_board()
        
        if row_position >= 0 and row_position < len(board[0]) \
           and col_position >= 0 and col_position < len(board):
            return True

        return False
        

class Faller:
    def __init__(self,jewel1,jewel2,jewel3):
        self._jewel_in_faller = [jewel1,jewel2,jewel3]


    def get_jewel_in_faller(self):
        return self._jewel_in_faller


    def change_jewel_status_in_faller(self,status:str):
        jewel_list = self._jewel_in_faller

        for jewel in jewel_list:
            jewel.change_status(status)

            
    def rotate(self,game_state)->'Faller':

        if self._jewel_in_faller[2].get_status() != 'freeze':
            
        
            t_jewel = Jewel(self._jewel_in_faller[2].get_row()+2,self._jewel_in_faller[2].get_col(),self._jewel_in_faller[2].get_color(),
                                self._jewel_in_faller[2].get_status())
            
            self._jewel_in_faller[2] = Jewel(self._jewel_in_faller[1].get_row()-1,self._jewel_in_faller[1].get_col(),self._jewel_in_faller[1].get_color(),
                                self._jewel_in_faller[1].get_status())

            self._jewel_in_faller[1] = Jewel(self._jewel_in_faller[0].get_row()-1,self._jewel_in_faller[0].get_col(),self._jewel_in_faller[0].get_color(),
                                self._jewel_in_faller[0].get_status())

            self._jewel_in_faller[0] = t_jewel

            for jewel in self.get_jewel_in_faller():
                if jewel.check_if_jewel_on_board(game_state) == True:
                    game_state.add_jewel(jewel,jewel.get_row(),jewel.get_col())


    def faller_move_down(self,game_state):
        for index in reversed(range(0,3)):
            jewel = self.get_jewel_in_faller()[index]
            if jewel.check_if_jewel_on_board_after_move_down(game_state) == True:
                if jewel.check_if_jewel_on_board(game_state) == True:
                    
                    row = jewel.get_row()
                    col = jewel.get_col()
                    game_state.add_jewel(jewel,row-1,col)
                    jewel.change_jewel_position(row-1,col)
                    game_state.del_jewel(row,col)

                elif jewel.check_if_jewel_on_board(game_state) == False:
                    row = jewel.get_row()
                    col = jewel.get_col()

                    game_state.add_jewel(jewel,row-1,col)
                    jewel.change_jewel_position(row-1,col)

            elif jewel.check_if_jewel_on_board_after_move_down(game_state) == False:
                if jewel.get_row() != 0:
                    jewel.position_move_down()


        
                
            
    def check_if_faller_could_move_down(self,game_state):
        if self.get_jewel_in_faller()[2].get_status() == 'freeze':
            return False
        return self.get_jewel_in_faller()[2].check_if_jewel_could_move_down(game_state)
                
        
    def check_if_faller_could_move_left(self,game_state):
        if self.get_jewel_in_faller()[2].get_status() == 'freeze':
            return False
        
        for jewel in self._jewel_in_faller:
            if jewel.check_if_jewel_could_move_left(game_state) == False:
                return False

        return True


    def check_if_faller_could_move_right(self,game_state):
        if self.get_jewel_in_faller()[2].get_status() == 'freeze':
            return False
        
        for jewel in self._jewel_in_faller:
            if jewel.check_if_jewel_could_move_right(game_state) == False:
                return False

        return True


    def check_if_faller_could_move_left_and_move_left(self,game_state):
        if self.check_if_faller_could_move_left(game_state) == True:
            for jewel in self._jewel_in_faller:
                if jewel.check_if_jewel_on_board(game_state) == True:
                    jewel.move_left(game_state)
                elif jewel.check_if_jewel_on_board(game_state) == False:
                    jewel.position_move_left()

            if self.check_if_faller_could_move_down(game_state) == True:
                self.change_jewel_status_in_faller('faller')

            if self.check_if_faller_could_move_down(game_state) == False:
                self.change_jewel_status_in_faller('faller_land') 
                
    def check_if_faller_could_move_right_and_move_right(self,game_state):
        if self.check_if_faller_could_move_right(game_state) == True:
            for jewel in self._jewel_in_faller:
                if jewel.check_if_jewel_on_board(game_state) == True:
                    jewel.move_right(game_state)
                elif jewel.check_if_jewel_on_board(game_state) == False:
                    jewel.position_move_right()

            if self.check_if_faller_could_move_down(game_state) == True:
                self.change_jewel_status_in_faller('faller')

            if self.check_if_faller_could_move_down(game_state) == False:
                self.change_jewel_status_in_faller('faller_land')

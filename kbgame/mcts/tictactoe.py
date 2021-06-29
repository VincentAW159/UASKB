from copy import deepcopy
from mcts import *


class Board():

    def __init__(self, board=None):

        self.player_1 = 'x'
        self.player_2 = 'o'
        self.empty_square = '.'
        

        self.position = {}
        
        self.init_board()

        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)
    
    def init_board(self):
        for row in range(3):
            for col in range(3):
                self.position[row, col] = self.empty_square
    
    def make_move(self, row, col):

        board = Board(self)
        

        board.position[row, col] = self.player_1
        

        (board.player_1, board.player_2) = (board.player_2, board.player_1)
    

        return board
    

    def is_draw(self):
        for row, col in self.position:
            if self.position[row, col] == self.empty_square:
                return False
        

        return True
    

    def is_win(self):
        

        for col in range(3):

            winning_sequence = []
            

            for row in range(3):
 
                if self.position[row, col] == self.player_2:

                    winning_sequence.append((row, col))
                    
  
                if len(winning_sequence) == 3:

                    return True
       

        for row in range(3):

            winning_sequence = []
            

            for col in range(3):

                if self.position[row, col] == self.player_2:

                    winning_sequence.append((row, col))
                    

                if len(winning_sequence) == 3:

                    return True
        winning_sequence = []

        for row in range(3):
 
            col = row
        
  
            if self.position[row, col] == self.player_2:
 
                winning_sequence.append((row, col))
                
 
            if len(winning_sequence) == 3:

                return True
        
        
        # define winning sequence list
        winning_sequence = []
        
        # loop over board rows
        for row in range(3):
            # init column
            col = 3 - row - 1
        
            # if found same next element in the row
            if self.position[row, col] == self.player_2:
                # update winning sequence
                winning_sequence.append((row, col))
                
            # if we have 3 elements in the row
            if len(winning_sequence) == 3:
                # return the game is won state
                return True
        
        # by default return non winning state
        return False
    
    # generate legal moves to play in the current position
    def generate_states(self):
        # define states list (move list - list of available actions to consider)
        actions = []
        
        # loop over board rows
        for row in range(3):
            # loop over board columns
            for col in range(3):
                # make sure that current square is empty
                if self.position[row, col] == self.empty_square:
                    # append available action/board state to action list
                    actions.append(self.make_move(row, col))
        
        # return the list of available actions (board class instances)
        return actions
    
    # main game loop
    def game_loop(self):
        print('\n  Tic Tac Toe \n')
        print('  Type "exit" to quit the game')
        print('  Move format [x,y]: 1,2 where 1 is column and 2 is row')
        
        # print board
        print(self)
        
        # create MCTS instance
        mcts = MCTS()
                
        # game loop
        while True:
            # get user input
            user_input = input('> ')
        
            # escape condition
            if user_input == 'exit': break
            
            # skip empty input
            if user_input == '': continue
            
            try:
                # parse user input (move format [col, row]: 1,2) 
                row = int(user_input.split(',')[1]) - 1
                col = int(user_input.split(',')[0]) - 1

                # check move legality
                if self.position[row, col] != self.empty_square:
                    print(' Illegal move!')
                    continue

                # make move on board
                self = self.make_move(row, col)
                
                # print board
                print(self)
                
                # search for the best move
                best_move = mcts.search(self)
                
                # legal moves available
                try:
                    # make AI move here
                    self = best_move.board
                
                # game over
                except:
                    pass
                
                # print board
                print(self)
                
                # check if the game is won
                if self.is_win():
                    print('player "%s" has won the game!\n' % self.player_2)
                    break
                
                # check if the game is drawn
                elif self.is_draw():
                    print('Game is drawn!\n')
                    break
            
            except Exception as e:
                print('  Error:', e)
                print('  Illegal command!')
                print('  Move format [x,y]: 1,2 where 1 is column and 2 is row')
        
    # print board state
    def __str__(self):
        # define board string representation
        board_string = ''
        
        # loop over board rows
        for row in range(3):
            # loop over board columns
            for col in range(3):
                board_string += ' %s' % self.position[row, col]
            
            # print new line every row
            board_string += '\n'
        
        # prepend side to move
        if self.player_1 == 'x':
            board_string = '\n--------------\n "x" to move:\n--------------\n\n' + board_string
        
        elif self.player_1 == 'o':
            board_string = '\n--------------\n "o" to move:\n--------------\n\n' + board_string
                        
        # return board string
        return board_string

# main driver
if __name__ == '__main__':
    # create board instance
    board = Board()
    
    # start game loop
    board.game_loop()
# A simple tic tac toe game run from command line

'''
Requirments:
have a board state that can be modified by the user and the computer opponent. Start with user and user verion and expand to computer 'AI'
take input from user on where to place X or O.
display the board state for the user for every move
determine after every round if a win has happened, or if a draw has happened. Fastest win is at player turn 3

example board render:
   a.  b.  c.
1.   |   |  
   ----------
2.   |   |  
   ----------
3.   |   |  

take user input
Enter your position (ex. a1, b3, c2) ---> 

'''

def play(board, position, player): #helper function to modify the board
    Xcoord = {'1':0,'2':1,'3':2}
    Ycoord = {'a':0,'b':1,'c':2}
    board[Xcoord[position[0]]][Ycoord[position[1]]] = player
    return board

def printBoard(board):# prints the current board state
    print('   a.  b.  c.')
    print('1. {} | {} | {}'.format(board[0][0], board[0][1], board[0][2]))
    print('   ----------')
    print('2. {} | {} | {}'.format(board[1][0], board[1][1], board[1][2]))
    print('   ----------')
    print('3. {} | {} | {}'.format(board[2][0], board[2][1], board[2][2]))
    return

def didWin(board, player): #looks at the 8 possible lines and if any are all the same, returns a True result
    result = False
    check = [
        [board[0][0],board[1][0],board[2][0]],
        [board[0][1],board[1][1],board[2][1]],
        [board[0][2],board[1][2],board[2][2]],
        [board[0][0],board[0][1],board[0][2]],
        [board[1][0],board[1][1],board[1][2]],
        [board[2][0],board[2][1],board[2][2]],
        [board[0][0],board[1][1],board[2][2]],
        [board[0][2],board[1][1],board[2][0]]]

    for i in check:
        result = all(ele == player for ele in i)
    print(result)
    return result


def game(): #where the game and turn loop takes place
    board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    result = False
    userInput = ''
    player = 'X'

    while not result:
        printBoard(board)
        userInput = input('Enter your position (ex. 1a, b3, c2) ---> ')#need to ensure user inputs proper expression, this will break currently if not8
        board = play(board, userInput, player)
        if didWin(board, player):
            result = True
            print('Player ' + player + ' Won this game!')
            printBoard(board)
        if player == 'X': player = 'O'
        else: player = 'X'
        



    return



def main(): #where the game loop takes place and tallying results of win and losses
    rounds = 5
    win, loss = 0,0

    for i in range(rounds):
        if game():
            win+=1
        else:
            loss+=1
        print('wins: ' + str(win) + ' loss: ' + str(loss))

    return


if __name__ == '__main__':
    main()
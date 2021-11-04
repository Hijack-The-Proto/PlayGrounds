def gameOfLife(board):
    X, Y = len(board), len(board[0])
    tmpBoard = [[0 for a in range(Y)] for b in range(X)]
    
    def search(x, y, board):
        r = 0
        ones=0
        X, Y = len(board), len(board[0])
        mod = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

        for i in mod:
            if 0 <= x+i[0] < X and 0 <= y+i[1] < Y:
                ones+= board[x+i[0]][y+i[1]]

        if board[x][y] == 1:
            if ones < 2: r=0
            if 2<= ones <=3: r=1
            if ones > 3: r=0
        else:
            if ones == 3: r=1
        return r
    
    for i in range(X):
        for j in range(Y):
            tmpBoard[i][j] = search(i, j, board)
            
    for i in range(X):
        for j in range(Y):
            board[i][j]=tmpBoard[i][j]

def main():
    board =[[0,1,0,1,0,0,1,1],
            [0,0,1,1,1,0,0,1],
            [1,1,1,0,0,1,0,0],
            [0,0,0,1,1,0,1,0],
            [0,0,1,1,0,1,0,1],
            [1,1,0,1,0,0,0,0]]
    for i in board:
        print(i)

    for x in range(10):
        gameOfLife(board)
        print('\n')
        for i in board:
            print(i)

if '__main__' == __name__:
    main()


'''
        TOP=False
        BOTTOM=False
        RIGHT=False
        LEFT=False
        
        
        if x > 0: #check top
            ones += board[x-1][y]
            TOP=True
        if x < X-1: #check bottom
            ones += board[x+1][y]
            BOTTOM=True
        if y > 0: #Check left
            ones += board[x][y-1]
            LEFT=True
        if y < Y-1: #Check right
            ones += board[x][y+1]
            RIGHT=True
            
        if TOP and RIGHT: #Check topright
            ones += board[x-1][y+1]
        if TOP and LEFT: #check topleft
            ones += board[x-1][y-1]
        if BOTTOM and RIGHT: #Check bottomright
            ones += board[x+1][y+1]
        if BOTTOM and LEFT: #Check bottomleft
            ones += board[x+1][y-1]
        '''
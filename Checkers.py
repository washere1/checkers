from tkinter import *
from tkinter import messagebox as mbx

class CheckersBoard:
    '''represents a board of Checkers'''

    def __init__(self):
        '''CheckersBoard()
        creates a CheckersBoard in starting position'''
        self.board = {}  # dict to store position
        # create opening position
        for row in range(8):
            for column in range(8):
                coords = (row, column)
                if row in [0, 2]:
                    if column in [1, 3, 5, 7]:
                        self.board[coords] = 0
                    else:
                        self.board[coords] = None
                elif row == 1:
                    if column in [0,2,4,6]:
                        self.board[coords] = 0
                    else:
                        self.board[coords] = None
                elif row in [5 ,7]:
                    if column in [0,2,4,6]:
                        self.board[coords] = 1
                    else:
                        self.board[coords] = None
                elif row == 6:
                    if column in [1,3,5,7]:
                        self.board[coords] = 1
                    else:
                        self.board[coords] = None
                else:
                    self.board[coords] = None
                        
        self.currentPlayer = 0  # player 0 starts
        self.endgame = None  # replace with string when game ends

    def get_piece(self,coords):
        '''CheckersBoard.get_piece(coords) -> int
        returns the piece at coords'''
        return self.board[coords]

    def get_endgame(self):
        '''CheckersBoard.get_endgame() -> None or str
        returns endgame state'''
        return self.endgame

    def get_player(self):
        '''CheckersBoard.get_player() -> int
        returns the current player'''
        return self.currentPlayer

    def next_player(self):
        '''CheckersBoard.next_player()
        advances to next player'''
        self.currentPlayer = 1 - self.currentPlayer

    def get_scores(self):
        '''CheckersBoard.get_scores() -> tuple
        returns a tuple containing player 0's and player 1's scores'''
        pieces = list( self.board.values() )  # list of all the pieces
        # count the number of pieces belonging to both players
        return pieces.count(0), pieces.count(1)

    def check_endgame(self):
        '''CheckersBoard.check_endgame()
        checks if game is over
        updates endgameMessage if over'''
        scores = self.get_scores()
        counter = 0
        for score in scores:
            if score == 0:
                self.endgame = counter
            else:
                counter += 1

class CheckersSquare(Canvas):
    '''displays a square in the Checkers game'''

    def __init__(self,master,r,c, color):
        '''ReversiSquare(master,r,c)
        creates a new blank Reversi square at coordinate (r,c)'''
        # create and place the widget
        Canvas.__init__(self,master,width=50,height=50,bg=color)
        self.grid(row=r,column=c)
        # set the attributes
        self.position = (r,c)
        # bind button click to placing a piece
        self.bind('<Button>',self.clicked)
        self.isOpen = True
        self.isKing = False

    def get_position(self):
        '''ReversiSquare.get_position() -> (int,int)
        returns (row,column) of square'''
        return self.position

    def clicked(self, event):
        if  not self.isOpen:
            self.master.selectedPiece = ()
            self.master.selectedPiece = (self, self.master.colors[self.master. \
                                                                 board.get_piece(self.position)])
            self['highlightbackground'] = 'blue2'
                
            for piece in self.master.squares.values():
                if piece != self:
                    piece['highlightbackground'] = 'white'
                
        else:
            if len(self.master.selectedPiece) != 0:
                currentPlayer = self.master.board.get_player()
                pieceColor = self.master.board.get_piece(self.master. \
                                                     selectedPiece[0].position)

                if currentPlayer == pieceColor:
                    if self.master.selectedPiece[0].isKing:
                        validMoves = self.master.get_diags(self.master.selectedPiece[0], False, True)
                    else:
                        validMoves = self.master.get_diags(self.master.selectedPiece[0])
                    if self in validMoves:
                        self.make_color(self.master.selectedPiece[1])
                        self.master.add_piece(self, self.master.selectedPiece[0])
                        self.isOpen = False
                        
                        self.master.remove_piece(self.master.selectedPiece[0])
                        self.master.selectedPiece[0]['highlightbackground'] = 'white'
                        self.master.selectedPiece[0].remove_token()
                        self.master.selectedPiece[0].isOpen = True

                        if self.master.selectedPiece[0].isKing:
                                self.add_king()
                        else:
                            self.master.check_king(self.position)
                        
                        self.master.selectedPiece = ()
                        self.master.update_display()
                
                    else:
                        clickedDiags = self.master.get_diags(self, True)
                        selectedDiags = self.master.get_diags(self.master.selectedPiece[0], True)

                        overLap = 0
                        finished = False
                        for i in clickedDiags:
                            if not finished:
                                for j in selectedDiags:
                                    if i == j:
                                        overLapVal = self.master.board.get_piece(i.position)
                                        otherVal = self.master.board.get_piece(self.master.selectedPiece[0].position)
                                        if overLapVal != otherVal:
                                            overLap = i
                                            if not overLap.isOpen:
                                                finished = True
                            else:
                                break

                        if overLap != 0:
                            self.make_color(self.master.selectedPiece[1])
                            self.master.add_piece(self, self.master.selectedPiece[0])
                            self.isOpen = False

                            self.master.remove_piece(self.master.selectedPiece[0])
                            self.master.selectedPiece[0]['highlightbackground'] = 'white'
                            self.master.selectedPiece[0].remove_token()
                            self.master.selectedPiece[0].isOpen = True

                            self.master.remove_piece(overLap)
                            overLap.remove_token()
                            overLap.isOpen = True

                            if self.master.selectedPiece[0].isKing:
                                self.add_king()
                            else:
                                self.master.check_king(self.position)
                            
                            self.master.selectedPiece = ()
                            self.master.update_display()
                                
                        else:
                            return #do nothing
                    
    def make_color(self,color):
        '''ReversiSquare.make_color(color)
        changes color of piece on square to specified color'''
        ovalList = self.find_all()  # remove existing piece
        for oval in ovalList:
            self.delete(oval)
        self.create_oval(10,10,44,44,fill=color)
        if self.isKing:
            self.create_text(28, 35, font = ("Helvectia", 24), text = '*')

    def remove_token(self):
        ovalList = self.find_all()  # remove piece
        for oval in ovalList:
            self.delete(oval)

    def add_king(self):
        self.create_text(28, 35, font = ("Helvectia", 24), text = '*')
        self.isKing = True

class CheckersGame(Frame):
    '''represents a game of Checkers'''

    def __init__(self,master):
        '''CheckersGame(master,[computerPlayer])
        creates a new Reversi game'''
        # initialize the Frame
        Frame.__init__(self,master,bg='white')
        self.grid()
        # set up game data
        self.colors = ('gray','red')  # players' colors
        # create board in starting position, player 0 going first
        self.board = CheckersBoard()
        self.selectedPiece = () #will need later for moving pieces
        self.jumpInProgress = False #will need later for jumping
        self.validMoves = '' #need later for storing valid moves
        self.validJumps = '' #as above except jumps
        self.squares = {}  # stores CheckersSquares
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                if row%2 == 0:
                    if column%2 == 0:
                        self.squares[rc] = CheckersSquare(self,row,column,"black")
                    else:
                        self.squares[rc] = CheckersSquare(self,row,column,"white")
                else:
                    if column%2 == 0:
                        self.squares[rc] = CheckersSquare(self,row,column,"white")
                    else:
                        self.squares[rc] = CheckersSquare(self,row,column,"black")

                        
        # set up scoreboard and status markers
        self.rowconfigure(8,minsize=3)  # leave a little space
        self.turnSquares = []  # to store the turn indicator squares
        self.update_display()


    def select_piece(self,event, origSquare):
        '''ReversiGame.get_click(event)
        event handler for mouse click
        gets click data and tries to make the move'''
        coords = event.widget.get_position()
        pieceNum = self.board.board[coords]
        piece = self.squares.get(coords)
        
        if pieceNum is not None:
            piece['highlightbackground'] = 'purple2'
            piece['highlightthickness'] = 3
            self.selectedPiece = piece
        else:
            self.move_piece()
                    
    def remove_piece(self, pieceToRemove):
        piece = pieceToRemove
        self.board.board[piece.position] = None

    def add_piece(self, pieceToAdd, other):
        piece = pieceToAdd
        pieceNum = self.board.get_piece(other.position)
        self.board.board[piece.position] = pieceNum

    def check_king(self, pieceCoord):
        coord = pieceCoord
        pieceNum = self.board.get_piece(coord)
        if pieceNum == 0:
            if coord[0] == 7:
                actualPiece =  self.squares.get(coord)
                actualPiece.add_king()
        else:
            if coord[0] == 0:
                actualPiece =  self.squares.get(coord)
                actualPiece.add_king()
                
    def find_jumps(self, piece, piece2 = None):
        clicked = piece
        if piece2 == None:
            piece2 = self.selectedPiece[0]
        clickedDiags = self.get_diags(clicked, True)
        selectedDiags = self.get_diags(piece2, True)
        returnList = []

        overLap = 0
        finished = False
        for i in clickedDiags:
            if not finished:
                for j in selectedDiags:
                    if i == j:
                        overLapVal = self.board.get_piece(i.position)
                        otherVal = self.board.get_piece(piece.position)
                        if overLapVal != otherVal:
                            overLap = i
                            if i == clickedDiags[-1]:
                                finished = True
                            if not overLap.isOpen:
                                returnList.append(overLap)
            else:
                break
            return returnList
        
                
    def get_diags(self, piece, checkFilled = False, isKing = False):
        diagonalList = []
        validDiagonals = []
        coord = piece.position
        pieceNum = self.board.get_piece(coord)

        if pieceNum == 0 and not checkFilled and not isKing:
            rightUp = (coord[0] + 1, coord[1] + 1)
            rightDown = (coord[0] + 1, coord[1] - 1)
            diagonalList.extend([rightUp, rightDown])
        elif pieceNum == 1 and not checkFilled and not isKing:
            leftUp = (coord[0] - 1, coord[1] + 1)
            leftDown = (coord[0] - 1, coord[1] - 1)
            diagonalList.extend([leftUp, leftDown])
        elif isKing:
            rightUp = (coord[0] + 1, coord[1] + 1)
            rightDown = (coord[0] + 1, coord[1] - 1)
            leftUp = (coord[0] - 1, coord[1] + 1)
            leftDown = (coord[0] - 1, coord[1] - 1)
            diagonalList.extend([rightUp, rightDown, leftUp, leftDown])
        else:
            rightUp = (coord[0] + 1, coord[1] + 1)
            rightDown = (coord[0] + 1, coord[1] - 1)
            leftUp = (coord[0] - 1, coord[1] + 1)
            leftDown = (coord[0] - 1, coord[1] - 1)
            diagonalList.extend([rightUp, rightDown, leftUp, leftDown])

        for coord in diagonalList:
            if coord in self.squares.keys():
                if not checkFilled:
                    if self.squares[coord].isOpen:
                        validDiagonals.append(self.squares[coord])
                else:
                    validDiagonals.append(self.squares[coord])
        
        return validDiagonals        
        
    def pass_move(self):
        '''ReversiGame.pass_move()
        event handler for Pass button
        passes for the player's turn'''
        self.board.next_player()  # move onto next player
        self.update_display()

    def update_display(self):
        '''ReversiGame.update_display()
        updates squares to match board
        also updates scoreboard'''
        # update squares
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                piece = self.board.get_piece(rc)
                if piece is not None:
                    square = self.squares[rc]
                    square.make_color(self.colors[piece])
                    square.isOpen = False
                    
                    
        # update the turn indicator
        self.board.next_player()
        newPlayer = self.board.get_player()
        oldPlayer = 1 - newPlayer
        self['highlightbackground'] = self.colors[newPlayer]
        self['highlightthickness'] = 9


        # if game over, show endgame message
        self.board.check_endgame()
        endgame = self.board.get_endgame()
        if endgame is not None:  # if game is over
            # remove the turn indicator
            #self.turnSquares[newPlayer]['highlightbackground'] = 'white'
            if isinstance(endgame,int):  # if a player won
                winner = self.colors[endgame]  # color of winner
                endgameMessage = '{} wins!'.format(winner.title())
            else:
                endgameMessage = "It's a tie!"
            mxb.showinfo(title = "Endgame", message = endgameMessage)
            Label(self,text=endgameMessage,font=('Arial',18)).grid(row=9,column=2,columnspan=4)

def play_checkers():
    '''play_reversi()
    starts a new game of Reversi'''
    root = Tk()
    root.title('CHECKERS')
    RG = CheckersGame(root)
    RG.mainloop()

play_checkers()

## AoPS GRADE IS BELOW##


##Technical Score: 5 / 7
##Style Score: 0.7 / 1
##Comments:
##A good attempt at this week's solution! You have the basic functionality of moving and overtaking pieces covered!
##
##One of the requirements for this problem was to oblige a player to take an opponent's checker whenever they can. One way to implement this is to scan all the checkers of a player to see if they're in a position to take an opponent's checker and only allow them to be selected. Of course, if there are no such checkers, the player would be free to select whichever piece they like.
##
##Another requirement was to allow the player to continue jumping and take the opponent's checker with a single one during their turn. One possibility of solving this is to keep scanning the checker that was just moved until there are no checkers it can overtake. Only then can you toggle the current player and switch it to the opponent.
##
##Recall that only the king can jump backward. Notice that your game allows any piece to jump backwards if there is an opponent's piece to take in that direction.
##
##You also don't display any messages for winning or losing. That's because you've misspelled $\verb#mxb#$ on line 380. Try to be more careful and proofread your solutions in the future to avoid such inaccuracies.
##
##On line 107, among others, you're accessing the $\verb#selectedPiece#$ attribute of a board from outside its class. This goes against one of the principles of OOP, which states that you shouldn't reveal the implementation of the class to the outside world. Instead, be sure to define setters and getters and use them instead. That way, you won't reveal the underlying implementation (i.e. attributes) but just the interface (i.e. methods) of a class.
##
##From a semantic standpoint, it would be better for the click action to be delegated to the board class. This is because clicking on a square requires additional information about the surroundings of the board, and it shouldn't be the responsibility of the cell class to know about its surroundings - that's the job of the board class. Try to refactor your code so that the bulk of the action handling the click on a square is moved to the board class.
##
##The conditions on lines 18-39 can be improved and summarized better. Try to think of a dependency between the remainder that the sum of the column and row of a square gives when divided by 2. This should give you which squares can hold game pieces. In order to generate the players' checkers, an additional condition about the row (using greater than or less than) would suffice.
##
##Take a look at lines 323-334. There, you have an $\verb#elif#$ clause and an $\verb#else#$ clause that do the exact same thing. This means that you just need one $\verb#else#$ clause to fulfill your logic.
##
##In terms of style, good job using mostly meaningful variable names! However, some of them can be improved, in particular, in your $\verb#clicked#$ method. There, for example, you have variables $\verb#selectedDiags#$ and $\verb#clickedDiags#$. Wouldn't that mean the same thing? Also, how can you actually select diagonals in this game? You're selecting a destination square, not the whole diagonal. Try to be a bit more precise with your variable names in the future.
##
##This method in particular would benefit from some comments that would help guide the reader through the code. Make sure you also include docstrings for all your methods as well to boost your readability.
##
##Well done adding a description of your approach in the text box! However, don't forget to include information about testing, too. This is important because it's the only way to guarantee that our code works as expected. Here, testing would consist of trying out the core mechanics of the game, such as movement and capturing, as well as more advanced ones, such as turning into a king, correct king behavior, jump obligation, and ability to chain jump within a single turn.
##
##Keep working hard!

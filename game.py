from tkinter import *
import random
game = Tk()
game.title("TIC TAC TOE")
game.geometry("450x555")

# create text label in frame
with_AI = Label(text="Play with AI:",
                font=("Helvatica", 15), fg="#000000")
with_AI.grid(row=0, column=0, columnspan=2, sticky='e')
# create checkbox in frame
yes_AI = IntVar()
Checkbutton(game, variable=yes_AI).grid(row=0, column=2, sticky='w')
# create text label in frame
textPlay = Label(text="Start", font=("Helvatica", 15), fg="red")
textPlay.grid(row=1, column=0, columnspan=3)


# randomly choose 1st player
temp = random.choice([0, 1])
if temp == 0:
    player = 'O'
else:
    player = 'X'
stop_game = False


# minimax algorithm using alpha beta pruning
# this returns the scores of each possible move
def minimax(states, depth, isMax, playerAI, scores, alpha, beta):

    # return score if winner is found
    # this is also the end of recursive loop
    result = checkWinner1()
    if result != None:
        return scores[result]-depth

    # for maximizing move i.e. AI move
    if isMax:
        bestVal = -1000
        for i in range(3):
            for j in range(3):
                if states[i][j] == 0:
                    states[i][j] = playerAI
                    bestVal = minimax(states, depth + 1, False,
                                      playerAI, scores, alpha, beta)
                    states[i][j] = 0
                    alpha = max(alpha, bestVal)
                    if alpha >= beta:
                        break
        return alpha
    # for minimizing move i.e. human player move
    else:
        bestVal = 1000
        for i in range(3):
            for j in range(3):
                if states[i][j] == 0:
                    if playerAI == 'X':
                        states[i][j] = 'O'
                    else:
                        states[i][j] = 'X'
                    bestVal = minimax(states, depth + 1, True,
                                      playerAI, scores, alpha, beta)
                    states[i][j] = 0
                    beta = min(beta, bestVal)
                    if alpha >= beta:
                        break
        return beta

# this functions compares the scores and provide the position of best move (maximum score) for AI

def bestMove(states, playerAI, scores):
    bestVal = -1000
    for i in range(3):
        for j in range(3):
            if states[i][j] == 0:
                states[i][j] = playerAI
                moveVal = minimax(states, 0, False, playerAI,
                                  scores, -1000, 1000)
                states[i][j] = 0
                if moveVal > bestVal:
                    bestRow = i
                    bestColumn = j
                    bestVal = moveVal
    return bestRow, bestColumn

# this function changes the frame(display) on clicking any of the buttons


def callback(r, c):
    global player
    global textPlay
    global states
    global yes_AI
#2 player
    if player == 'X' and states[r][c] == 0 and stop_game == False:
        board[r][c].configure(text='X', fg='#76D7C4')
        states[r][c] = 'X'
        player = 'O'
        textPlay.config(text="O's turn")
        checkWinner()
        if yes_AI.get() == 1 and stop_game == False:
            scores = {'X': -10, 'O': 10, 'tie': 0}
            bestRow, bestColumn = bestMove(states, player, scores)
            board[bestRow][bestColumn].configure(text='O', fg='#FDD835')
            states[bestRow][bestColumn] = 'O'
            player = 'X'
            textPlay.config(text="X's turn")

    if player == 'O' and states[r][c] == 0 and stop_game == False:
        board[r][c].configure(text='O', fg='#FDD835')
        states[r][c] = 'O'
        player = 'X'
        textPlay.config(text="X's turn")
        checkWinner()
        if yes_AI.get() == 1 and stop_game == False:
            scores = {'X': 10, 'O': -10, 'tie': 0}
            bestRow, bestColumn = bestMove(states, player, scores)
            board[bestRow][bestColumn].configure(text='X', fg='#76D7C4')
            states[bestRow][bestColumn] = 'X'
            player = 'O'
            textPlay.config(text="O's turn")

    checkWinner()


# check the winner but does not change the frame(display)
def checkWinner1():
    global states

    win = None

    for i in range(3):
        if states[i][0] == states[i][1] == states[i][2] != 0:
            if states[i][0] == 'X':
                win = 'X'
            else:
                win = 'O'

    for i in range(3):
        if states[0][i] == states[1][i] == states[2][i] != 0:
            if states[0][i] == 'X':
                win = 'X'
            else:
                win = 'O'

    if states[0][0] == states[1][1] == states[2][2] != 0:
        if states[1][1] == 'X':
            win = 'X'
        else:
            win = 'O'

    if states[2][0] == states[1][1] == states[0][2] != 0:
        if states[1][1] == 'X':
            win = 'X'
        else:
            win = 'O'

    if win == None:
        temp1 = 0
        for i in range(3):
            for j in range(3):
                if states[i][j] == 0:
                    temp1 = 1
        if temp1 == 0:
            win = 'tie'

    return win


# check the winner and also change the frame(display)
def checkWinner():
    global stop_game
    global states
    global board

    win = None

    win_color = '#7D6608'
    for i in range(3):
        if states[i][0] == states[i][1] == states[i][2] != 0:
            board[i][0].config(bg=win_color)
            board[i][1].config(bg=win_color)
            board[i][2].config(bg=win_color)
            stop_game = True
            if states[i][0] == 'X':
                textPlay.config(text="X wins! Click on 'Reset' to play again.")
                win = 'X'
            else:
                textPlay.config(text="O wins! Click on 'Reset' to play again.")
                win = 'O'

    for i in range(3):
        if states[0][i] == states[1][i] == states[2][i] != 0:
            board[0][i].config(bg=win_color)
            board[1][i].config(bg=win_color)
            board[2][i].config(bg=win_color)
            stop_game = True
            if states[0][i] == 'X':
                textPlay.config(text="X wins! Click on 'Reset' to play again.")
                win = 'X'
            else:
                textPlay.config(text="O wins! Click on 'Reset' to play again.")
                win = 'O'

    if states[0][0] == states[1][1] == states[2][2] != 0:
        board[0][0].configure(bg=win_color)
        board[1][1].configure(bg=win_color)
        board[2][2].configure(bg=win_color)
        stop_game = True
        if states[1][1] == 'X':
            textPlay.config(text="X wins! Click on 'Reset' to play again.")
            win = 'X'
        else:
            textPlay.config(text="O wins! Click on 'Reset' to play again.")
            win = 'O'

    if states[2][0] == states[1][1] == states[0][2] != 0:
        board[2][0].configure(bg=win_color)
        board[1][1].configure(bg=win_color)
        board[0][2].configure(bg=win_color)
        stop_game = True
        if states[1][1] == 'X':
            textPlay.config(text="X wins! Click on 'Reset' to play again.")
            win = 'X'
        else:
            textPlay.config(text="O wins! Click on 'Reset' to play again.")
            win = 'O'

    if stop_game == False:
        temp1 = 0
        for i in range(3):
            for j in range(3):
                if states[i][j] == 0:
                    temp1 = 1
        if temp1 == 0:
            textPlay.configure(
                text="It's a tie! Click on 'Reset' to play again.")
            win = 'tie'
            stop_game = True

    return win


# resets all the values when reset button is clicked
def reset():
    global stop_game
    global player
    global board
    global states
    for i in range(3):
        for j in range(3):
            board[i][j].configure(text=' ', fg='#ffda30', bg="#330066")
            states[i][j] = 0
    stop_game = False
    textPlay.configure(text="Start the Game!!!")
    temp = random.choice([0, 1])
    if temp == 0:
        player = 'O'
    else:
        player = 'X'

    temp2 = random.choice([0, 1])
    temp3 = random.choice([0, 1])
    if yes_AI.get() == 1:
        if temp2 == 0:
            if temp3 == 0:
                scores = {'X': -10, 'O': 10, 'tie': 0}
                bestRow, bestColumn = bestMove(states, player, scores)
                board[bestRow][bestColumn].configure(text='O', fg='#FDD835')
                states[bestRow][bestColumn] = 'O'
                player = 'X'
                textPlay.config(text="X's turn")
            else:
                scores = {'X': 10, 'O': -10, 'tie': 0}
                bestRow, bestColumn = bestMove(states, player, scores)
                board[bestRow][bestColumn].configure(text='X', fg='#76D7C4')
                states[bestRow][bestColumn] = 'X'
                player = 'O'
                textPlay.config(text="O's turn")


# initialize frame values
f = [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]]
# initialize board values
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
# initialize player states i.e. 0(empty), X or O
states = [[0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]

# creates a board of 3x3 with buttons
for i in range(3):
    for j in range(3):
        f[i][j] = Frame(game, width=150, height=150)
        f[i][j].propagate(False)
        f[i][j].grid(row=i+2, column=j, sticky="nsew", padx=1, pady=1)
        board[i][j] = Button(f[i][j], font=("Helvatica", 70), bg="#330066", fg="#ffda30",
                             command=lambda r=i, c=j: callback(r, c))
        board[i][j].pack(expand=True, fill=BOTH)

# create reset button
reset_game = Button(text="Reset the game!", font=("Helvatica", 15), bg="#ffda30", fg="#000000",
                    command=lambda: reset())
reset_game.grid(row=5, column=0, columnspan=2, sticky='nsew')

# create quit button
quit_game = Button(text="Quit game!", font=("Helvatica", 15), bg="#ffda30", fg="purple",
                   command=lambda: game.destroy())
quit_game.grid(row=5, column=2, sticky='nsew')

# make game window non-resizable
game.resizable(False, False)
# run all
game.mainloop()

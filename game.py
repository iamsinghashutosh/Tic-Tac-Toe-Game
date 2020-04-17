from tkinter import *
from tkinter import messagebox
import random
window=Tk()

window.title("Artificial Intelligence Assignment 2")
window.geometry("800x600")
window.configure(bg="yellow")

HOST = '127.0.0.1' 
PORT = 65005        

player = "X"
turn = 0
hidden_grid = []
gamemode = "Standard"
aiMode = "vs Player"
text = " "
button = []
settingButtons = []

iterationLimit = 10
gridSize = 9
winLength = 3

lblGrid=Label(window, text="Grid Size")
lblGrid.grid(row=2, column=5)
lblWin=Label(window, text="Win length")
lblWin.grid(row=3, column=5)


e1 = Entry(window)
e2 = Entry(window)


e1.grid(row=2, column=4)
e2.grid(row=3, column=4)

def generate_seed():
    seed = []
    memCounter = 0
    while len(seed) < gridSize and memCounter < 50:
        memCounter = 0
        rand = random.randint(0,gridSize-1)
        for number in seed:
            if(rand == number):
                memCounter = memCounter + 1
        if(memCounter == 0):
            seed.append(rand)
    return seed

def begin():
    lbl=Label(window,text="Tic-tac-toe Game",font=('none 24 bold','15'),bg="yellow")
    lbl.config(anchor=CENTER)
    lbl.grid(row=0,column=0)
    settingButtons.append(Button(window, text="Reset",bg="Red", fg="White",width=7,height=1,font=('none 24 bold','10'),command=lambda:reset()))
    settingButtons[0].grid(row = 1, column = 0)
    settingButtons.append(Button(window, text="vs Player",bg="Black", fg="White",width=10,height=1,font=('none 24 bold','10'),command=lambda:aiClick(settingButtons[1])))
    settingButtons[1].grid(row = 3, column = 0)
    settingButtons.append(Button(window, text="Start game",bg="Black", fg="White",width=10,height=1,font=('none 24 bold','10'),command=lambda:completeSetup(settingButtons[2], settingButtons[4], int(e1.get()), int(e2.get()), str(0), int(0))))
    settingButtons[2].grid(row = 1, column = 4)
    settingButtons.append(Button(window, text="Player: X",bg="Black", fg="White",width=10,height=1,font=('none 24 bold','10'),command=lambda:playerClick(settingButtons[3])))
    settingButtons[3].grid(row = 1, column = 5)
    settingButtons.append(Button(window, text="Fixed Grid",bg="Black", fg="White",width=10,height=1,font=('none 24 bold','10'),command=lambda:completeSetup(settingButtons[4], settingButtons[2], 9, 3, HOST, PORT)))
    settingButtons[4].grid(row = 1, column = 6)
# The "Fixed Grid" button implements the first part of the assignment i.e. Simple Tic-tac-Toe Game with Grid Size of 9 and 3 same symbols required to win.

def completeSetup(self, buttonTwo, eGridSize, eWinLength, eHOST, ePORT):
    global HOST
    global PORT
    HOST = eHOST
    PORT = ePORT

    self.destroy()
    buttonTwo.destroy()
    lblGrid.destroy()
    lblWin.destroy()
    e1.destroy()
    e2.destroy()

    global hidden_grid
    global button
    global player

    global gridSize
    global winLength

    gridSize = eGridSize
    winLength = eWinLength
    rowSize = int(pow(gridSize, 0.5) + 0.99)

    for i in range(gridSize):
        button.append(Button(window, text=" ",bg="lightblue", fg="Black",width=3,height=1,font=('Helvetica',int(210/rowSize)),command=lambda i=i:clicked(button[i], button, i)))
        hidden_grid.append(" ")
        button[i].grid(row=int(i/rowSize+1), column=int(i%rowSize+1))


def reset():
    global hidden_grid
    global turn
    global player
    global button
    global gamemode
    global aiMode
    global settingButtons

    for i in range(gridSize):
        hidden_grid[i] = " "
        button[i]["text"] = " "
    
    turn = 0
    player = "X"
    gamemode = "Standard"
    
    aiMode = "vs Player"
    settingButtons[1]["text"] = "vs Player" 

def switchPlayer():
    global player
    if(player == "X"):
        player = "O"
    elif(player == "O"):
        player = "X"

def clicked(self, button, number):
    global hidden_grid
    global gamemode
    global player
    global turn
    if hidden_grid[number] != "X" and hidden_grid[number] != "O":
        self["text"] = player
        hidden_grid[number] = player
        turn += 1
        if(gamemode == "Standard"):
            switchPlayer()
        check()
        if(aiMode == "vs AI" and gamemode != "Over"):
            turnAI(hidden_grid, player)
            check()


def settingsClick(self):
    global gamemode
    gamemode = "Standard"
    self["text"] = gamemode

def aiClick(self):
    global aiMode
    global iterationLimit
    global text
    if(aiMode == "vs Player"):
        aiMode = "vs AI"
        text = "vs easy AI"
        iterationLimit = 50*0.99**gridSize
    elif(text == "vs easy AI"):
        text = "vs normal AI"
        iterationLimit = 300*0.99**gridSize
    elif(text == "vs normal AI"):
        text = "vs hard AI"
        iterationLimit = 4000*0.99**gridSize
    elif(text == "vs hard AI"):
        aiMode = "vs Player"
        text = "vs Player"
    self["text"] = text

def playerClick(self):
    switchPlayer()
    self["text"] = "Player: " + str(player)
    
def check():   
    global turn 
    global hidden_grid
    rowCounter = 0
    colCounter = 0
    fDiagCounter = 0
    bDiagCounter  = 0
    rowSize = int(pow(gridSize, 0.5) + 0.99)
    iconList = []
    iconList.append("X")
    iconList.append("O")

    for icon in iconList:
        for i in range(gridSize):
            #Check rows
            if i%rowSize == 0:
                rowCounter = 0
            if(hidden_grid[i] == icon):
                rowCounter = rowCounter + 1
            else:
                rowCounter = 0
            #Check columns & diags
            fDiagRow = []
            bDiagRow = []
            for j in range(winLength):
                #iterators
                a = 0
                b = 0
                c = 0
                d = 0

                #Check columns
                if (i+rowSize*j < gridSize):
                    if(hidden_grid[i+rowSize*j] == icon):
                        colCounter = colCounter + 1
            
                #Check diagonals
                if (i+j+rowSize*j) < gridSize:
                    fDiagRow.append(int((i+j+rowSize*j)/rowSize))
                    if(hidden_grid[i+j+rowSize*j] == icon):
                        fDiagCounter = fDiagCounter + 1
                        while a < len(fDiagRow):
                            while b < len(fDiagRow):
                                if(fDiagRow[a]==fDiagRow[b] and a != b):
                                    fDiagCounter = 0
                                b = b + 1
                            b = 0
                            a = a + 1

                if (-1 < (i+j+(2-j)*rowSize) and (i+j+(2-j)*rowSize) < gridSize):
                    if(hidden_grid[i+j+(2-j)*rowSize] == icon):
                        bDiagRow.append(int((i+j+(2-j)*rowSize)/rowSize))
                        bDiagCounter = bDiagCounter + 1
                        while c < len(bDiagRow):
                            while d < len(bDiagRow):
                                if(bDiagRow[c]==bDiagRow[d] and c != d):
                                    bDiagCounter = 0
                                d = d + 1
                            d = 0
                            c = c + 1

            #Win check
            if(rowCounter > winLength-1):
                win(hidden_grid[i])
                rowCounter = 0 
            elif colCounter > winLength-1:
                win(hidden_grid[i])
            elif fDiagCounter > winLength-1:
                win(hidden_grid[i])
            elif bDiagCounter > winLength-1:
                win(hidden_grid[i+j+(2-j)*rowSize])                
            elif turn > gridSize-1:
                win(" ")
            colCounter = 0 
            fDiagCounter = 0
            bDiagCounter = 0

        

def hide(exception, button):
    for i in range(gridSize):
        if(i != exception):
            button[i]["text"] = " "
        
def unhide():
    global hidden_grid
    for i in range(gridSize):
        if(button[i]["text"] != hidden_grid[i]):
            button[i]["text"] = hidden_grid[i]

def win(player):
    global gamemode
    gamemode = "Over"
    unhide()
    if player == " ":
        messagebox.showinfo("Game finished" ,"Tie game")
        reset()
    else:
        ans = "Game complete " + player + " wins "
        messagebox.showinfo("Congratulations", ans)
        reset()


def turnAI(entryGrid, player):
    predictionGrid = []
    for i in range(gridSize):
        predictionGrid.append(entryGrid[i])

    decision = possibilitySearch(predictionGrid, player)

    global hidden_grid
    global button

    if(decision != -1):
        hidden_grid[decision] = player
        button[decision]["text"] = player
    
    global turn
    turn = turn + 1
    switchPlayer()

def possibilitySearch(predictionGrid, aiPlayer):
    originalPlayer = aiPlayer
    iterationNumber = 0
    global iterationLimit
    aiOptions = []
    tempGrid = []
    for i in range(gridSize):
        aiOptions.append(0)
        tempGrid.append(predictionGrid[i])

    while (iterationNumber < iterationLimit):
        j = 0
        seed = generate_seed()

        while(j < gridSize):
            if tempGrid[seed[j]] == " ":
                tempGrid[seed[j]] = aiPlayer
                aiOptions[seed[0]] += checkPrediction(tempGrid, originalPlayer, j)

                if aiOptions[seed[j]] == 0:
                    aiOptions[seed[j]] = 0.001

                if aiPlayer == "X":
                    aiPlayer = "O"
                elif aiPlayer == "O":
                    aiPlayer = "X"
            elif tempGrid[seed[j]] != " ":
                aiOptions[seed[j]] = -10**10
            j = j + 1
        iterationNumber = iterationNumber + 1
        
        for i in range(gridSize):
            tempGrid[i] = predictionGrid[i]

    highestNumber = -10**11
    finalDecision = 0
    for i in range(gridSize):
        if aiOptions[i] > highestNumber:
            highestNumber = aiOptions[i]
            finalDecision = i
    if(highestNumber == -100):
        finalDecision = -1
    return finalDecision


def checkPrediction(predictionGrid, aiPlayer, turns):
    weight = pow(8 - turns, 2)
    if aiPlayer == "X":
        opPlayer = "O"
    elif aiPlayer == "O":
        opPlayer = "X"

    rowCounter = 0
    colCounter = 0
    fDiagCounter = 0
    bDiagCounter  = 0
    rowSize = int(pow(gridSize, 0.5) + 0.99)
    iconList = []
    iconList.append("X")
    iconList.append("O")

    for icon in iconList:
        for i in range(gridSize):
            #Check rows
            if i%rowSize == 0:
                rowCounter = 0
            if(predictionGrid[i] == icon):
                rowCounter = rowCounter + 1
            else:
                rowCounter = 0
            
            #Check columns & diags
            fDiagRow = []
            bDiagRow = []
            for j in range(winLength):
                a = 0
                b = 0
                c = 0
                d = 0

                if (i+rowSize*j < gridSize):
                    if(predictionGrid[i+rowSize*j] == icon):
                        colCounter = colCounter + 1
            
                if (i+j+rowSize*j) < gridSize:
                    fDiagRow.append(int((i+j+rowSize*j)/rowSize))
                    if(predictionGrid[i+j+rowSize*j] == icon):
                        fDiagCounter = fDiagCounter + 1
                        while a < len(fDiagRow):
                            while b < len(fDiagRow):
                                if(fDiagRow[a]==fDiagRow[b] and a != b):
                                    fDiagCounter = 0
                                b = b + 1
                            b = 0
                            a = a + 1

                if (-1 < (i+j+(2-j)*rowSize) and (i+j+(2-j)*rowSize) < gridSize):
                    if(predictionGrid[i+j+(2-j)*rowSize] == icon):
                        bDiagRow.append(int((i+j+(2-j)*rowSize)/rowSize))
                        bDiagCounter = bDiagCounter + 1
                        while c < len(bDiagRow):
                            while d < len(bDiagRow):
                                if(bDiagRow[c]==bDiagRow[d] and c != d):
                                    bDiagCounter = 0
                                d = d + 1
                            d = 0
                            c = c + 1

            #Win check
            if(rowCounter > winLength-1):
                if(icon==aiPlayer):
                    return 1*weight
                if(icon==opPlayer):
                    return -1*weight
                rowCounter = 0 
            elif colCounter > winLength-1:
                if(icon==aiPlayer):
                    return 1*weight
                if(icon==opPlayer):
                    return -1*weight
            elif fDiagCounter > winLength-1:
                if(icon==aiPlayer):
                    return 1*weight
                if(icon==opPlayer):
                    return -1*weight
            elif bDiagCounter > winLength-1:
                if(icon==aiPlayer):
                    return 1*weight
                if(icon==opPlayer):
                    return -1*weight
           
            colCounter = 0 
            fDiagCounter = 0
            bDiagCounter = 0
    return 0


#main function
def main():
    begin()    
    window.mainloop()


if __name__ == "__main__":
    main()

global numHeighest
global numLowest
global lastGuessed
global tryAgain
tryAgain = True
trys = 0

def settings():
    global numHeighest
    global numLowest
    global lastGuessed
    while True:
        lowest = input("What is the lowest possible Number?")
        heighest = input("What is the highest possible Number?")
        if int(lowest) >= int(heighest):
            print("This isn't possible, try again")
        else:
            numLowest = lowest
            numHeighest = heighest
            lastGuessed = numLowest
            break

def askNumber():
    input("Please guess a number between " + str(numLowest)
            + " and " + str(numHeighest) + ".")

def guess(bigger):
    global trys
    global numHeighest
    global numLowest
    global lastGuessed
    global tryAgain
    trys+=1

    calcWith = 0
    if bool(bigger):
        if int(numLowest) < int(lastGuessed):
            numLowest = lastGuessed
        calcWith = int(numHeighest) - (int(numHeighest) - int(lastGuessed)) / 2
    else:
        if int(numHeighest) > int(lastGuessed):
            numHeighest = lastGuessed
        calcWith = int(lastGuessed) - (int(lastGuessed) - int(numLowest))/ 2
    lastGuessed = int(calcWith)

    result = input("Is your Number = " + str(int(calcWith)) + "?\n"
                    + "2 = bigger than, 1 = smaller than, 0 = You got it")
    if int(result) == 2:
        guess(True)
    elif int(result) == 0:
        print("Booyah, it took me " + str(trys) + " trys!")
        again = input("Play again? 1 = yes, 2 = no")
        if int(again) == 1:
            tryAgain = True
        else:
            tryAgain = False
    else:
        guess(False)

while bool(tryAgain):
    settings()
    askNumber()
    guess(True)
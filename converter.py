#!/usr/bin/env python

import sys
import datetime
import time

def main(argv):
    inputFileName = argv[0]
    outputFileName = argv[1]
    limitSmallBet = int(argv[2])
    limitBigBet = int(argv[3])

    if len(argv) < 5:
        limitSmallBlind = limitSmallBet/2;
    else:
        limitSmallBlind = int(argv[4])

    if len(argv) < 6:
        limitBigBlind = limitSmallBet;
    else:
        limitBigBlind = int(argv[5])

    count = 1;
    with open(inputFileName,'r') as inputFile:
        with open(outputFileName, 'w') as outputFile:
            for line in inputFile:
                lineChomp = line.rstrip('\n')
                if lineChomp[0] == '#':
                    continue

                outputHistory = processLine(lineChomp,limitSmallBet,limitBigBet,limitSmallBlind,limitBigBlind)
                if count == 10000:
                    break
                count = count + 1

def processLine(inputHistory,limitSmallBet,limitBigBet,limitSmallBlind,limitBigBlind):
    iHColonSplit = inputHistory.split(':')

    if iHColonSplit[0] != 'STATE':
        return ""

    if len(iHColonSplit) != 6:
        print inputHistory
        raise Exception("Incorrect number of fields")

    stateNumber = iHColonSplit[1]
    actions = iHColonSplit[2]
    cards = iHColonSplit[3]
    results = iHColonSplit[4]
    players = iHColonSplit[5]

    if not RepresentsInt(stateNumber):
        raise Exception("Incorrect hand number format")

    actionsByRound = actions.split('/')

    if len(actionsByRound) < 1 or len(actionsByRound) > 4:
        raise Exception("Invalid number of action rounds")

    cardsSplit = cards.split('|')
    holeCards = []
    holeCards.append(cardsSplit[0])
    holeCards.append(cardsSplit[1])
    cardsLastSplit = cardsSplit[2].split('/')
    holeCards.append(cardsLastSplit[0])
    boardCards = cardsLastSplit[1:]

    if len(actionsByRound) != len(boardCards) + 1:
        raise Exception("Number of action rounds doesn't match number of board card")

    resultsSplit = results.split('|')
    playersSplit = players.split('|')

    numPlayers = len(playersSplit)

    if len(resultsSplit) != numPlayers:
        raise Exception("Number of results and number of players don't match")

    #dateNow = datetime.date.today()
    dateNow = datetime.date.fromtimestamp(time.time())

    outputString = ""
    outputString += "PokerStars Hand #"
    outputString += str(stateNumber)
    outputString += ": Hold'em Fixed Limit ($" + str(limitSmallBet) +  ".00/$" + str(limitBigBet) +  ".00) - "
    outputString += dateNow.strftime('%Y/%m/%d')
    outputString += " "
    outputString += dateNow.strftime('%H:%M:%S')
    outputString += "\n"

    buttonPosition = numPlayers-1
    sbPosition = (buttonPosition + 1) % numPlayers
    bbPosition = (sbPosition + 1) % numPlayers
    utgPosition = (bbPosition + 1) % numPlayers

    outputString += "Table '#"
    outputString += str(10782437)
    outputString += "' "
    outputString += "6 - max "
    outputString += "Seat #" + str(buttonPosition+1) + " is the button"
    outputString += "\n"

    # seats and chips
    for seat in range(numPlayers):
        outputString += "Seat " + str(seat+1) + ": "
        outputString += playersSplit[seat]
        outputString += " ($10000 in chips)\n"

    # blinds
    outputString += playersSplit[sbPosition] + ": posts small blind $" + str(limitSmallBlind) + "\n"
    outputString += playersSplit[bbPosition] + ": posts big blind $" + str(limitBigBlind) + "\n"

    outputString += "*** HOLE CARDS ***\n"

    for seat in range(numPlayers):
        outputString += "Dealt to " + playersSplit[seat] + " ["
        outputString += holeCards[seat][0:2] + " " + holeCards[seat][2:4] + "]\n"

    # now run through the hand actions and append the string to be written
    playerInHand = [True] * numPlayers

    # action rounds
    for round in range(len(actionsByRound)):
        playerContributed = [0] * numPlayers
        if round == 0:
            startingPlayer = utgPosition
            currentBet = limitSmallBet
            playerContributed[sbPosition] += limitSmallBlind
            playerContributed[bbPosition] += limitBigBlind
        else:
            startingPlayer = sbPosition
            currentBet = 0
        if round == 0 or round == 1: # preflop or flop
            currentBetIncrement = limitSmallBet
        else:
            currentBetIncrement = limitBigBet
        if round == 1:
            outputString += "*** FLOP *** ["
            outputString += boardCards[0][0:2] + " " + boardCards[0][2:4] + " " + boardCards[0][4:6] + "]\n"
        if round == 2:
            outputString += "*** TURN *** ["
            outputString += boardCards[0][0:2] + " " + boardCards[0][2:4] + " " + boardCards[0][4:6] + "]"
            outputString += " [" + boardCards[1][0:2] + "]\n"
        if round == 3:
            outputString += "*** RIVER *** ["
            outputString += boardCards[0][0:2] + " " + boardCards[0][2:4] + " " + boardCards[0][4:6] + "]"
            outputString += " [" + boardCards[1][0:2] + "]"
            outputString += " [" + boardCards[2][0:2] + "]\n"

        actionsThisRound = actionsByRound[round]
        currentPlayer = startingPlayer
        for actionIndex in range(len(actionsThisRound)):
            action = actionsThisRound[actionIndex]

            # determine which player this corresponds to (get next available player)
            while not playerInHand[currentPlayer]:
                currentPlayer = (currentPlayer + 1) % numPlayers

            amountToCall = currentBet - playerContributed[currentPlayer]
            # execute action, record state, and write string
            if action == 'f':
                playerInHand[currentPlayer] = False
                outputString += playersSplit[currentPlayer] + ": folds\n"
            elif action == 'c': # this is either check or call
                if amountToCall == 0: # check
                    outputString += playersSplit[currentPlayer] + ": checks\n"
                else: # call
                    playerContributed[currentPlayer] += amountToCall
                    outputString += playersSplit[currentPlayer] + ": calls $" + str(amountToCall) + "\n"
            elif action == 'r': # this is either bet or raise
                playerContributed[currentPlayer] += amountToCall + currentBetIncrement
                currentBet += currentBetIncrement
                if amountToCall > 0 or round == 0: # normal raise or option raise
                    outputString += playersSplit[currentPlayer] + ": raises $" + str(amountToCall + currentBetIncrement)
                    outputString += " to $" + str(currentBet) + "\n"
                else: # bet
                    outputString += playersSplit[currentPlayer] + ": bets $" + str(currentBetIncrement) + "\n"

            # move to next player
            currentPlayer = (currentPlayer + 1) % numPlayers

    playersLeft = sum(playerInHand)

    if playersLeft >= 2:
        outputString += "*** SHOW DOWN ***\n"
        for seat in range(numPlayers):
            if playerInHand[seat]:
                outputString += playersSplit[seat] + ": shows ["
                outputString += holeCards[seat][0:2] + " " + holeCards[seat][2:4] + "]\n"

    # was working on this code
    #pot = 0
    #for r in range(len(resultsSplit)):
    #    result = int(resultsSplit[r])
    #    if result > 0:
    #        pot += result
    #        outputString +=
#
    outputString += "*** SUMMARY ***\n"

    print outputString


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])



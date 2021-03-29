# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 16:44:45 2021
@author: mbust
"""

from HanabiClasses import *
from ai_new import Solver
from inputNumber import inputNumber
from displayMenu import displayMenu
from BeliefSpace import BeliefSpace
import random

class CustomError(Exception):
    pass

def startGame():
    
    #random.seed(114)
    #Player
    order1 = 1
    order2 = 2
    
    #Deck
    distributionOptionsList = [[1,2,3,4,5],[1,2,2,3,3,3,4,4,4,4,5,5,5,5,5],[1,1,1,2,2,3,3,4,4,5]]
    distributionOptionsStr = [str(x) for x in distributionOptionsList]
    
    print("How do you want to play the game?")
    choicePvA = ["Player & AI (test playing with the AI)","Player & Player (in case you would like to test the game engine independently of the AI)"]
    PvAOption = displayMenu(choicePvA)
    
    if PvAOption==1:
        PvA=True
    elif PvAOption==2:
        PvA=False
    
    
    #default set up?
    print("Do you want to use the default game configuration?")
    choiceSetUp = ["Default set-up","Manual set-up"]
    defaultOption = displayMenu(choiceSetUp)
    
    if defaultOption==1:
        default=True
    elif defaultOption==2:
        default=False

    if default:
        name1 = input("Name of first player: ")
        if PvA:
            name2 = "AI"
        else:
            name2 = input("Name of second player: ")
        numberOfCards = 4
        numberOfColors = 2
        cardsDistribution = distributionOptionsList[2]
        maxHTokens = 8
        maxPTokens = 3
        green = ';'.join([str(1), str(32), str(28)])
        print("")
        print('\x1b[%smDefault configurations: \x1b[0m' % (green))
        print("\x1b[%sm-4 cards in hand\x1b[0m" % (green))
        print("\x1b[%sm-2 colors in the game\x1b[0m" % (green))
        print("\x1b[%sm-cards in the deck: three 1s, two 2s, 3s ,4s and one 5 (for each color)\x1b[0m" % (green))
        print("\x1b[%sm-total number of cards in the deck: 20\x1b[0m" % (green))
        print("\x1b[%sm-Max number of Hint tokens: 8\x1b[0m" % (green))
        print("\x1b[%sm-Max number of Penalty tokens: 3\x1b[0m" % (green))
        #finalMessage = ('\x1b[%sm %s \x1b[0m' % (color, message))
        
    else:
        name1 = input("Name of first player: ")
        if PvA:
            name2 = "AI"
        else:
            name2 = input("Name of second player: ")
        numberOfCards = int(input("How many cards per player? "))
        numberOfColors = int(input("How many colors? "))
        print("Choose card distribution.")
        choiceDistribution = displayMenu(distributionOptionsStr)
        cardsDistribution = distributionOptionsList[int(choiceDistribution)-1]
        maxHTokens = int(input("Choose max number of Hint Tokens: "))
        maxPTokens = int(input("Choose max number of Penalty Tokens: "))
    
    #create Player objects
    Player1 = Player(name1,order1,numberOfCards)
    Player2 = Player(name2,order2,numberOfCards)
    
    #create Deck object
    deck = Deck(numberOfColors,cardsDistribution)
            
    #create Played Pile object
    playedPile = PlayedPile(numberOfColors)
    
    #create Discard Pile object
    discardPile = DiscardPile([])
    
    #create Tokens objects
    hintTokens = HintTokens(maxHTokens, maxHTokens)
    penaltyTokens = PenaltyTokens(0, maxPTokens)
    
    #create final variables for state
    turn = 1
    parent = []
    
    #create a list of states and store the starting state
    states = []
    Player1.drawNewHand(deck)
    Player2.drawNewHand(deck)
    initialState = State(Player1, Player2, deck, playedPile, discardPile, hintTokens, penaltyTokens, turn, parent,PvA)
    states.append(initialState)
    
    return states

def chooseCardFromHand(activePlayer, otherPlayer, action):
    
    if action == "hint":
        print("{}, what card do you want to {}?".format(activePlayer.name, action))
        cardOptions = []
        for i in range(len(otherPlayer.cards)):
            word2 = str(otherPlayer.cards[i].number)
            word1 = otherPlayer.cards[i].color
            
            if otherPlayer.cards[i].colorHinted:
                word1 = word1+"*"
            if otherPlayer.cards[i].numberHinted:
                word2 = word2+"#"
                
                
            cardInHand = ("Position of the card in hand: {}, color: {}, number: {}".format(i+1, word1, word2))
            cardOptions.append(cardInHand)
        cardOptions.append("Go Back")
        choiceCard = displayMenu(cardOptions)
        return (choiceCard - 1)
        
        
    else:
        print("{}, what card do you want to {}?".format(activePlayer.name, action))
        cardOptions = []
        for i in range(len(activePlayer.cards)):
            word1 = "?"
            word2 = "?"
            if activePlayer.cards[i].colorHinted:
                word1 = activePlayer.cards[i].color
            if activePlayer.cards[i].numberHinted:
                word2 = str(activePlayer.cards[i].number)
            cardInHand = ("Position of the card in hand: {}, color: {}, number: {}".format(i+1, word1, word2))
            cardOptions.append(cardInHand)
        cardOptions.append("Go Back")
        choiceCard = displayMenu(cardOptions)
        return (choiceCard - 1)

def chooseHintType(activePlayer, otherPlayer, cardChoice):
    
    cardHinted = otherPlayer.cards[cardChoice]
    '''
    print("Here are all cards in that player's hand:")
    otherPlayer.storeInfo()
    print("")
    print("And here is the card you chose:")
    cardHinted.sayInfo()
    '''
    print("")
    print("{}, what hint would you like to give? (All cards that share that attribute will also be hinted)".format(activePlayer.name))
    hintOptions = ["color"+" ({})".format(cardHinted.color), "number"+" ({})".format(cardHinted.number), "Go Back"]
    choiceHint = displayMenu(hintOptions)
    
    if choiceHint == 1:
        hintType = "color"
        hint = cardHinted.color
    elif choiceHint == 2:
        hintType = "number" 
        hint = cardHinted.number
    elif choiceHint == 3:
        hintType = "Go Back"
        hint = None
    
    return hintType, hint
    
    

def playRound(states, action, parameter):
    if isinstance(states,list):
        initialState = states[-1]
    else:
        initialState = states
    
    if initialState.turn == 1:
        activePlayer = initialState.Player1
        otherPlayer = initialState.Player2
        human = True
    elif initialState.turn == 2:
        activePlayer = initialState.Player2
        otherPlayer = initialState.Player1
        if initialState.PvA:
            human = False
        else:
            human = True
        
    
    actionOptions = ["Play a card", "Give a hint", "Discard a card","Quit"]
    
    #ask for user input if human 
    #get input from computer if AI
    


    while True:
        
        #----------------------AI: disable human = true, if you want to test with AI
        #human = True
        if human:
            print("{}'s turn, choose an action: ".format(activePlayer.name))
            choiceAction = displayMenu(actionOptions)
        else:
            solver = Solver(2, 4)
            """
            print("Turn: ", states[-1].turn)
            print("Human: ", states[-1].human)
            print("Played Pile Red: ", states[-1].playedPile.convertList(0))
            print("Played Pile Blue: ", states[-1].playedPile.convertList(1))
            print("Length of Hand: ", len(initialState.AI.cards))
            """
            
            space = BeliefSpace(states[-1],len(initialState.AI.cards))
            choiceAction,parameter = solver.evaluate(space.states,states[-1], False)
            #print(choiceAction,parameter)
        #PLAY
        if choiceAction == 1:
            if human:
                cardChoice = int(chooseCardFromHand(activePlayer,None, "play"))
            else:
                cardChoice = parameter
            if cardChoice == len(activePlayer.cards):
                newState = None
            else:
                newState = Action.play(initialState,cardChoice)
                break
        #HINT
        elif choiceAction == 2:
            if human:
                cardChoice = int(chooseCardFromHand(activePlayer, otherPlayer, "hint"))
                if cardChoice == len(activePlayer.cards):
                    newState = None
                else:
                    hintType, hint = chooseHintType(activePlayer, otherPlayer, cardChoice)
                    if hintType == "Go Back":
                        newState = None
                    else:
                        newState = Action.hint(initialState,hintType, hint)
                        break
            else:
                hintType, hint = parameter
                newState = Action.hint(initialState,hintType, hint)
                break
        
        #DISCARD
        elif choiceAction == 3:
            
            if human:
                cardChoice = int(chooseCardFromHand(activePlayer, None, "discard"))
            else:
                cardChoice = parameter
            
            if cardChoice == len(activePlayer.cards):
                newState = None
            else:
                newState = Action.discard(initialState,cardChoice)
                break
            
        #QUIT
        elif choiceAction == 4:
            
            raise CustomError("Program will terminate")
            break
        
            
    if newState == None:
        print("Choose another option!")
        newState = initialState

    if isinstance(states,list):
        states.append(newState)
    else:
        states = newState
            
    return states
        
    
def playGame(states):
    if states == None:
        states = startGame()
    
        
    
    while True:
        if states[-1].human:
            states[-1].display()
        else:
            print("")
            print("*********************")
            print("    AI Playing        ")
            print("*********************")
        try:
            #-----------------------------AI: action and parameter must be defined when the AI is playing
            action = None 
            parameter = None
            states = playRound(states, action, parameter)
            print("Round ended.")
            
        except(CustomError):
            print("User has chosen to Quit.")
            print("Program terminating...")
            break
        
        gameEnd, message = states[-1].checkGoal()
        if gameEnd:
            print("")
            print("/\/\/\/\/\/\/\/\/\/\\/\/\/\/\/\/\/\/\/\/\/")
            print(message)
            print("/\/\/\/\/\/\/\/\/\/\\/\/\/\/\/\/\/\/\/\/\/")
            break
            
        
        
    return states
if __name__ == "__main__":
    playGame(None)
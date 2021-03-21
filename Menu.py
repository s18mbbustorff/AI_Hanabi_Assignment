# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 16:44:45 2021

@author: mbust
"""

from Main import *
from inputNumber import inputNumber
from displayMenu import displayMenu

class CustomError(Exception):
    pass

def startGame():
    
    #create initial state
    
    #create Player objects
    name1 = input("Name of first player: ")
    name2 = input("Name of second player: ")
    order1 = 1
    order2 = 2
    numberOfCards = int(input("How many cards per player? "))
    Player1 = Player(name1,order1,numberOfCards)
    Player2 = Player(name2,order2,numberOfCards)
    
    #create Deck object
    numberOfColors = int(input("How many colors? "))
    distributionOptionsList = [[1,2,3,4,5],[1,2,2,3,3,3,4,4,4,4,5,5,5,5,5],[1,1,1,2,2,3,3,4,4,5]]
    distributionOptionsStr = [str(x) for x in distributionOptionsList]
    print("Choose card distribution.")
    choiceDistribution = displayMenu(distributionOptionsStr)
    cardsDistribution = distributionOptionsList[int(choiceDistribution)-1]
    deck = Deck(numberOfColors,cardsDistribution)
            
    #create Played Pile object
    playedPile = PlayedPile(numberOfColors)
    
    #create Discard Pile object
    discardPile = DiscardPile([])
    
    #create Tokens objects
    maxTokens = int(input("Choose max number of Hint Tokens: "))
    hintTokens = HintTokens(maxTokens, maxTokens)
    
    maxTokens = int(input("Choose max number of Penalty Tokens: "))
    penaltyTokens = PenaltyTokens(0, maxTokens)
    
    #create final variables for state
    turn = 1
    parent = []
    
    #create a list of states and store the starting state
    states = []
    Player1.drawNewHand(deck)
    Player2.drawNewHand(deck)
    initialState = State(Player1, Player2, deck, playedPile, discardPile, hintTokens, penaltyTokens, turn, parent)
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
                word2 = word2+"*"
                
                
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
    print("Here are all cards in that player's hand:")
    otherPlayer.storeInfo()
    print("")
    print("And here is the card you chose:")
    cardHinted.sayInfo()
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
        human = False
    elif initialState.turn == 2:
        activePlayer = initialState.Player2
        otherPlayer = initialState.Player1
        human = True
        
    
    actionOptions = ["Play a card", "Give a hint", "Discard a card","Quit"]
    
    #ask for user input if human 
    #get input from computer if AI
    


    while True:
        #----------------------AI: disable human = true, if you want to test with AI
        human = True
        if human:
            print("{}, (Player{}), choose an option: ".format(activePlayer.name, activePlayer.order))
            choiceAction = displayMenu(actionOptions)
        else:
            choiceAction = action
    
    
        #PLAY
        if choiceAction == 1:
            if human:
                cardChoice = int(chooseCardFromHand(activePlayer,None, "play"))
            else:
                cardChoice = parameter+1
            if cardChoice == 4:
                newState = None
            else:
                newState = Action.play(initialState,cardChoice)
                break
        #HINT
        elif choiceAction == 2:
            if human:
                cardChoice = int(chooseCardFromHand(activePlayer, otherPlayer, "hint"))
                if cardChoice == 4:
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
                cardChoice = parameter+1
            
            if cardChoice == 4:
                newState = None
            else:
                newState = Action.discard(initialState,cardChoice)
                break
            
        #QUIT
        elif choiceAction == 4:
            print("Quitting")
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
        states[-1].display()
        try:
            #-----------------------------AI: action and parameter must be defined when the AI is playing
            action = None 
            parameter = None
            states = playRound(states, action, parameter)
            print("Round ended.")
            
        except(CustomError):
            print("error")
            break
        
    return states
        
        
        
    
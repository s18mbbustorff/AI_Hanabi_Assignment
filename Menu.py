# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 16:44:45 2021

@author: mbust
"""

from Main import *
from inputNumber import inputNumber
from displayMenu import displayMenu


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
    maxTokens = input("Choose max number of Hint Tokens: ")
    hintTokens = HintTokens(maxTokens, maxTokens)
    
    maxTokens = input("Choose max number of Penalty Tokens: ")
    penaltyTokens = PenaltyTokens(maxTokens, maxTokens)
    
    #create final variables for state
    turn = 1
    parent = []
    
    #create a list of states and store the starting state
    states = []
    initialState = State(Player1, Player2, deck, playedPile, discardPile, hintTokens, penaltyTokens, turn, parent)
    states.append(initialState)
    
    return states

def playRound(initialState):
    if initialState.turn == 1:
        activePlayer = initialState.Player1
        nonActivePlayer = initialState.Player2
    elif initialState.turn == 2:
        activePlayer = initialState.Player2
        nonActivePlayer = initialState.Player1
        
    print("{}, (Player{}), choose an option: ".format(activePlayer.name, activePlayer.order))
    
    
        
    
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 19:30:29 2021

@author: mbust
"""

from Main import *
    
    
def firstTest():
    numberOfColors = 2
    cardsDistribution = [1,1,1,2,2,3,3,4,4,5]
    newDeck = Deck(numberOfColors,cardsDistribution)
    
    numberOfColors = 4
    Player1 = Player("Miguel", 1, numberOfColors)
    Player1.drawNewHand(newDeck)
    Player2 = Player("Sara", 2, numberOfColors)
    Player2.drawNewHand(newDeck)
    
    playedPile = PlayedPile(numberOfColors)
    
    #create Discard Pile object
    discardPile = DiscardPile([])
    
    #create Tokens objects
    maxTokens = 8
    hintTokens = HintTokens(maxTokens, maxTokens)
    
    maxTokens = 3
    penaltyTokens = PenaltyTokens(maxTokens, maxTokens)
    
    #create final variables for state
    turn = 1
    parent = []
    
    states = []
    initialState = State(Player1, Player2, newDeck, playedPile, discardPile, hintTokens, penaltyTokens, turn, parent)
    states.append(initialState)
    
    return states
    
print("Running test 1:")

states = firstTest()
state1 = states[0]
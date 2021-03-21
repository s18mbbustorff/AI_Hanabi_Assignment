# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 19:30:29 2021

@author: mbust
"""

from itertools import combinations
from Main import *
    
    
def firstTest():
    numberOfColors = 2
    cardsDistribution = [1,1,1,2,2,3,3,4,4,5]
    newDeck = Deck(numberOfColors,cardsDistribution)
    
    numberOfCards = 4
    Player1 = Player("Miguel", 1, numberOfCards = 4)
    Player1.drawNewHand(newDeck)
    Player2 = Player("AI", 2, numberOfCards = 4)
    Player2.drawNewHand(newDeck)
    
    playedPile = PlayedPile(numberOfColors)
    
    #create Discard Pile object
    discardPile = DiscardPile([])
    
    #create Tokens objects
    maxTokens = 8
    hintTokens = HintTokens(maxTokens, maxTokens)
    
    maxTokens = 3
    penaltyTokens = PenaltyTokens(0, maxTokens)
    
    #create final variables for state
    turn = 2
    parent = []
    
    states = []
    initialState = State(Player1, Player2, newDeck, playedPile, discardPile, hintTokens, penaltyTokens, turn, parent)
    states.append(initialState)
    
    return states
"""  
print("Running test 1:")
states = firstTest()
state1 = states[0]
a = state1.Player2.storeInfo() + state1.deck.storeInfo()
print(len(a))
comb = combinations(a,4)
print(len(list(comb)))
"""

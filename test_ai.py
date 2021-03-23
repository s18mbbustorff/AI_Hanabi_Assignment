#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 22:27:53 2021

@author: kuba
"""

import random
from ai_new import Solver, State_search
from Main import Deck, PlayedPile, HintTokens, PenaltyTokens, DiscardPile, Player
from BeliefSpace import BeliefSpace
    
def firstTest():
    numberOfColors = 2
    cardsDistribution = [1,1,1,2,2,3,3,4,4,5]
    newDeck = Deck(numberOfColors,cardsDistribution)
    
    numberOfCards = 4
    Player1 = Player("Miguel", 1, numberOfCards)
    Player1.drawNewHand(newDeck)
    Player2 = Player("AI", 2, numberOfCards)
    Player2.drawNewHand(newDeck)
    
    playedPile = PlayedPile(numberOfColors)
    
    #create Discard Pile object
    discardPile = DiscardPile([])
    
    #create Tokens objects
    maxTokens = 9
    hintTokens = HintTokens(maxTokens-1, maxTokens)
    
    maxTokens = 3
    penaltyTokens = PenaltyTokens(0, maxTokens)
    
    #create final variables for state
    turn = 2
    parent = []
    
    states = []
    initialState = State_search(Player1, Player2, newDeck, playedPile, discardPile, hintTokens, penaltyTokens, turn, parent)
    states.append(initialState)
    
    return states
    

if __name__ == "__main__":
    
    random.seed(114)
    states = firstTest()
    state = states[0]
    state.Player.cards[2].colorHinted = True
    state.Player.cards[2].numberHinted = True
    #state.AI.cards[2].numberHinted = True
    space = BeliefSpace(state,4)
    print("Starting state: PLAYER ", state.Player.storeInfo())
    print("Starting state: AI ", state.AI.storeInfo())
    solver = Solver(2, 4)
    #print(solver.evaluate(space.states))
    
    terminal, actions, top_action = solver.evaluate(space.states, True)
    #print("Terminal info: ", terminal)
    for i, (action,value) in enumerate(zip(actions, terminal)):
        print(str(i) + ". Action: ", action, "    Value: ", str(int(value)))
    print("Starting state: PLAYER ", state.Player.storeInfo())
    print("Starting state: AI ", state.AI.storeInfo())
    print("DO: ", top_action)
    
    
    
    
    
    
    
    
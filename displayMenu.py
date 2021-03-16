def displayMenu(options): 
    '''
    DISPLAYMENU Displays a menu of options, ask the user to choose an item 
    and returns the number of the menu item chosen. 
    
    * Input arguments: Menu options (array of strings) 
    
    * Output arguments: Chosen option (integer) 
    
    * Author: Mikkel N. Schmidt, mnsc@dtu.dk, 2015
    '''
    
    import numpy as np
    from inputNumber import inputNumber
    
    # Display menu options 
    for i in range(len(options)): 
        print("{:d}. {:s}".format(i+1, options[i]))
    # Get a valid menu choice 
    choice = 0 
    while not(np.any(choice == np.arange(len(options))+1)): 
        choice = inputNumber("Please choose a menu item: ")
    return choice

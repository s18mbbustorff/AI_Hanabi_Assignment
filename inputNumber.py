def inputNumber(prompt):
    while True:
        try:
            number = float(input(prompt))
            break
        except ValueError:
            print('Please, provide a correct input value')
            pass
    return number
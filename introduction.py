def introduction():
    print('')
    with open('intro', 'r') as intro:
        print(intro.readline().strip())
        for line in intro:
            t1 = perf_counter()
            t2 = t1 
            while t2 - t1 < 2:
                t2 = perf_counter()
            print(line, end='')    
    choice = 'No'
    while choice.lower()[0] != 'y':
        name = input(' Can you at least tell me your name before I go? ')
        choice = input("""*{}*\nAre you sure? (y/n): """.format(name))

    return name

class SetUp:
    def __init__(self):
        com = input("print 'help' to help\nWant to setup Game? ")
        while com:
            if 'help' in com:
                print("'check' to show data about game\n\
'edit' to edit list of players\n\
'end' to complete setup the game\n\
You also can just press <<Enter>> to complete setup")
            elif 'end' in com:
                print("Setup completed")
                return
            elif 'check' in com:
                with open('note.txt', 'r') as f:
                    for line in f.readlines():
                        print(line, end='')
            elif 'edit' in com:
                self.edit()
            com = input()
    
    def edit(self):
        com = input("---Edit LOP mod---\n\
    print 'help' to help\n    ")
        lop = []
        with open('note.txt', 'r') as f:
            rl = f.readlines()
            num = rl[0]
            for line in rl[1:]:
                lop.append(line[:-1])
        while com:
            if 'help' in com:
                print("\tUse this form to edit list of players (futher LOP):\n\
    '[comand]/[Nick]'\n\
    For example:'pop/Alex' - \
this comand remove Alex from LOP\n\
    available commands:\n\
        'add' to add player(s) to LOP\n\
        'pop' to remove player(s) from LOP\n\
        'clear' to remove ALL players from LOP\n\
        'new' to create new LOP futher you must to list all players\n\
    You cannot add already exist players\n\
    You also can use all command on a lot of players\n\
    For this just list all players, splitting '/'-char like this:\n\
    'Ann/Sam/Cile/Jim'\n\
    print 'end' or press <<Enter>> to complete edit LOP")
            elif 'end' in com:
                print("Edit completed")
                return
            else:
                players = list(map(str, com.split('/')))[1:]
                if 'add' in com:
                    lop = list(set(lop) | (set(players) - set(lop)))
                elif 'pop' in com:
                    lop = list(set(lop) - set(players))
                elif 'clear' in com:
                    lop = []
                elif 'new' in com:
                    lop = players
            with open('note.txt', 'w+') as f:
                f.write(num)
                for p in lop:
                    f.write(p + '\n')    
            com = input('    ')

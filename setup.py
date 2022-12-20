class SetUp:
    def __init__(self):
        y = '\033[1;33;40m'
        n = '\033[0;37;40m'
        g = '\033[1;32;40m'
        com = input("print 'help' to "+y+"help"+n+"\nWant to setup Game? ")
        while com:
            if 'help' in com:
                print(y+"'check' to show data about game\n\
'edit' to edit list of players\n\
'end' to complete setup the game\n\
You also can just press <<Enter>> to complete setup"+n)
            elif 'end' in com:
                print("Setup completed")
                return
            elif 'check' in com:
                with open('note.txt', 'r') as f:
                    for line in f.readlines():
                        print(g+line, end=n)
            elif 'edit' in com:
                self.edit()
            com = input()
    
    def edit(self):
        y = '\033[1;33;40m'
        n = '\033[0;37;40m'
        com = input("---Edit LOP mod---\n\
    print 'help' to "+y+"help"+n+"\n    ")
        lop = []
        with open('note.txt', 'r') as f:
            rl = f.readlines()
            num = rl[0]
            for line in rl[1:]:
                lop.append(line[:-1])
        while com:
            com = list(map(str, com.split('/')))
            com, players = com[0], com[1:]
            if 'help' in com:
                print(y+"    Use this form to edit list of players (futher LOP):\n\
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
    print 'end' or press <<Enter>> to complete edit LOP"+n)
            elif 'end' in com:
                print("Edit completed")
                return
            else:
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

from maf import Maf
from setup import SetUp

SetUp()
Game = input("Press <<Enter>> to start ")
if not Game:
    Game = Maf()
    Game.start()
    Game.end()  

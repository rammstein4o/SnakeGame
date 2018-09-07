import random
from lib.CoordList import CoordList
from lib.Configurable import Configurable

class Apples(Configurable, CoordList):
    def __init__(self, config, grid, *args, **kwargs):
        Configurable.__init__(self, config, *args, **kwargs)
        CoordList.__init__(self, grid, *args, **kwargs)

    def setSnake(self, snake):
        self.snake = snake
    
    def initApples(self):
        while self.len() < self.initApplesCount:
            self.addApple()
    
    def addApple(self):
        while True:
            x, y = random.randint(0, self.fieldWidth - 1), random.randint(0, self.fieldHeight - 1)
            if not self.snake.exists((x, y)) and not self.exists((x, y)):
                fld = self.getField((x, y))
                fld.setApple()
                self.append((x, y))
                break

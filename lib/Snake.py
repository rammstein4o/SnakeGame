import math
import random
from lib.CoordList import CoordList
from lib.Configurable import Configurable

class Snake(Configurable, CoordList):
    def __init__(self, config, grid, *args, **kwargs):
        Configurable.__init__(self, config, *args, **kwargs)
        CoordList.__init__(self, grid, *args, **kwargs)

    def initSnake(self):
        # Add snake head
        borderLine = math.ceil(self.initSnakeSize / 2)
        x = random.randint(borderLine, (self.fieldWidth - (borderLine + 1)))
        y = random.randint(borderLine, (self.fieldHeight - (borderLine + 1)))
        fld = self.getField((x, y))
        fld.setHead()
        self.append((x, y))
        
        if x <= ((self.fieldWidth - 1) / 2):
            initialDirectionX = 1
        else:
            initialDirectionX = -1
        
        if y <= ((self.fieldHeight - 1) / 2):
            initialDirectionY = 1
        else:
            initialDirectionY = -1
        
        # Add snake body
        while self.len() < self.initSnakeSize:
            if initialDirectionX > 0:
                x += 1
                if x > (self.fieldWidth - 1):
                    x = 0
                    if initialDirectionY > 0:
                        y += 1
                    else:
                        y -= 1
            else:
                x -= 1
                if x < 0:
                    x = 0
                    if initialDirectionY > 0:
                        y += 1
                    else:
                        y -= 1

            fld = self.getField((x, y))
            fld.setSnake()
            self.append((x, y))

import random
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPalette
from lib.Field import Field

class UserInterface(QMainWindow):
    MOVE_UP = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3
    MOVE_LEFT = 4
    
    def __init__(self, config):
        super(UserInterface, self).__init__()
        self.config = config
        self.fieldWidth = int(self.config['default']['fieldWidth'])
        self.fieldHeight = int(self.config['default']['fieldHeight'])
        self.initApplesCount = int(self.config['default']['initApplesCount'])
        self.initSnakeSize = int(self.config['default']['initSnakeSize'])
        self.growSnakeSegments = int(self.config['default']['growSnakeSegments'])
        self.addApplesOnTimeout = int(self.config['default']['addApplesOnTimeout'])
        self.appleTimeout = int(self.config['default']['appleTimeout'])
        self.snakeSpeed = float(self.config['default']['snakeSpeed'])
        self.resolution = int(self.config['ui']['resolution'])
        self.spacing = int(self.config['ui']['spacing'])
        self.fontSize = int(self.config['ui']['fontSize'])
        self.fontWeight = int(self.config['ui']['fontWeight'])
        
        self.snakeTimer = QTimer()
        self.snakeTimer.timeout.connect(self.moveSnake)
        self.statusbar = self.statusBar()

    def initFields(self):
        for x in range(0, self.fieldWidth):
            for y in range(0, self.fieldHeight):
                fld = Field(self.config, x, y)
                self.grid.addWidget(fld, y, x)

    def reset(self):
        self.direction = None
        self.currentScore = 0
        self.movesToGrow = 0
        self.snake = []
        self.apples = []
        self.isStarted = False
        
        # Reset all fields
        for x in range(0, self.fieldWidth):
            for y in range(0, self.fieldHeight):
                fld = self.grid.itemAtPosition(y, x).widget()
                fld.reset()
        
        # Add snake head
        borderLine = math.ceil(self.initSnakeSize / 2)
        x = random.randint(borderLine, (self.fieldWidth - (borderLine + 1)))
        y = random.randint(borderLine, (self.fieldHeight - (borderLine + 1)))
        fld = self.grid.itemAtPosition(y, x).widget()
        fld.setHead()
        self.snake.append((x, y))
        
        if x <= ((self.fieldWidth - 1) / 2):
            initialDirectionX = 1
        else:
            initialDirectionX = -1
        
        if y <= ((self.fieldHeight - 1) / 2):
            initialDirectionY = 1
        else:
            initialDirectionY = -1
        
        # Add snake body
        while len(self.snake) < self.initSnakeSize:
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

            fld = self.grid.itemAtPosition(y, x).widget()
            fld.setSnake()
            self.snake.append((x, y))
        
        # Add apples
        while len(self.apples) < self.initApplesCount:
            self.addApple()

    def updateScore(self):
        self.scoreLabel.setText("%03d" % self.currentScore)

    def addApple(self):
        while True:
            x, y = random.randint(0, self.fieldWidth - 1), random.randint(0, self.fieldHeight - 1)
            if (x, y) not in self.snake and (x, y) not in self.apples:
                fld = self.grid.itemAtPosition(y, x).widget()
                fld.setApple()
                self.apples.append((x, y))
                self.resetAppleTimer()
                break

    def resetAppleTimer(self):
        yield
        #~ self.appleTimer = QTimer()
        #~ self.appleTimer.timeout.connect(self.appleTimerTimeout)
        #~ self.appleTimer.start(self.appleTimeout * 1000)

    def appleTimerTimeout(self):
        for x in range(0, self.addApplesOnTimeout):
            self.addApple()

    def moveSnake(self):
        if not self.isStarted:
            return
        
        x, y = self.snake[0]
        currentFld = self.grid.itemAtPosition(y, x).widget()
        
        if self.direction == UserInterface.MOVE_UP:
            y -= 1
        elif self.direction == UserInterface.MOVE_RIGHT:
            x += 1
        elif self.direction == UserInterface.MOVE_DOWN:
            y += 1
        elif self.direction == UserInterface.MOVE_LEFT:
            x -= 1
        
        if x < 0 or x > (self.fieldWidth - 1) or y < 0 or y > (self.fieldHeight - 1):
            self.gameOver()
            return
        if (x, y) in self.snake:
            self.gameOver()
            return
        
        nextFld = self.grid.itemAtPosition(y, x).widget()
        
        if nextFld.isApple:
            self.apples.remove((x, y))
            self.movesToGrow += self.growSnakeSegments
            self.currentScore += 1
            self.updateScore()
            if len(self.apples) == 0:
                self.addApple()
        
        nextFld.setHead()
        currentFld.setSnake()
        self.snake.insert(0, (x, y))
        
        if self.movesToGrow > 0:
            self.movesToGrow -= 1
        elif self.movesToGrow == 0:
            x, y = self.snake.pop();
            lastFld = self.grid.itemAtPosition(y, x).widget()
            lastFld.reset()

    def keyPressEvent(self, event):
        key = event.key()
        if (key == Qt.Key_Left or key == Qt.Key_A) and self.direction != UserInterface.MOVE_RIGHT:
            self.direction = UserInterface.MOVE_LEFT
        elif (key == Qt.Key_Right or key == Qt.Key_D) and self.direction != UserInterface.MOVE_LEFT:
            self.direction = UserInterface.MOVE_RIGHT
        elif (key == Qt.Key_Down or key == Qt.Key_S) and self.direction != UserInterface.MOVE_UP:
            self.direction = UserInterface.MOVE_DOWN
        elif (key == Qt.Key_Up or key == Qt.Key_W) and self.direction != UserInterface.MOVE_DOWN:
            self.direction = UserInterface.MOVE_UP
        elif key == Qt.Key_Space:
            self.direction = None
            self.isStarted = False
            self.snakeTimer.stop()
        else:
            return
        
        if not self.isStarted and self.direction is not None:
            self.isStarted = True
            self.snakeTimer.start(self.snakeSpeed * 1000)

    def gameOver(self):
        self.direction = None
        self.isStarted = False
        self.snakeTimer.stop()
        self.statusbar.showMessage('GAME OVER!')
        
        palette = self.scoreLabel.palette()
        palette.setColor(QPalette.WindowText, Qt.red)
        self.scoreLabel.setPalette(palette)

    def createWindow(self):
        # Create a grid
        self.grid = QGridLayout()
        self.grid.setSpacing(self.spacing)
        self.initFields()
        self.reset()
        
        winWidth = (self.fieldWidth * (self.resolution + self.spacing)) + self.spacing
        winHeight = (self.fieldHeight * (self.resolution + self.spacing)) + self.spacing + self.fontSize
        
        # Create vertical box
        vBox = QVBoxLayout()
        
        # Create label for score
        self.scoreLabel = QLabel()
        self.scoreLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # Update font size
        font = self.scoreLabel.font()
        font.setPointSize(self.fontSize)
        font.setWeight(self.fontWeight)
        self.scoreLabel.setFont(font)
        palette = self.scoreLabel.palette()
        palette.setColor(QPalette.WindowText, Qt.black)
        self.scoreLabel.setPalette(palette)
        self.updateScore()
        
        # Create horizontal box
        hBox = QHBoxLayout()
        hBox.addWidget(self.scoreLabel)
        
        # Add horizontal box to vertical box
        vBox.addLayout(hBox)
        
        # Add grid to vertical box
        vBox.addLayout(self.grid)
        
        # Create widget
        widget = QWidget()
        widget.setLayout(vBox)
        
        self.setMinimumSize(QSize(winWidth, winHeight))
        self.setWindowTitle("Snake")
        self.setCentralWidget(widget)
        self.show()

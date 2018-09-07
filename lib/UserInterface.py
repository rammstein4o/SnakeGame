import random
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPalette, QIcon
from lib.Field import Field
from lib.Snake import Snake
from lib.Apples import Apples
from lib.Configurable import Configurable

class UserInterface(Configurable, QMainWindow):
    MOVE_UP = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3
    MOVE_LEFT = 4
    
    def __init__(self, config, *args, **kwargs):
        Configurable.__init__(self, config, *args, **kwargs)
        QMainWindow.__init__(self)
        
        self.snakeTimer = QTimer()
        self.snakeTimer.timeout.connect(self.moveSnake)
        self.statusbar = self.statusBar()
        
        self.createGrid()
        self.createResetButton()
        self.createStartButton()
        self.createPauseButton()
        self.createScoreLabel()
        
        self.apples = Apples(self.config, self.grid)
        self.snake = Snake(self.config, self.grid)
        self.apples.setSnake(self.snake)

    def updateScore(self):
        self.scoreLabel.setText("%03d" % self.currentScore)

    def resetAppleTimer(self):
        yield
        #~ self.appleTimer = QTimer()
        #~ self.appleTimer.timeout.connect(self.appleTimerTimeout)
        #~ self.appleTimer.start(self.appleTimeout * 1000)

    def appleTimerTimeout(self):
        for x in range(0, self.addApplesOnTimeout):
            self.apples.addApple()

    def moveSnake(self):
        if not self.isRunning or self.isGameOver:
            return
        
        x, y = self.snake.first()
        currentFld = self.grid.itemAtPosition(y, x).widget()
        
        if self.direction == UserInterface.MOVE_UP:
            y -= 1
        elif self.direction == UserInterface.MOVE_RIGHT:
            x += 1
        elif self.direction == UserInterface.MOVE_DOWN:
            y += 1
        elif self.direction == UserInterface.MOVE_LEFT:
            x -= 1
        else:
            return
        
        if x < 0 or x > (self.fieldWidth - 1) or y < 0 or y > (self.fieldHeight - 1):
            self.gameOver()
            return
        if self.snake.exists((x, y)):
            self.gameOver()
            return
        
        nextFld = self.grid.itemAtPosition(y, x).widget()
        
        if nextFld.isApple:
            self.apples.remove((x, y))
            self.movesToGrow += self.growSnakeSegments
            self.currentScore += 1
            self.updateScore()
            if self.apples.len() == 0:
                self.apples.addApple()
        
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
        else:
            event.ignore()

    def resetGame(self):
        self.direction = None
        self.currentScore = 0
        self.updateScore()
        self.movesToGrow = 0
        self.snake.empty()
        self.apples.empty()
        self.isRunning = False
        self.isGameOver = False
        self.resetButton.hide()
        self.startButton.show()
        self.pauseButton.hide()
        self.setScoreLabelColor(Qt.black)
        self.statusbar.clearMessage()
        
        # Reset all fields
        for x in range(0, self.fieldWidth):
            for y in range(0, self.fieldHeight):
                fld = self.grid.itemAtPosition(y, x).widget()
                fld.reset()
        
        # Add snake
        self.snake.initSnake()
        
        # Add apples
        self.apples.initApples()

    def startGame(self):
        self.isRunning = True
        self.snakeTimer.start(self.snakeSpeed * 1000)
        self.resetButton.hide()
        self.startButton.hide()
        self.pauseButton.show()

    def stopGame(self):
        self.isRunning = False
        self.snakeTimer.stop()
        self.resetButton.hide()
        self.startButton.show()
        self.pauseButton.hide()

    def gameOver(self):
        self.isGameOver = True
        self.isRunning = False
        self.snakeTimer.stop()
        self.resetButton.show()
        self.startButton.hide()
        self.pauseButton.hide()
        self.statusbar.showMessage('GAME OVER!')
        self.setScoreLabelColor(Qt.red)

    def createGrid(self):
        # Create a grid
        self.grid = QGridLayout()
        self.grid.setSpacing(self.spacing)
        for x in range(0, self.fieldWidth):
            for y in range(0, self.fieldHeight):
                fld = Field(self.config, x, y)
                self.grid.addWidget(fld, y, x)

    def createScoreLabel(self):
        # Create label for score
        self.scoreLabel = QLabel()
        self.scoreLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # Update font size
        font = self.scoreLabel.font()
        font.setPointSize(self.fontSize)
        font.setWeight(self.fontWeight)
        self.scoreLabel.setFont(font)
        self.setScoreLabelColor(Qt.black)

    def setScoreLabelColor(self, color):
        palette = self.scoreLabel.palette()
        palette.setColor(QPalette.WindowText, color)
        self.scoreLabel.setPalette(palette)
    
    def createButton(self, tooltip, icon, callback):
        button = QPushButton()
        button.setToolTip(tooltip)
        button.setFixedSize(QSize(40, 40))
        button.setIconSize(QSize(40, 40))
        button.setIcon(QIcon(icon))
        button.setFlat(True)
        button.clicked.connect(callback)
        button.hide()
        return button
    
    def createResetButton(self):
        self.resetButton = self.createButton('Reset game', './assets/reset.png', self.resetGame)

    def createStartButton(self):
        self.startButton = self.createButton('Start game', './assets/play.png', self.startGame)

    def createPauseButton(self):
        self.pauseButton = self.createButton('Pause game', './assets/pause.png', self.stopGame)

    def createWindow(self):
        self.resetGame()
        
        winWidth = (self.fieldWidth * (self.resolution + self.spacing)) + self.spacing
        winHeight = (self.fieldHeight * (self.resolution + self.spacing)) + self.spacing + self.fontSize
        
        # Create vertical box
        vBox = QVBoxLayout()
        
        # Create horizontal box
        hBox = QHBoxLayout()
        hBox.addWidget(self.scoreLabel)
        hBox.addWidget(self.resetButton)
        hBox.addWidget(self.startButton)
        hBox.addWidget(self.pauseButton)
        
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

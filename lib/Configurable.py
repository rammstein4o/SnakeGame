
class Configurable(object):
    def __init__(self, config, *args, **kwargs):
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

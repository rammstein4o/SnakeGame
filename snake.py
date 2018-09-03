import configparser
from lib.Application import Application

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    app = Application(config)
    app.run()

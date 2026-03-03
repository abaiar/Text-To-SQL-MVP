import sys,os
from loguru import logger

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(root_dir, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)



class MyLogger:
    def __init__(self):
        self.logger = logger
        self.logger.remove()
        self.logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
        self.logger.add(os.path.join(log_dir, 'log.log'), rotation="500 MB", encoding="utf-8")

        def get_logger(self):
            return self.logger

log = MyLogger().get_logger()

if __name__ == '__main__':
    print('str.pdf'['str.pdf'.rindex('.'):])

    def test():
        try:
            print(1/0)
        except Exception as e:
            log.error(e)

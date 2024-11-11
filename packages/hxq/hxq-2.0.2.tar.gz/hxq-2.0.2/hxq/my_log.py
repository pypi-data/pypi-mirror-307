import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler


class Log(logging.Logger):
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    def __init__(self, logs_path='logs', level=NOTSET, stream=True, file=True):
        """
        logs_path:log储存文件地址,默认为logs
        stream:是否输出到控制台
        file:是否保存到文件
        """
        self.level = level
        self.stream = stream
        self.file = file
        super().__init__(__name__, level=level)
        # 设置输出格式，依次为，线程，时间，名字，信息。
        self.fmt = '[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)-3d] %(threadName)s [%(name)s]:%(message)s'
        self.logs_path = logs_path  # logs文件夹

    def set_name(self, name=''):
        """
        file_name：保存的文件名
        name:日志名字
        """
        # 解决重复输出的问题
        if self.handlers:
            return
        if self.stream:
            self.__set_stream_handler__()
        if self.file:
            self.__set_file_handler__(name)
        return self

    def reset_name(self, name):
        """
        重置文件名
        :param name:文件名称
        :return:
        """
        self.name = name
        self.removeHandler(self.file_handler)
        self.__set_file_handler__(name)
        return self

    def __set_file_handler__(self, file_name: str):
        """
        设置输出文件
        """
        # 去除影响文件名称不规范的杂质
        for item in r'\/:*?!`~^&%$"<>|;':
            file_name = file_name.replace(item, '')
        self.name = file_name or self.name
        # file_name = [file_name := file_name.replace(char, '') for char in r'\/:*?"<>|;'].pop()  # 3.8以上 去除非法文件字符
        logs_dir = '{}/{}-Logs'.format(self.logs_path, file_name)
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):  # 存在且是文件夹
            pass
        else:
            os.makedirs(logs_dir)
        # 修改log保存位置和文件名
        # time_stamp = time.strftime("%Y-%m-%d", time.localtime())
        # log_file_name = '{}.txt'.format(time_stamp)
        filename = os.path.join(logs_dir, 'log.txt')
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留365天
        file_handler = TimedRotatingFileHandler(filename=filename, when='midnight', interval=1, backupCount=365,
                                                encoding='utf-8')
        file_handler.setLevel(self.level)
        formatter = logging.Formatter(self.fmt, '%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def __set_stream_handler__(self):
        """
        设置控制台输出
        """
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(self.fmt, '%Y-%m-%d %H:%M:%S')
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(self.level)
        self.addHandler(stream_handler)


my_log = Log()

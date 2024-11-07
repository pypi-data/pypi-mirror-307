import logging
import uuid
import os
from datetime import datetime
import sys
import threading
from contextvars import ContextVar

# 自定义trace_filter属性名
TRACE_FILTER_ATTR = "trace_filter"
# 当前线程的local_trace, 需要添加全局trace_id, 使用示例：trace.trace_id
local_trace = threading.local()
formatter = logging.Formatter(
    'time:%(asctime)s, traceId:%(trace_id)s, %(asctime)s - %(name)s - %(levelname)s - %(message)s')
_trace_id: ContextVar[str] = ContextVar('x_trace_id', default="")
_x_request_id: ContextVar[str] = ContextVar('_x_request_id', default="")


class TraceID:
    @staticmethod
    def set(req_id: str) -> ContextVar[str]:
        """设置请求ID，外部需要的时候，可以调用该方法设置
        Returns:
            ContextVar[str]: _description_
        """
        if req_id:
            _x_request_id.set(req_id)
        return _x_request_id

    @staticmethod
    def set_trace(trace_id: str) -> ContextVar[str]:
        """设置trace_id
        Returns:
            ContextVar[str]: _description_
        """
        if trace_id:
            _trace_id.set(trace_id)
        return _trace_id

    @staticmethod
    def new_trace():
        trace_id = uuid.uuid4().hex
        _trace_id.set(trace_id)

    @staticmethod
    def get_trace() -> str:

        """获取trace_id
        Returns:
            str: _description_
        """
        return _trace_id.get()


class TraceFilter(logging.Filter):
    """
    通过在record中添加trace_id, 实现调用跟踪和日志打印的分离
    """

    def __init__(self, name=""):
        """
        init
        @param name: filter name
        """
        super().__init__(name)

    def filter(self, record):
        """
        重写filter方法
        @param record: record
        @return:
        """
        # trace_id = local_trace.trace_id if hasattr(local_trace, 'trace_id') else uuid.uuid1()
        print("trace_id", _trace_id.get())
        record.trace_id = _trace_id.get()
        return True


class TraceLogger:
    @staticmethod
    def get_log_file_path(logger_name):
        # 创建日志文件路径
        basedir = os.path.abspath('..')
        log_dir_name = 'logs'
        current_working_directory = os.getcwd()
        log_file_path = os.path.join(current_working_directory, log_dir_name)
        log_dir = os.path.join(basedir, log_file_path)
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        log_file_name = "user_{}_log.{}.log".format(logger_name, str(datetime.now().strftime('%Y-%m-%d')))
        log_file_path = os.path.join(log_dir, log_file_name)
        return log_file_path

    @staticmethod
    def get_logger_func(logger_name, logger_level=logging.DEBUG, console_level=logging.INFO, is_console=True):
        # 创建一个名为'access'的日志记录器实例
        access_filename = TraceLogger.get_log_file_path(logger_name)
        access_logger = logging.getLogger(logger_name)
        access_logger.setLevel(logger_level)  # 设置日志记录器的最低捕获级别为DEBUG
        # 添加日志跟踪filter
        trace_filter = TraceFilter()
        access_logger.addFilter(trace_filter)
        # 创建一个文件处理器，用于输出logger1的日志到'debug.log'
        access_debug = logging.FileHandler(access_filename, encoding='utf-8', delay=False)
        # access_debug.setLevel(logging.DEBUG)  # 设置处理器的级别为DEBUG
        # 将格式化器添加到处理器中
        access_debug.setFormatter(formatter)
        # 将处理器添加到日志记录器中
        access_logger.addHandler(access_debug)
        if is_console:
            # 再创建一个handler，用于将日志输出到控制台
            console_handler = logging.StreamHandler()
            console_handler.setLevel(console_level)  # 设置控制台handler的日志级别
            console_handler.setFormatter(formatter)
            access_logger.addHandler(console_handler)

        return access_logger


# 创建一个日志格式化器


access_logger = TraceLogger.get_logger_func("access")
server_logger = TraceLogger.get_logger_func("server", is_console=False)
error_logger = TraceLogger.get_logger_func("error", logger_level=logging.ERROR, console_level=logging.ERROR)

# error_logger = TraceLogger.get_logger()
console_handler = logging.StreamHandler()
# logger = TraceLogger.get_logger()
# server_logger = TraceLogger.get_server_logger()
# error_logger = TraceLogger.get_server_logger()

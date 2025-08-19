import logging
import logging.config

# 定义日志配置
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'detailed',
            'class': 'logging.FileHandler',
            'filename': 'agi_deployment.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'self_replication': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'global_brain_deployment': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'autonomous_deployment': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'self_expansion': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

# 应用日志配置
def setup_logging():
    """
    设置日志配置
    """
    logging.config.dictConfig(LOGGING_CONFIG)

# 获取特定模块的日志记录器
def get_logger(name):
    """
    获取指定名称的日志记录器
    
    Args:
        name (str): 日志记录器名称
        
    Returns:
        logging.Logger: 日志记录器实例
    """
    return logging.getLogger(name)
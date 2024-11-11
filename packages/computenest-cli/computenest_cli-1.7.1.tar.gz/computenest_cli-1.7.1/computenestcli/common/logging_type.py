from enum import Enum

class LoggingType(Enum):
    """
    日志打印类别
    """
    # 暴露给用户
    # 用户可看的日志统一收集到/tmp/build-service.log
    USER = "user"
    # 暴露给开发者
    # 开发者可看的日志统一收集到/tmp/developer.log
    DEVELOPER = "developer"
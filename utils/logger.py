from loguru import logger
import os
import sys
 #创建日志目录
if not os.path.exists('./logs'):
    os.makedirs('./logs')#目录里是否存在这个文件夹，如果没有就创建一个

    # 先清空默认的loguru配置（避免重复输出）
    logger.remove()

    # 配置1：输出到控制台（关键！pytest-html会捕获控制台日志）
    logger.add(
        sink=sys.stdout,  # 输出到标准控制台
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",  # 和文件日志格式一致
        enqueue=True  # 异步输出，避免日志丢失
    )

    #配置日志同时输入到控制台和文件
logger.add(
    sink='./logs/test.log',#日志文件路径
    level='INFO',#级别，只看INFO以上的
    rotation='500MB',#文件大小超过500MB自动分割
    retention='7 days',#日志保留7天
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}' #日志格式
)
#使其他文件可以直接导入
log=logger
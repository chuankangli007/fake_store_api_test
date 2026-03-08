from loguru import logger
import os
 #创建日志目录
if not os.path.exists('./logs'):
    os.makedirs('./logs')#目录里是否存在这个文件夹，如果没有就创建一个

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
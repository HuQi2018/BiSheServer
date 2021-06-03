# Redis 连接工具
import socket
import sys

import redis
from BiSheServer.settings import CONFIG

try:
    socket.create_connection((CONFIG.get('REDIS', 'REDIS_HOST'), CONFIG.get('REDIS', 'REDIS_PORT')))
except Exception as ex:
    print("Redis连接失败！请检查Redis服务以及配置是否正常后再启动系统！", ex)
    sys.exit()

POOL = redis.ConnectionPool(host=CONFIG.get('REDIS', 'REDIS_HOST'), port=CONFIG.get('REDIS', 'REDIS_PORT'),
                            password=CONFIG.get('REDIS', 'REDIS_PASSWORD'), max_connections=1000)
cache = redis.Redis(connection_pool=POOL)

# redis_client.py
import redis
from redis.sentinel import Sentinel

class CacheSentinelClient:
    def __init__(self, sentinels, master_name, password, socket_timeout=1):
        self.sentinels = sentinels
        self.master_name = master_name
        self.password = password
        self.socket_timeout = socket_timeout

        # 创建 Sentinel 对象
        self.sentinel = Sentinel(self.sentinels, socket_timeout=self.socket_timeout, password=self.password)

        # 获取主节点和从节点
        self.master = self.sentinel.master_for(self.master_name, socket_timeout=self.socket_timeout, password=self.password)
        self.slave = self.sentinel.slave_for(self.master_name, socket_timeout=self.socket_timeout, password=self.password)

    def set(self, key, value):
        return self.master.set(key, value)

    def set5min(self, key, value):
        return self.master.set(key, value,ex=300)

    def delete(self,key):
        self.master.delete(key)

    def get(self, key):
        value = self.slave.get(key)
        if value is None:
            return None
        return value.decode("utf-8")


    def incr(self, key):
        try:
            return self.master.incr(key)
        except redis.exceptions.RedisError as e:
            print(f'Error incrementing key {key}: {e}')
            return None

    def keys(self, pattern='*'):
        try:
            return self.slave.keys(pattern)
        except redis.exceptions.RedisError as e:
            print(f'Error getting keys with pattern {pattern}: {e}')
            return []

# 配置哨兵
sentinels = [
    ('192.168.0.164',26379),
    ('192.168.0.163',26379)
]

# 创建 Redis 客户端实例
cache_sentinel_client = CacheSentinelClient(sentinels, 'mymaster', 'imslave')

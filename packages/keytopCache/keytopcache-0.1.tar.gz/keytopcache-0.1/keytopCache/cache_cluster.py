# myredisclient/myredisclient/redis_client.py
import redis

class CacheClusterClient:
    def __init__(self, host='localhost', port=6379, password=None, db=0):
        self.host = host
        self.port = port
        self.password = password
        self.db = db

        # 创建 Redis 连接
        self.client = redis.StrictRedis(host=self.host, port=self.port, password=self.password, db=self.db)

    def set(self, key, value):
        return self.client.set(key, value)

    def set5min(self, key, value):
        return self.client.set(key, value,ex=300)

    def get(self, key):
        value = self.client.get(key)
        if value is None:
            return None
        return value.decode("utf-8")

    def delete(self,key):
        self.client.delete(key)

    def incr(self, key):
        return self.client.incr(key)

    def keys(self, pattern='*'):
        return self.client.keys(pattern)

# 创建 Redis 客户端实例
cache_cluster_client = CacheClusterClient(host='192.168.0.164', port=9223, password='imslave', db=0)

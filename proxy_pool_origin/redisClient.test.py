from redisClient import RedisClient
REDIS_KEY = 'test'

client = RedisClient()

# print(client.db.zscore(REDIS_KEY, '111'))
# print(client.db.zadd(REDIS_KEY, {'111': 12}))
print(client.db.zincrby(REDIS_KEY, -1, '111'))

print(client.add('1112'))

print(client.all())

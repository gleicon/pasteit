# uuid generator
import redis


class IdGenerator():
    def __init__(self, name="generic"):
        p = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self._redis = redis.Redis(connection_pool=p)
        self._countername = "%s:counter" % name

    def request(self):
        return self._redis.incr(self._countername)

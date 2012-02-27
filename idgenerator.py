# uuid generator
import redis

class IdGenerator():
    def __init__(self, name = None):
        p = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self._redis = redis.Redis(connection_pool = p)
        self._countername = "%s:counter" % "generic" if not name else name

    def request(self):
        return self._redis.incr(self._countername)

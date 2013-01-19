import redis
import time

# throttle control


class ThrottleControl(object):
    def __init__(self, name=None, reqs_per_minute=2, ban_threshold=12):
        p = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self._redis = redis.Redis(connection_pool=p)
        self._name = "generic" if not name else name
        self._THROTTLENAME = "%s:throttle:%s:%s"
        self._BLACKLIST = "%s:blacklist" % self._name
        self._reqs_per_minute = reqs_per_minute
        self._ban_threshold = ban_threshold

    def check(self, ip):
        s = self._redis.sismember(self._BLACKLIST, ip)

        if s is True:
            return False

        lt = time.localtime()
        ts = time.strftime("%Y:%m:%d:%H:%M", lt)
        key = self._THROTTLENAME % (self._name, ts, ip)
        t = self._redis.incr(key)

        if t == 1:
            t = self._redis.expire(key, 600)  # expires in 10 minutes

        if t > self._ban_threshold:
            self._redis.sadd(self._BLACKLIST, ip)

        if t > self._reqs_per_minute:
            return False

        return True

    def unban_ip(self, ip):
        self._redis.srem(self._BLACKLIST, ip)

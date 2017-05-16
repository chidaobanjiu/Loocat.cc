from models import Mongua
import json
import logging
ogger = logging.getLogger("blog")


class Cache(object):
    def get(self, key):
        pass

    def set(self, key, value):
        pass


class MemoryCache(Cache):
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache[key]

    def set(self, key, value):
        self.cache[key] = value


class RedisCache(Cache):
    import redis
    redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set(self, key, value):
        return RedisCache.redis_db.set(key, value)

    def get(self, key):
        return RedisCache.redis_db.get(key)


class Blog(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('title', str, ''),
        ('content', str, ''),
        ('author', str, ''),
        ('image', str, ''),
        ('category', int, -1),
    ]

    should_update_all = True
    # 1. memory cache
    # cache = MemoryCache()
    # 2. redis cahce
    redis_cache = RedisCache()

    def to_json(self):
        d = dict()
        for k in Blog.__fields__:
            key = k[0]
            if not key.startswith('_'):
                d[key] = getattr(self, key)
        return json.dumps(d)

    @classmethod
    def from_json(cls, j):
        d = json.loads(j)

        instance = cls()
        for k, v in d.items():
            setattr(instance, k, v)
        return instance

    @classmethod
    def all_delay(cls):
        # time.sleep(3)
        return Blog.all()

    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def save(self):
        super(Blog, self).save()
        Blog.should_update_all = True

    @classmethod
    def cache_all(cls):
        # 2. redis cache
        if Blog.should_update_all:
            Blog.redis_cache.set('blog_all', json.dumps([i.to_json() for i in cls.all_delay()]))
            Blog.should_update_all = False
        j = json.loads(Blog.redis_cache.get('blog_all').decode('utf-8'))
        j = [Blog.from_json(i) for i in j]
        return j


class BlogComment(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('content', str, ''),
        ('author', str, ''),
        ('blog_id', int, ''),
    ]
from models import Mongua
from models.blog import Blog

import json
import logging
ogger = logging.getLogger("category")


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


class Category(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('title', str, ''),
        ('image', str, ''),
        ('abstract', str, ''),

    ]

    should_update_all = True
    # 1. memory cache
    cache = MemoryCache()
    # 2. redis cahce
    redis_cache = RedisCache()

    def to_json(self):
        d = dict()
        for k in Category.__fields__:
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
        return Category.all()

    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def save(self):
        super(Category, self).save()
        should_update_all = True

    @classmethod
    def cache_all(cls):
        # 2. redis cache
        if Category.should_update_all:
            Category.redis_cache.set('topic_all', json.dumps([i.to_json() for i in cls.all_delay()]))
            Category.should_update_all = False
        j = json.loads(Category.redis_cache.get('topic_all').decode('utf-8'))
        j = [Category.from_json(i) for i in j]
        return j

    def blogs(self):
        blogs = Blog.find_all(category=self.id)
        return blogs

    def cached_blogs(self):
        # 2. redis cache
        #if Category.should_update_all:
        Category.redis_cache.set('category_all_blogs', json.dumps([i.to_json() for i in self.blogs()]))
            # Category.should_update_all = False
        j = json.loads(Category.redis_cache.get('category_all_blogs').decode('utf-8'))
        j = [Category.from_json(i) for i in j]
        return j

    def blog(self):
        # 返回找到的第一个博客
        return Blog.find_by(category=self.id)


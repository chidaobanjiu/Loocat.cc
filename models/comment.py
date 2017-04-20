from models import Mongua


class Comment(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('content', str, ''),
        ('author', str, ''),
        ('blog_id', int, ''),
    ]


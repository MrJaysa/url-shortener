from functools import wraps
from App.model import HitCount, Hits, UrlCount
from flask import request
from datetime import date
from sqlalchemy import func

def hits(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not Hits.query.filter_by(ip=request.remote_addr, sys=request.headers.get('User-Agent')).filter(func.date(Hits.timestamp) == date.today()).all():
            hit = Hits()
            hit.create(ip=request.remote_addr, sys = request.headers.get('User-Agent'))
            hit.save()
            hit.add_count()

        return f(*args, **kwargs)
    return decorator

def get_counts(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        hit_count = HitCount.query.first().count
        url_count = UrlCount.query.first().count
        return f(hit_count, url_count, *args, **kwargs)
    return decorator
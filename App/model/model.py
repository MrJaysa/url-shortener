from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class UrlCount(db.Model):
    id = db.Column('id_', db.Integer, primary_key=True)
    count = db.Column('count', db.Integer, default=0)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Urls(db.Model):
    
    id = db.Column('id_', db.Integer, primary_key=True)
    long = db.Column('long', db.String())
    short = db.Column('short', db.String())
    url = db.Column('url', db.String())
    timestamp = db.Column('timestamp', db.DateTime, server_default=func.now())

    def create(self, long, short, url):
        self.long = long
        self.short = short
        self.url = url

    def add_count(self):
        count = UrlCount.query.first()
        count.count += 1
        count.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

class HitCount(db.Model):
    id = db.Column('id_', db.Integer, primary_key=True)
    count = db.Column('count', db.Integer, default=0)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Hits(db.Model):
    id = db.Column('id_', db.Integer, primary_key=True)
    ip = db.Column('ip', db.String())
    sys = db.Column('sys', db.String())
    timestamp = db.Column('timestamp', db.DateTime, server_default=func.now())

    def create(self, ip, sys):
        self.ip = ip
        self.sys = sys

    def add_count(self):
        count = HitCount.query.first()
        count.count += 1
        count.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
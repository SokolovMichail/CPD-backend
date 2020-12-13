from app import db
from sqlalchemy.dialects.postgresql import JSON

class Graph(db.Model):
    __tablename__ = 'graphstorage'

    token = db.Column(db.VARCHAR, primary_key=True)
    graph = db.Column(db.Text)

    def __init__(self, token, graph):
        self.token = token
        self.graph = graph

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Graph(db.Model):
    __tablename__ = 'graphstorage'

    token = db.Column(db.VARCHAR, primary_key=True)
    graph = db.Column(db.Text)

    def __init__(self, token, graph):
        self.token = token
        self.graph = graph

    def __repr__(self):
        return '<id {}>'.format(self.id)
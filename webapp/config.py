import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://tkvzeqhgrnbszs:899301ba612f5b92a57b37a2cf961522c71580809f6eb8c79c9b404cde0e4450@ec2-52-210-120-210.eu-west-1.compute.amazonaws.com:5432/da532n97r99dvu"
    #DATABASE_URL = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret_key"
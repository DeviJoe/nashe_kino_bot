from peewee import *
from config import DB

conn = SqliteDatabase(DB)


class BaseModel(Model):
    class Meta:
        database = conn

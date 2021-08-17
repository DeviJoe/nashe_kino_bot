import peewee
from models.BaseModel import BaseModel
from models import Team


class User(BaseModel):
    user_id = peewee.TextField(column_name='user_id')
    username = peewee.TextField(column_name='username')
    team_id = peewee.IntegerField(column_name='team_id')
    chat_id = peewee.AutoField(column_name='chat_id')

    class Meta:
        table_name = 'users'
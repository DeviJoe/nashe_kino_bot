import peewee
from models.BaseModel import BaseModel


class Money(BaseModel):
    team_id = peewee.AutoField(column_name='team_id')
    money = peewee.IntegerField(column_name='money', null=True)

    class Meta:
        table_name = 'money'

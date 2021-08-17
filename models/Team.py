import peewee
from models.BaseModel import BaseModel


class Team(BaseModel):
    team_id = peewee.AutoField(column_name='team_id')
    score = peewee.IntegerField(column_name='score', null=True)

    class Meta:
        table_name = 'teams'

import peewee
from models.BaseModel import BaseModel


class Point(BaseModel):
    point_id = peewee.AutoField(column_name='point_id')
    latitude = peewee.FloatField(column_name='latitude', null=True)
    longitude = peewee.FloatField(column_name='longitude', null=True)
    description = peewee.TextField(column_name='description')

    class Meta:
        table_name = 'points'

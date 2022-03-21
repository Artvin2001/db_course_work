from peewee import *

db = PostgresqlDatabase('turbot', user='postgres', password='Artvin2001', host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Climate_cl(BaseModel):
    id = IntegerField(column_name='id', primary_key=True)
    tur_month = CharField(column_name= 'tur_month')
    day_temp = IntegerField(column_name= 'day_temp')
    night_temp = IntegerField(column_name= 'night_temp')
    water_temp = IntegerField(column_name= 'water_temp')

    class Meta:
        table_name = 'climate'

class Inform_cl(BaseModel):
    id = IntegerField(column_name='id', primary_key=True)
    capital = CharField(column_name='capital')
    population = FloatField(column_name='population')
    image = CharField(column_name='image')
    descr = TextField(column_name='descr')

    class Meta:
        table_name = 'information'

class Countries_cl(BaseModel):
    id = IntegerField(column_name='id', primary_key=True)
    id_info = IntegerField(column_name='id_info')
    name = CharField(column_name='name')
    continent = CharField(column_name='continent')

    class Meta:
        table_name = 'countries'

def find_info_by_name(name):
    selection = Inform_cl.select().where(Inform_cl.id == Countries_cl.select(Countries_cl.id_info).where(Countries_cl.name == name))
    result = selection.dicts().execute()
    return result

def climate_inform(id):
    selection = Climate_cl.select().where(Climate_cl.id == id)
    result = selection.dicts().execute()
    return result

def info_inform(id):
    selection = Inform_cl.select().where(Inform_cl.id == id)
    result = selection.dicts().execute()
    return result


from peewee import *

db = PostgresqlDatabase('turbot', user='postgres', password='Artvin2001', host='localhost', port=5432)


def new_context(login, password):
    db =  PostgresqlDatabase('turbot', user=login, password=password, host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Users_cl(BaseModel):
    id = IntegerField(column_name='id', primary_key=True)
    login = CharField(column_name='login')
    password = CharField(column_name='password')
    permission = IntegerField(column_name='permission')

    class Meta:
        table_name = 'users'


class Countries_cl(BaseModel):
    id = IntegerField(column_name='id', primary_key=True)
    name = CharField(column_name='name')
    continent = CharField(column_name='continent')
    capital = CharField(column_name='capital')
    population = FloatField(column_name='population')
    image = CharField(column_name='image')
    descr = TextField(column_name='descr')

    class Meta:
        table_name = 'countries'

class Climate_cl(BaseModel):
    id = IntegerField(column_name='id', primary_key=True)
    id_country = IntegerField(column_name='id_country')
    tur_month = CharField(column_name= 'tur_month')
    day_temp = IntegerField(column_name= 'day_temp')
    night_temp = IntegerField(column_name= 'night_temp')
    water_temp = IntegerField(column_name= 'water_temp')

    class Meta:
        table_name = 'climate'

class Cities_cl(BaseModel):
    id = IntegerField(column_name='id', primary_key=True)
    id_country = IntegerField(column_name='id_country')
    name = CharField(column_name='name')
    population = FloatField(column_name='population')
    sight = CharField(column_name='sight')

    class Meta:
        table_name = 'cities'


class Hotels_cl(BaseModel):
    id = IntegerField(column_name='id', primary_key=True)
    id_country = IntegerField(column_name='id_country')
    name = CharField(column_name='name')
    stars = IntegerField(column_name='stars')
    beach = BooleanField(column_name='beach')
    all_inc = BooleanField(column_name='all_inc')

    class Meta:
        table_name = 'hotels'

class Rooms_cl(BaseModel):
    id = IntegerField(column_name='id', primary_key=True)
    id_hotel = IntegerField(column_name='id_hotel')
    name = CharField(column_name='name')
    capacity = IntegerField(column_name='capacity')
    floor = IntegerField(column_name='floor')
    price = IntegerField(column_name='price')

    class Meta:
        table_name = 'rooms'








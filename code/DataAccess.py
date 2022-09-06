import storage
from peewee import *
from abc import ABCMeta, abstractmethod

class UserRepository():
    __metaclass__ = ABCMeta

    @abstractmethod
    def check_user_data(self, login, password):
        """is exist"""

    @abstractmethod
    def check_user_login(self, login):
        """check login"""

    @abstractmethod
    def check_user_password(self, password):
        """check password"""

    @abstractmethod
    def insert_user(self, login, password, permission):
        """insert user"""

    @abstractmethod
    def get_all_users(self):
        """get all users"""

    @abstractmethod
    def delete_user(self, id):
        """delete user"""

    @abstractmethod
    def update_user(self, id, permission):
        """update user"""

    @abstractmethod
    def get_user_id(self, login):
        """get id"""

    @abstractmethod
    def get_user_perm(self, id):
        """get permission"""

class UserRepositoryPSQL(UserRepository):
    def __init__(self):
        self.db = storage.db

    def change_context(self, login, password):
        self.db = storage.new_context(login, password)

    def check_user_data(self, login, password):
        elem = storage.Users_cl.select().where(storage.Users_cl.login == login, storage.Users_cl.password == password)
        return elem

    def check_user_login(self, login):
        elem = storage.Users_cl.select().where(storage.Users_cl.login == login)
        return elem

    def check_user_password(self, password):
        elem = storage.Users_cl.select().where(storage.Users_cl.password == password)
        return elem

    def insert_user(self, login, password, permission):
        max_id = storage.Users_cl.select(fn.MAX(storage.Users_cl.id)).scalar()
        new_id = max_id + 1
        storage.Users_cl.insert(id=new_id, login=login, password=password, permission=permission).execute()

    def get_all_users(self):
        res = storage.Users_cl.select().order_by(storage.Users_cl.id)
        return res

    def delete_user(self, id):
        storage.Users_cl.delete().where(storage.Users_cl.id == id).execute()

    def update_user(self, id, permission):
        storage.Users_cl.update(permission=permission).where(storage.Users_cl.id == id).execute()

    def get_user_id(self, login):
        el = storage.Users_cl.select(storage.Users_cl.id).where(storage.Users_cl.login == login).get()
        return el.id

    def get_user_perm(self, id):
        el = storage.Users_cl.select().where(storage.Users_cl.id == id).get()
        return el

class CountryRepository():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_country_by_name(self, name):
        """"get info by name"""
    @abstractmethod
    def get_all_countries_names(self):
        """get all names"""


class CountryRepositoryPSQL(CountryRepository):
    def __init__(self):
        self.db = storage.db

    def change_context(self, login, password):
        self.db = storage.new_context(login, password)

    def get_country_by_name(self, name):
        elem = storage.Countries_cl.select().where(storage.Countries_cl.name == name).get()
        return elem

    def get_all_countries_names(self):
        res = storage.Countries_cl.select(storage.Countries_cl.name)
        return res

class CityRepository():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_city_by_name(self, country_name, name):
        """info by country"""

    @abstractmethod
    def get_all_cities(self, name):
        """get all names"""

    @abstractmethod
    def change_city_by_country(self, country_name, name, population, sight):
        """update city"""

    @abstractmethod
    def insert_city_by_country(self, country_name, name, population, sight):
        """insert city"""

class CityRepositoryPSQL(CityRepository):
    def __init__(self):
        self.db = storage.db

    def change_context(self, login, password):
        self.db = storage.new_context(login, password)

    #upgarde + country name
    def get_city_by_name(self, name):
        elem = storage.Cities_cl.select().where(storage.Cities_cl.name == name).get()
        return elem

    def get_all_cities(self, name):
        res = storage.Cities_cl.select(storage.Cities_cl.name).where(storage.Cities_cl.id_country == storage.Countries_cl.select(storage.Countries_cl.id)
                                                                     .where(storage.Countries_cl.name == name))
        return res

class ClimateRepository():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_climate_by_country(self, name):
        """get climate"""

    @abstractmethod
    def change_climtae_by_country(self, name, tur_month, day_tamp, nigth_temp, water_temp):
        """update climate"""


class ClimateRepositoryPSQL(ClimateRepository):
    def __init__(self):
        self.db = storage.db

    def change_context(self, login, password):
        self.db = storage.new_context(login, password)

    def get_climate_by_country(self, name):
        elem = storage.Climate_cl.select().where(storage.Climate_cl.id_country == storage.Countries_cl.select(storage.Countries_cl.id).
                                                 where(storage.Countries_cl.name == name)).get()
        return elem

    def change_climtae_by_country(self, name, tur_month, day_tamp, nigth_temp, water_temp):
        storage.Climate_cl.update(tur_month=tur_month, day_temp=day_tamp, night_temp=nigth_temp, water_temp=water_temp).where(storage.Climate_cl.id_country == storage.Countries_cl.select(storage.Countries_cl.id).
                                                 where(storage.Countries_cl.name == name)).execute()

class HotelRepository():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_hotel_by_name(self, name):
        """get hotel"""

    @abstractmethod
    def get_hotel_id_by_name(self, name):
        """get hotel id"""

    @abstractmethod
    def get_all_hotels_by_country(self, name):
        """get all hotels names"""

    @abstractmethod
    def change_hotel_by_name(self, country_name, name, stars, beach, all_inc):
        """update hotel"""

    @abstractmethod
    def insert_hotel(self, name, stars, beach, all_inc, country_name):
        """insert hotel"""

    @abstractmethod
    def check_hotel_name(self, country_name, name):
        """check hotel name"""

class HotelRepositoryPSQL(HotelRepository):
    def __init__(self):
        self.db = storage.db

    def change_context(self, login, password):
        self.db = storage.new_context(login, password)

    def get_hotel_by_name(self, name):
        elem = storage.Hotels_cl.select().where(storage.Hotels_cl.name == name).get()
        return elem

    def get_hotel_id_by_name(self, name):
        id = storage.Hotels_cl.select(storage.Hotels_cl.id).where(storage.Hotels_cl.name == name).get()
        return id

    def get_all_hotels_by_country(self, name):
        res = storage.Hotels_cl.select().where(storage.Hotels_cl.id_country == storage.Countries_cl.select(storage.Countries_cl.id)
                                                                     .where(storage.Countries_cl.name == name))
        return res

    def change_hotel_by_name(self, id, country_name, name, stars, beach, all_inc):
        storage.Hotels_cl.update(name=name, stars=stars, beach=beach, all_inc=all_inc).where(storage.Hotels_cl.id == id, storage.Hotels_cl.id_country == storage.Countries_cl.select(storage.Countries_cl.id).
                                                 where(storage.Countries_cl.name == country_name)).execute()

    def insert_hotel(self, name, stars, beach, all_inc, country_name):
        max_id = storage.Hotels_cl.select(fn.MAX(storage.Hotels_cl.id)).scalar()
        new_id = max_id + 1
        id_country = storage.Countries_cl.select(storage.Countries_cl.id).where(storage.Countries_cl.name == country_name).get()
        storage.Hotels_cl.insert(id=new_id, id_country=id_country, name=name, stars=stars, beach=beach, all_inc=all_inc).execute()

    def check_hotel_name(self, country_name, name):
        elem = storage.Hotels_cl.select().where(storage.Hotels_cl.name == name , storage.Hotels_cl.id_country == storage.Countries_cl.select(storage.Countries_cl.id).
                                                 where(storage.Countries_cl.name == country_name))
        return elem


class RoomRepository():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_room_by_name(self, name, hotel):
        """get hotel"""

    @abstractmethod
    def get_all_rooms_by_hotel(self, name):
        """get all rooms"""

    @abstractmethod
    def get_room_id(self, name, hotel):
         """get room id"""

    @abstractmethod
    def change_room(self, id, name, capacity, floor, price):
        """room update"""

    @abstractmethod
    def insert_room(self, name, capacity, floor, price, hotel):
        """insert hotel"""

    @abstractmethod
    def check_room(self, hotel, name):
        """check room name"""


class RoomRepositoryPSQL(RoomRepository):
    def __init__(self):
        self.db = storage.db

    def change_context(self, login, password):
        self.db = storage.new_context(login, password)

    def get_room_by_name(self, name, hotel):
        elem = storage.Rooms_cl.select().where(storage.Rooms_cl.name == name, storage.Rooms_cl.id_hotel == storage.Hotels_cl.select(storage.Hotels_cl.id).
                                               where(storage.Hotels_cl.name == hotel)).get()
        return elem

    def get_all_rooms_by_hotel(self, name):
        res = storage.Rooms_cl.select().where(storage.Rooms_cl.id_hotel == storage.Hotels_cl.select(storage.Hotels_cl.id).where(storage.Hotels_cl.name == name))
        return res

    def get_room_id(self, name, hotel):
        id = storage.Rooms_cl.select(storage.Rooms_cl.id).where(storage.Rooms_cl.name == name, storage.Rooms_cl.id_hotel == storage.Hotels_cl.
                                                                select(storage.Hotels_cl.id).where(storage.Hotels_cl.name == hotel)).get()
        return id

    def change_room(self, id, name, capacity, floor, price):
        storage.Rooms_cl.update(name=name, capacity=capacity, floor=floor, price=price).where(storage.Rooms_cl.id == id).execute()

    def insert_room(self, name, capacity, floor, price, hotel):
        max_id = storage.Rooms_cl.select(fn.MAX(storage.Rooms_cl.id)).scalar()
        new_id = max_id + 1
        id_hotel = storage.Hotels_cl.select(storage.Hotels_cl.id).where(
            storage.Hotels_cl.name == hotel).get()
        storage.Rooms_cl.insert(id=new_id, id_hotel=id_hotel, name=name, capacity=capacity, floor=floor,
                                 price=price).execute()

    def check_room(self, hotel, name):
        elem = storage.Rooms_cl.select().where(storage.Rooms_cl.name == name, storage.Rooms_cl.id_hotel == storage.Hotels_cl.
                                                                select(storage.Hotels_cl.id).where(storage.Hotels_cl.name == hotel))
        return elem
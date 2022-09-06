import keyboards
import DataAccess
import user
import climate
import hotel
import room

class Facade():
    def __init__(self):
        self.user = user.User(0, '', '', 3)
        self.climate = climate.Climate('', '', 0, 0, 0)
        self.hotel = hotel.Hotel(0, '', '', 0, False, False)
        self.room = room.Room(0, '', '', 0, 0, 0)
        self.mode = "no"
        self.country_rep = DataAccess.CountryRepositoryPSQL()
        self.city_rep = DataAccess.CityRepositoryPSQL()
        self.hotel_rep = DataAccess.HotelRepositoryPSQL()
        self.climate_rep = DataAccess.ClimateRepositoryPSQL()
        self.user_rep = DataAccess.UserRepositoryPSQL()
        self.room_rep = DataAccess.RoomRepositoryPSQL()
        self.keyb = None
        self.id = 0

    def menu_keyb(self):
        if self.user.permission == 2:
            self.keyb = keyboards.UserMenu().keyb
        elif self.user.permission == 1:
            self.keyb = keyboards.ModerMenu().keyb
        elif self.user.permission == 0:
            self.keyb = keyboards.AdminMenu().keyb
        # admin

    def get_all_hotels(self, data):
        return self.hotel_rep.get_all_hotels_by_country(data)




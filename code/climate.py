class Climate():
    def __init__(self, country, tur_month, day_temp, night_temp, water_temp):
        self.country = country
        self.tur_month = tur_month
        self.day_temp = day_temp
        self.night_temp = night_temp
        self.water_temp = water_temp

    def set_country(self, country):
        self.country = country

    def set_month(self, tur_month):
        self.tur_month = tur_month

    def set_day_temp(self, day_temp):
        self.day_temp = day_temp

    def set_night_temp(self, night_temp):
        self.night_temp = night_temp

    def set_water_temp(self, water_temp):
        self.water_temp = water_temp


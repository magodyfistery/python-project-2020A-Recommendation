from models.serializable import Serializable


class City(Serializable):

    def __init__(self, id_country, name):
        self.id_country = id_country
        self.name = name
    @staticmethod
    def select_cities_from_country(connection, id_country):
        cursor = connection.cursor()
        sql = "SELECT name FROM city WHERE id_country={id_country}".format(id_country=id_country)

        try:
            cursor.execute(sql)
            cities = []
            fetch = cursor.fetchall()

            for city in fetch:
                cities.append(City(
                    id_country,
                    city['name']
                ))

            return cities
        except Exception as e:
            print(__name__, "select_cities_from_country: ", "ERROR: " + str(e))
            return None
    @staticmethod
    def select_user_cities(connection):
        cursor = connection.cursor()
        sql = "select city from user group by city order by city"
        try:
            cursor.execute(sql)
            cities = []
            fetch = cursor.fetchall()
            for city in fetch:
                cities.append(city['city'])
            return cities
        except Exception as e:
            print(__name__, "select_user_cities: " , "ERROR", str(e))
    @staticmethod
    def select_alluser_cities(connection):
        cursor = connection.cursor()
        sql = "select id,city from user where username in (select username_user from user_product_rating) order by city"
        try:
            cursor.execute(sql)
            cities = []
            fetch = cursor.fetchall()
            for city in fetch:                              #Reutilizo el constructor de esta clase para obtener
                cities.append(City(city['id'],city['city'])) # [user_id,user_city_name]
            return cities
        except Exception as e:
            print(__name__, "select_alluser_cities: " , "ERROR", str(e))
    @staticmethod
    def check_user_city(connection,user_id):
        cursor = connection.cursor()
        sql = "select city from user where id={user_id} and username in (select username_user from user_product_rating)".format(user_id=user_id)
        try:
            cursor.execute(sql)
            city = cursor.fetchone()
            if city:
                return city['city']
            else:
                return None
        except Exception as e:
            print(__name__, "check_user_city: ", "ERROR: " + str(e))
            return None

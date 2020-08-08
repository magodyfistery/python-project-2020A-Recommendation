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
class Country:

    def __init__(self, country_id, name):
        self.id = country_id
        self.name = name

    @staticmethod
    def select_countries(connection):
        cursor = connection.cursor()
        sql = "SELECT * FROM country"

        try:
            cursor.execute(sql)
            countries = []
            fetch = cursor.fetchall()

            for country in fetch:
                countries.append(Country(
                    country['id'],
                    country['name']
                ))

            return countries
        except Exception as e:
            print(__name__, "select_countries: ", "ERROR: " + str(e))
            return None
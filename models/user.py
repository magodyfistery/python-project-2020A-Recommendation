from models.serializable import Serializable


class User(Serializable):

    def __init__(self, username, fullname, country_id, city_name, email, passwd):
        self.username = username  # varchar(30)
        self.fullname = fullname  # varchar(255)
        self.country_id = country_id  # int
        self.city_name = city_name  # varchar(255)
        self.email = email  # varchar(255)
        self.passwd = passwd  # varchar(255)

    def register(self, connection):
        cursor = connection.cursor()
        sql = "INSERT INTO user(username, fullname, id_country, city, email, passwd) "
        sql += "VALUES('{0}', '{1}', {2}, '{3}', '{4}', '{5}')"
        sql = sql.format(self.username, self.fullname, self.country_id, self.city_name, self.email, self.passwd)

        try:
            cursor.execute(sql)
            connection.commit()
            return True

        except Exception as e:
            print(__name__, "register: ", "ERROR: " + str(e))
            return False

    def authAndRetrieve(self, connection):
        cursor = connection.cursor()
        sql = "SELECT * FROM user WHERE username='{0}' AND passwd='{1}'".format(self.username, self.passwd)

        try:
            cursor.execute(sql)
            user = cursor.fetchone()

            if user is None:
                return False
            else:
                self.fullname = user['fullname']
                self.email = user['email']
                self.city_name = user['city']
                self.country_id = int(user['id_country'])
                return True

        except Exception as e:
            print(__name__, "auth: ", "ERROR: " + str(e))
            return False

    def update(self, connection):
        cursor = connection.cursor()
        sql = "UPDATE user SET fullname='{0}', id_country={1}, city='{2}', email='{3}' WHERE username='{4}'"
        sql = sql.format(self.fullname, self.country_id, self.city_name, self.email,  self.username)

        try:
            cursor.execute(sql)
            connection.commit()
            return True

        except Exception as e:
            print(__name__, "update: ", "ERROR: " + str(e))
            return False


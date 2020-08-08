from models.serializable import Serializable


class User(Serializable):

    def __init__(self, username, fullname, country_id, city_name, email, passwd):
        self.username = username  # varchar(30)
        self.fullname = fullname  # varchar(255)
        self.country_id = country_id  # int
        self.city_name = city_name  # varchar(255)
        self.email = email  # varchar(255)
        self.passwd = passwd  # varchar(255)


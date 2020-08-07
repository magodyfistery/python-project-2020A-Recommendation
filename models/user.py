class User:

    def __init__(self, username, fullname, city, email, passwd):
        self.username = username  # varchar(30)
        self.fullname = fullname  # varchar(255)
        self.city = city  # varchar(255)
        self.email = email  # varchar(255)
        self.passwd = passwd  # varchar(255)

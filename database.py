import pymysql


class Database:

    connection = None

    @staticmethod
    def getConnection():

        # Patrón Singleton
        if Database.connection is None:
            Database.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='shop',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

        return Database.connection

    def __del__(self):
        Database.connection.close()

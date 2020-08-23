from models.serializable import Serializable


class Order(Serializable):

    def __init__(self, id_order, username_user, order_date, total):
        self.id_order = id_order  # int
        self.username_user = username_user  # varchar(30)
        self.order_date = order_date  # string of Date
        self.total = total  # float(10, 2)

    @staticmethod    
    def insert_order(connection, order):
        cursor = connection.cursor()
        sql = "insert into orders values (0,'{username}','{order_date}',{total})".format(username=order.username_user,order_date=str(order.order_date),total=order.total)
        try:
            cursor.execute(sql)
            connection.commit()
            return True
        except Exception as e:
            print(__name__, "insert_order: " + str(e))
            return None




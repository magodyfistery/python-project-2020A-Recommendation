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

    @staticmethod
    def select_ten_last_days(connection):

        cursor = connection.cursor()
        sql = "SELECT Date(order_date) as odate, SUM(total) as total  "
        sql += "FROM orders as o GROUP BY Date(order_date) ORDER BY order_date DESC LIMIT 10"


        try:
            cursor.execute(sql)
            labels = []
            values = []
            fetch = cursor.fetchall()
            for product in fetch:
                labels.append(str(product['odate']))
                values.append(product['total'])
            return labels, values
        except Exception as e:
            print(__name__, "query: " + str(e))
            return [], []



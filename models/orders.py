from models.serializable import Serializable


class Order(Serializable):

    def __init__(self, id_order, username_user, order_date, total):
        self.id_order = id_order  # int
        self.username_user = username_user  # varchar(30)
        self.order_date = order_date  # string of Date
        self.total = total  # float(10, 2)
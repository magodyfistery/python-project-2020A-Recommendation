from models.serializable import Serializable


class OrderDetails(Serializable):

    def __init__(self, detail_number, id_order, id_product, quantity, subtotal):
        self.detail_number = detail_number  # int
        self.id_order = id_order  # int
        self.id_product = id_product  # int
        self.quantity = quantity  # int
        self.subtotal = subtotal  # float(10, 2)

from models.serializable import Serializable


class Cart(Serializable):

    def __init__(self,id_product,product_name,quantity,price,total):
        self.id_product=id_product
        self.product_name=product_name
        self.quantity=quantity
        self.price=price
        self.total=total

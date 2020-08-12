from models.serializable import Serializable


class UserProductRating(Serializable):

    def __init__(self, username_user, id_product, rating, id_processing_status):
        self.username_user = username_user
        self.id_product = id_product
        self.rating = rating
        self.id_processing_status = id_processing_status
    @staticmethod
    def insert_product_notrated(connection, userproductrating):
        cursor = connection.cursor()
        sql1 = "select * from user_product_rating where username_user='{user}' and id_product={id_product}".format(user=userproductrating.username_user,id_product=userproductrating.id_product)
        try:
            cursor.execute(sql1)
            rating = cursor.fetchone()
            if not rating:
                sql2 = "INSERT INTO user_product_rating VALUES ('{user}',{id_product},NULL,0)".format(user=userproductrating.username_user,id_product=userproductrating.id_product)
                try:
                    cursor.execute(sql2)
                    connection.commit()
                    return True
                except Exception as e:
                    print(__name__, "insert_product_notrated: " + str(e))
                    return None
        except Exception as e:
                print(__name__, "insert_product_notrated: " + str(e))
                return None
    @staticmethod
    def insert_product_rated(connection, userproductrating):
        cursor = connection.cursor()
        sql = "UPDATE user_product_rating SET rating={rating} WHERE id_product={id_product} and username_user='{user}'".format(user=userproductrating.username_user,id_product=userproductrating.id_product,rating=float(userproductrating.rating))
        try:
            cursor.execute(sql)
            connection.commit()
            return True
        except Exception as e:
            print(__name__, "insert_product_rated: " + str(e))
            return None
    
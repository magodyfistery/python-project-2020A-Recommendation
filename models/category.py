from models.serializable import Serializable


class Category(Serializable):

    def __init__(self, id_category, category_name, info):
        self.id_category = id_category  # int
        self.category_name = category_name  # varchar(255)
        self.info = info  # varchar(255)

    # read
    @staticmethod
    def select_categories(connection):
        cursor = connection.cursor()
        sql = "SELECT * FROM category"

        try:
            cursor.execute(sql)
            categories = []
            fetch = cursor.fetchall()

            for category in fetch:
                categories.append(Category(
                    category['id_category'],
                    category['category_name'],
                    category['info']
                ))

            return categories
        except Exception as e:
            print(__name__, "select_categories: ", "ERROR: " + str(e))
            return None
    @staticmethod
    def get_user_top_category(connection,username):
        cursor = connection.cursor()
        q1 = "select id_product from order_details where id_order in (select id_order from orders where username_user='{username}') group by id_product order by sum(quantity) desc limit 1".format(username=username)

        try:
            ###Simplificar a un solo query cuando cambie de versión de base de datos###
            cursor.execute(q1)
            fetch = cursor.fetchone()
            id_product = fetch['id_product']
            q2 = "select id_category from product where id_product={id_product}".format(id_product=id_product)
            cursor.execute(q2)
            fetch = cursor.fetchone()
            id_category = fetch['id_category']
            q3 = "select * from category where id_category={id}".format(id=id_category)
            cursor.execute(q3)
            cat = cursor.fetchone()
            return Category(cat['id_category'],cat['category_name'],cat['info'])

        except Exception as e:
            print(__name__, "get_user_top_category", "ERROR: " + str(e))
            return None
    

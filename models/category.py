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

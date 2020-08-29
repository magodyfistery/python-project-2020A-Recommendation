class News:

    def __init__(self, id, author_user, publish_date, title, description, url, content_html, id_news_category):
        self.id = id  # int
        self.author_user = author_user  # varchar(30)
        self.publish_date = publish_date  # date
        self.title = title  # varchar(30)
        self.description = description  # varchar(140)
        self.url = url  # text
        self.content_html = content_html  # text
        self.id_news_category = id_news_category  # int

    @staticmethod
    def get_news_from_date(connection, from_date):
        # '2020-08-28'
        cursor = connection.cursor()
        sql = "SELECT * FROM `news` WHERE Date(publish_date) >= '{from_date}'".format(from_date=from_date)
        print("SQL", sql)
        try:
            cursor.execute(sql)
            news = []
            fetch = cursor.fetchall()
            for new in fetch:
                news.append(News(
                    new['id'],
                    new['author_user'],
                    new['publish_date'],
                    new['title'],
                    new['description'],
                    new['url'],
                    new['content_html'],
                    new['id_news_category']
                ))
            return news

        except Exception as e:
            print(__name__, "get_news_from_date: ", "ERROR: " + str(e))
            return []

    @staticmethod
    def get_recommended_news(connection, from_date, username_user):
        # '2020-08-28'
        cursor = connection.cursor()
        sql = "SELECT n.id_news_category as id_news_category FROM user_view_news as uv, news as n "
        sql += "WHERE uv.id_news=n.id AND uv.username_user='{username_user}'"
        sql += "GROUP BY n.id_news_category ORDER BY COUNT(n.id_news_category) DESC"

        sql = sql.format(username_user=username_user)

        print("1: SQL", sql)
        try:
            cursor.execute(sql)
            fetch = cursor.fetchall()

            sql_news_recommended = "SELECT n.* FROM news as n "
            sql_news_recommended += "WHERE Date(publish_date) >= '{from_date}' ORDER BY field(n.id_news_category".format(from_date=from_date)

            for category in fetch:
                sql_news_recommended += ", " + str(category['id_news_category'])

            sql_news_recommended += ")"
            print("2: SQL news", sql_news_recommended)

            try:
                cursor.execute(sql_news_recommended)
                fetch_news = cursor.fetchall()
                news = []
                for new in fetch_news:
                    news.append(News(
                        new['id'],
                        new['author_user'],
                        new['publish_date'],
                        new['title'],
                        new['description'],
                        new['url'],
                        new['content_html'],
                        new['id_news_category']
                    ))

                return news

            except Exception as e:
                print(__name__, "get_recommended_news: Part2: ", "ERROR: " + str(e))
                return []

        except Exception as e:
            print(__name__, "get_recommended_news: Part1: ", "ERROR: " + str(e))
            return []

    @staticmethod
    def add_interact_with_user(connection, id_news, username_user):

        cursor = connection.cursor()
        sql = "INSERT INTO user_view_news(id_news, username_user) "
        sql += "VALUES({id_news}, '{username_user}')".format(id_news=id_news, username_user=username_user)
        print("SQL", sql)
        try:
            cursor.execute(sql)
            connection.commit()
            return True

        except Exception as e:
            print(__name__, "add_interact_with_user: ", "ERROR: " + str(e))
            return False


    @staticmethod
    def select_news(connection, skip, step):
        cursor = connection.cursor()
        sql = "SELECT * FROM news LIMIT {skip}, {step}".format(skip=skip, step=step)
        try:
            cursor.execute(sql)
            news = []
            fetch = cursor.fetchall()
            for new in fetch:
                news.append(News(
                    new['id'],
                    new['author_user'],
                    new['publish_date'],
                    new['title'],
                    new['description'],
                    new['url'],
                    new['content_html'],
                    new['id_news_category']
                ))
            return news
        except Exception as e:
            print(__name__, "select_news: " + str(e))
            return []







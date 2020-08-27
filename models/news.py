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






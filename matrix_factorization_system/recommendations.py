
import pandas as pd

from database import Database
from utils.similarity_measures import *
from utils.console_functions import log
import pickle
import os

from matrix_factorization_system.config import Config



def user_candidate_generation(user_id, label_user_id, label_item_id, measure='score', with_rated = False, k=100):

    conf = Config()


    if os.path.isfile(conf.model_path):  # si existe el modelo
        print('Loading existing data for {} model'.format(conf.data_name))
        with open(conf.model_path, 'rb') as handle:
            conf = pickle.load(handle)
            model = conf.cf_model
            id_items = conf.id_items
            print("La funcion de costo del modelo es", model.minimum_test_loss)
            print("Los productos con que se entrenó el modelo son", id_items)

            print("Embedings", len(model.embeddings[label_user_id]))

            scores = None
            try:
                scores = dot_product_with_norms_controlled(
                      model.embeddings[label_user_id][user_id-1], model.embeddings[label_item_id].T
                )
            except IndexError as e:
                # no hay recomendaciones para ese usuario
                return []

            # log(' model.embeddings["id"][user_id]', model.embeddings["id"][user_id])
            # log('model.embeddings["id_product"]', model.embeddings["id_product"])
            score_key = measure

            # log("scores", scores)

            df = pd.DataFrame({
                score_key: list(scores),
                'product_id': list(range(len(scores)))
            })
            # print(df.head())

            """
            todo: excluse rates
            if not with_rated:
              # remove items that are already rated
              rated_items = ratings[ratings.user_id == user_id-1][item_id].values
              df = df[df.product_id.apply(lambda item_id: item_id not in rated_movies)]
              """

            top_reccomendations = df.sort_values([score_key], ascending=False)
            log("top_reccomendations", top_reccomendations.head(k))
            return list(map(lambda x: x + 1, top_reccomendations["product_id"].values))

    else:
        print("No hay un modelo entrenado para predecir")
        return []



def get_total_sources(candidates, user_id, with_rated=False, verbosity=1):


    extra_ponderation = len(candidates)/4

    connection = Database.getConnection()
    sql_catalog = "SELECT p.id_product, p.id_category, p.price FROM product as p"

    sql_popular_products = "SELECT p.id_product FROM product as p ORDER BY avgrating DESC limit 5"

    sql_best_seller_products = "SELECT p.id_product FROM order_details as o, product as p "
    sql_best_seller_products += "WHERE p.id_product=o.id_product GROUP BY id_product ORDER BY SUM(quantity) DESC LIMIT 5"


    catalog_products = pd.read_sql(sql_catalog, connection, index_col="id_product")
    catalog_products["score"] = [0 for v in range(len(catalog_products.iloc[:, 0]))[::-1]]



    for index, id in enumerate(candidates[::-1]):
        catalog_products.loc[id, :] = index + 1



    # other sources
    popular_products = pd.read_sql(sql_popular_products, connection)['id_product'].values
    best_seller_products = pd.read_sql(sql_best_seller_products, connection)['id_product'].values



    already_rated = []
    if not with_rated:
        already_rated = pd.read_sql("SELECT id_product FROM user_product_rating, user WHERE username_user=user.username AND user.id={}".format(user_id), connection)['id_product'].values


    if verbosity == 1:
        log("catalog_products", catalog_products)
        log("popular_products", popular_products)
        log("best_seller_products", best_seller_products)


    for id in popular_products:

        if id not in already_rated:
            if id not in candidates:
                catalog_products.loc[id, :] += extra_ponderation/2
            else:
                catalog_products.loc[id, :] += extra_ponderation  # doble aprobación

    for id in best_seller_products:

        if id not in already_rated:
            if id not in candidates:
                catalog_products.loc[id, :] += extra_ponderation/2
            else:
                catalog_products.loc[id, :] += extra_ponderation  # doble aprobación

    if verbosity == 1:
        log("catalog_products", catalog_products.sort_values(["score"], ascending=False))

    return catalog_products.sort_values(["score"], ascending=False)



def get_sparse_matrix_ratings():
    connection = Database.getConnection()

    sql = "SELECT u.id, r.id_product, r.rating FROM user_product_rating as r, user as u WHERE u.username = r.username_user AND id_processing_status=1"


    ratings = pd.read_sql(sql, connection)
    users_count = int(np.max(ratings['id']))  # se le redujo 1
    items_count = int(np.max(ratings['id_product']))

    sparse_matrix = [[0 for _ in range(items_count)] for _ in range(users_count)]

    print(ratings)


    for index in range(len(ratings['id'].values)):
        i = ratings.loc[index, 'id'] - 1
        j = ratings.loc[index, 'id_product'] - 1
        sparse_matrix[i][j] = ratings.loc[index, 'rating']

    print("Rating sparse matrix")
    for i in range(len(sparse_matrix)):
        for j in range(len(sparse_matrix[0])):
            print("%.1f" % sparse_matrix[i][j], end="    ")
        print()

    return sparse_matrix

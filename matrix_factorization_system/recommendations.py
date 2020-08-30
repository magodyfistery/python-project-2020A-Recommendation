
import pandas as pd
import numpy as np
from flask import jsonify

from database import Database
from models.product import Product
from models.city import City
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
    sql_catalog = "SELECT p.* FROM product as p"

    sql_popular_products = "SELECT p.id_product FROM product as p ORDER BY avgrating DESC limit 5"

    sql_best_seller_products = "SELECT p.id_product FROM order_details as o, product as p "
    sql_best_seller_products += "WHERE p.id_product=o.id_product GROUP BY id_product ORDER BY SUM(quantity) DESC LIMIT 5"


    catalog_products = pd.read_sql(sql_catalog, connection, index_col="id_product")
    catalog_products["score"] = [0 for v in range(len(catalog_products.iloc[:, 0]))[::-1]]



    for index, id in enumerate(candidates[::-1]):
        catalog_products.loc[id, 'score'] = index + 1



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
                catalog_products.loc[id, 'score'] += extra_ponderation/2
            else:
                catalog_products.loc[id, 'score'] += extra_ponderation  # doble aprobación

    for id in best_seller_products:

        if id not in already_rated:
            if id not in candidates:
                catalog_products.loc[id, 'score'] += extra_ponderation/2
            else:
                catalog_products.loc[id, 'score'] += extra_ponderation  # doble aprobación

    if verbosity == 1:
        log("catalog_products", catalog_products.sort_values(["score"], ascending=False))


    df = catalog_products.sort_values(["score"], ascending=False)

    products = []
    for index in df.index:
        products.append(Product(
            index,
            int(df.loc[index, 'id_category']),
            str(df.loc[index, 'product_name']),
            float(df.loc[index, 'price']),
            str(df.loc[index, 'img_path']),
            float(df.loc[index, 'avgrating'])
        ))

    return products



def get_sparse_matrix_ratings():
    connection = Database.getConnection()

    sql = "SELECT u.id, r.id_product, r.rating FROM user_product_rating as r, user as u WHERE u.username = r.username_user"


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
    #Asumiendo que los productos siempre estarán en orden de id y que no habrá brecha entre id's.
    #Uso un diccionario de estilo {'user_id1':[],'user_id2':[]}
    b = {}
    i=1
    for item in sparse_matrix:
        b[str(i)]=item
        i += 1

    return b

def grs(user_id):
    allusers = get_sparse_matrix_ratings()
    print('####INICIO########')
    print(allusers)
    connection = Database.getConnection()
    cities = City.select_user_cities(connection)
    user_cities = City.select_alluser_cities(connection)  # [[user_id,user_city_name],...]
    groups = {c:{} for c in cities}
    for city in cities:
        for item in user_cities:
            if item.name == city:
                groups[city][str(item.id_country)]=allusers[str(item.id_country)]
    print(groups)
    city = City.check_user_city(connection,user_id)
    if city:
        grupo = groups[city]
        #Aditive Utilitarian Strategy
        print("#########ADITIVE#######")
        suma = np.zeros(len(grupo[str(user_id)]))# Si pasa el check_user_city, user_id existe en grupo
        for k,v in grupo.items():
            suma = suma + v
        print(suma)
        print(-np.sort(-(np.argpartition(suma,-6)[-6:]+1)))
        suma = (-np.sort(-(np.argpartition(suma,-6)[-6:]+1)))
        #Multiplicative Utilitarian Strategy
        print("#########MULTIPLICATIVE#######")
        mult = np.ones(len(grupo[str(user_id)]))
        for k,v in grupo.items():
            varr = np.array(v)
            varr[varr==0]=1
            mult = mult * varr
        print(mult)
        print(-np.sort(-(np.argpartition(mult,-3)[-3:]+1)))
        mult = (-np.sort(-(np.argpartition(mult,-3)[-3:]+1)))
        #Least Misery Strategy
        print("#########LEAST MISERY#######")
        least = np.array(grupo[str(user_id)])
        least[least==0]=1
        for k,v in grupo.items():
            varr = np.array(v)
            varr[varr==0]=1
            i=0
            for x in least:
                if varr[i]<=x:
                    least[i]=varr[i]
                i+=1
        print(least)
        print(-np.sort(-(np.argpartition(least,-3)[-3:]+1)))
        least = (-np.sort(-(np.argpartition(least,-3)[-3:]+1)))
        #Most Pleasure
        print("#########MOST PLEASURE#######")
        most = np.array(grupo[str(user_id)])
        for k,v in grupo.items():
            varr = np.array(v)
            i=0
            for x in most:
                if varr[i]>x:
                    most[i]=varr[i]
                i+=1
        print(most)
        print(-np.sort(-(np.argpartition(most,-3)[-3:]+1)))
        most = (-np.sort(-(np.argpartition(most,-3)[-3:]+1)))
        recommendations = []
        if np.in1d(mult,most).any():
            for x in suma:
                recommendations.append(Product.get_product(connection,x))
        else:
            for x in mult:
                recommendations.append(Product.get_product(connection,x))
            for y in most:
                recommendations.append(Product.get_product(connection,y))
        return recommendations
    else:
        return None
    
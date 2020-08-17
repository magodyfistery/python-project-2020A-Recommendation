
import pandas as pd
from utils.similarity_measures import *
from utils.console_functions import log
import numpy as np
import pickle
import os

from matrix_factorization_system.config import Config

def user_recommendations(user_id, label_user_id, label_item_id, measure='score', exclude_rated=False, k=6):

    conf = Config()


    if os.path.isfile(conf.model_path):  # si existe el modelo
        print('Loading existing data for {} model'.format(conf.data_name))
        with open(conf.model_path, 'rb') as handle:
            conf = pickle.load(handle)
            model = conf.cf_model
            id_items = conf.id_items
            print("La funcion de costo del modelo es", model.minimum_test_loss)
            print("Los productos con que se entrenó el modelo son", id_items)

            scores = dot_product_with_norms_controlled(
                  model.embeddings[label_user_id][user_id-1], model.embeddings[label_item_id].T
            )

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
            if exclude_rated:
              # remove items that are already rated
              rated_movies = ratings[ratings.user_id == user_id-1][item_id].values
              df = df[df.product_id.apply(lambda item_id: item_id not in rated_movies)]
              """

            top_reccomendations = df.sort_values([score_key], ascending=False)
            log("top_reccomendations", top_reccomendations.head(k))
            return list(map(lambda x: x + 1, top_reccomendations["product_id"].values))

    else:
        print("No hay un modelo entrenado para predecir")
        return []

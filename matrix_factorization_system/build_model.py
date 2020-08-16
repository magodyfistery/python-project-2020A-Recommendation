from tensorflow import float32
from tensorflow._api.v1 import random
from tensorflow.python import Variable
from tensorflow import executing_eagerly, enable_eager_execution

from database import Database
import pandas as pd
import numpy as np

from matrix_factorization_system.CFModel import *
from utils.console_functions import log
from utils.pandas_utils import split_dataframe
from utils.tf_utils import build_rating_sparse_tensor
from utils.similarity_measures import *

enable_eager_execution()


def build_model(ratings, users_count, items_count, embedding_dim=3, init_stddev=1.):
        """
        Args:
        ratings: a DataFrame of the ratings
        embedding_dim: the dimension of the embedding vectors.
        init_stddev: float, the standard deviation of the random initial embeddings.
        Returns:
        model: a CFModel.
        """
        # Split the ratings DataFrame into train and test.
        train_ratings, test_ratings = split_dataframe(ratings)

        log("train_ratings", train_ratings.head())
        log("test_ratings", test_ratings.head())

        # SparseTensor representation of the train and test datasets.
        # Its for optimization
        Matrix_A_train = build_rating_sparse_tensor(train_ratings, 'id', 'id_product', 'rating', users_count, items_count)
        Matrix_A_test = build_rating_sparse_tensor(test_ratings, 'id', 'id_product', 'rating', users_count, items_count)

        log("build_rating_sparse_tensor(train_ratings)", Matrix_A_train)
        log("build_rating_sparse_tensor(test_ratings)", Matrix_A_test)

        cambiarMatrizReferencia(Matrix_A_train)

        # Initialize the embeddings using a normal distribution.

        U = Variable(random.normal(
          [Matrix_A_train.dense_shape[0], embedding_dim], stddev=init_stddev), dtype=float32)  # stddev indicará que tan dispersos estarán los datos
        V = Variable(random.normal(
          [Matrix_A_train.dense_shape[1], embedding_dim], stddev=init_stddev), dtype=float32)  # mientras más alto estarán más dispersos

        log("Users init", U)
        log("Items init", V)

        train_loss = sparse_mean_square_error(U, V)
        test_loss = sparse_mean_square_error(U, V)

        log("train_loss", train_loss)
        log("test_loss", test_loss)

        metrics = {
          'train_error': train_loss,
          'test_error': test_loss
        }
        embeddings = {
          "id": U,
          "id_product": V
        }
        return Matrix_A_test, CFModel(embeddings, train_loss, [metrics])


def user_recommendations(model, user_id, products, measure='score', exclude_rated=False, k=6):

    scores = dot_product_with_norms_controlled(
          model.embeddings["id"][user_id], model.embeddings["id_product"].T
    )

    # log(' model.embeddings["id"][user_id]', model.embeddings["id"][user_id])
    # log('model.embeddings["id_product"]', model.embeddings["id_product"])
    score_key = measure

    log("scores", scores)


    df = pd.DataFrame({
        score_key: list(scores),
        'product_id': list(range(len(scores)))
    })
    print(df.head())

    """
    if exclude_rated:
      # remove movies that are already rated
      rated_movies = ratings[ratings.user_id == "943"]["movie_id"].values
      df = df[df.product_id.apply(lambda item_id: item_id not in rated_movies)]
      """
    print(df.sort_values([score_key], ascending=False).head(k))







connection = Database.getConnection()

sql = "SELECT u.id, r.id_product, r.rating FROM user_product_rating as r, user as u WHERE u.username = r.username_user AND id_processing_status=1"

try:
    ratings = pd.read_sql(sql, connection)

    ratings["id_product"] = ratings["id_product"].apply(lambda x: str(x-1))
    ratings["id"] = ratings["id"].apply(lambda x: str(x-1))  # se reduce para indexar más facilmente desde el 0
    ratings["rating"] = ratings["rating"].apply(lambda x: float(x))

    users_count = int(np.max(ratings['id'])) + 1  # se le redujo 1
    items_count = int(np.max(ratings['id_product'])) + 1

    # Build the CF model and train it.
    Matrix_A_test, model = build_model(ratings, users_count, items_count,
                                       embedding_dim=35, init_stddev=0.1)  # embedding_dim=30  num_iterations=1000
    U, V = model.train(num_iterations=1000, learning_rate=0.03)

    cambiarMatrizReferencia(Matrix_A_test)

    model.minimum_test_loss = sparse_mean_square_error(U, V)

    log("test_loss obtenido", model.minimum_test_loss)

    user_recommendations(model, 1, ratings["id_product"])













except Exception as e:

    raise e


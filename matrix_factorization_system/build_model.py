from tensorflow import float32
from tensorflow._api.v1 import random
from tensorflow.python import Variable
from tensorflow import enable_eager_execution

from database import Database
import pandas as pd
import pickle
import os

from matrix_factorization_system.CFModel import *
from utils.console_functions import log
from utils.pandas_utils import split_dataframe
from utils.tf_utils import build_rating_sparse_tensor
from matrix_factorization_system.config import Config

enable_eager_execution()


def build_model(ratings, users_count, items_count, embedding_dim=3, init_stddev=1., verbosity=1):
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

    if verbosity == 1:
        log("train_ratings", train_ratings.head())
        log("test_ratings", test_ratings.head())

    # SparseTensor representation of the train and test datasets.
    # Its for optimization
    Matrix_A_train = build_rating_sparse_tensor(train_ratings, 'id', 'id_product', 'rating', users_count, items_count)
    Matrix_A_test = build_rating_sparse_tensor(test_ratings, 'id', 'id_product', 'rating', users_count, items_count)

    if verbosity == 1:
        log("build_rating_sparse_tensor(train_ratings)", Matrix_A_train)
        log("build_rating_sparse_tensor(test_ratings)", Matrix_A_test)

    cambiarMatrizReferencia(Matrix_A_train)

    # Initialize the embeddings using a normal distribution.

    U = Variable(random.normal(
      [Matrix_A_train.dense_shape[0], embedding_dim], stddev=init_stddev), dtype=float32)  # stddev indicará que tan dispersos estarán los datos
    V = Variable(random.normal(
      [Matrix_A_train.dense_shape[1], embedding_dim], stddev=init_stddev), dtype=float32)  # mientras más alto estarán más dispersos

    if verbosity == 1:
        log("Users init", U)
        log("Items init", V)

    train_loss = sparse_mean_square_error(U, V)
    test_loss = sparse_mean_square_error(U, V)

    if verbosity == 1:
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


def save_model(model, ratings):
    """

    :param model:
    :param ratings:
    """
    print("Guardando nuevo modelo...")
    global conf
    conf.cf_model = model
    conf.id_items = ratings["id_product"]
    conf.id_users = ratings["id"]
    print(conf, type(conf))
    with open(conf.model_path, 'wb') as handle:
        pickle.dump(conf, handle, protocol=pickle.HIGHEST_PROTOCOL)


conf = Config()


def generateModel(embedding_dim=30, init_stddev=1, num_iterations=500, learning_rate=0.03, verbosity=1):
    """

    :param embedding_dim:
    :param init_stddev:
    :param num_iterations:
    :param learning_rate:
    :param verbosity:
    """
    last_loss_result = math.inf

    if os.path.isfile(conf.model_path):  # si existe el modelo
        # print('Loading existing data for {} model'.format(conf.data_name))
        with open(conf.model_path, 'rb') as handle:
            last_loss_result = pickle.load(handle).cf_model.minimum_test_loss
            # print("Anterior costo mínimo ", last_loss_result)

    connection = Database.getConnection()

    sql = "SELECT u.id, r.id_product, r.rating FROM user_product_rating as r, user as u WHERE u.username = r.username_user"

    try:
        ratings = pd.read_sql(sql, connection)

        ratings["id_product"] = ratings["id_product"].apply(lambda x: str(x-1))
        ratings["id"] = ratings["id"].apply(lambda x: str(x-1))  # se reduce para indexar más facilmente desde el 0
        ratings["rating"] = ratings["rating"].apply(lambda x: float(x))

        users_count = int(np.max(ratings['id'])) + 1  # se le redujo 1
        items_count = int(np.max(ratings['id_product'])) + 1

        # Build the CF model and train it.
        Matrix_A_test, model = build_model(ratings, users_count, items_count, embedding_dim=embedding_dim, init_stddev=init_stddev, verbosity=verbosity)  # embedding_dim=30  num_iterations=1000
        U, V = model.train(num_iterations=num_iterations, learning_rate=learning_rate, verbosity=verbosity)

        # El error se mide con una matriz de test que no ha sido mostrada al modelo
        cambiarMatrizReferencia(Matrix_A_test)

        model.minimum_test_loss = sparse_mean_square_error(U, V)
        if verbosity == 1:
            log("test_loss final obtenido", model.minimum_test_loss)

        save_model(model, ratings)

        """
        if last_loss_result == math.inf:
            save_model(model, ratings)
        else:
            if model.minimum_test_loss < last_loss_result:
                # print("El modelo mejoró por un ", ((last_loss_result-model.minimum_test_loss)*100)/last_loss_result, " % respecto al minimo inicial")
                save_model(model, ratings)
            # else:
                # print("El modelo empeoró un ", ((model.minimum_test_loss-last_loss_result)*100)/last_loss_result, " % respecto al minimo inicial")
        """
    except Exception as e:
        raise e

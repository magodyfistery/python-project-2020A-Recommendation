from tensorflow.contrib.losses import mean_squared_error

from utils.console_functions import get_summary_df, log
import tensorflow as tf
from tqdm import tqdm
import math
import numpy as np

"""
Se toma la recomendación para un usuario cualquiera
El modelo falta ser optimizado por las acotaciones de google
el learning rate y la desviación estandoar junto a la función de error pueden
ser mejoradas pero en general da buenas recomendaciones
"""
sparse_ratings = None


def cambiarMatrizReferencia(A):
    global sparse_ratings
    sparse_ratings = A


class CFModel(object):

  """Simple class that represents a collaborative filtering model"""

  def __init__(self, embedding_vars, loss, metrics=None):
    """Initializes a CFModel.
    Args:
      embedding_vars: A dictionary of tf.Variables.
      loss: A float Tensor. The loss to optimize.
      metrics: optional list of dictionaries of Tensors. The metrics in each
        dictionary will be plotted in a separate figure during training.
    """
    self._embedding_vars = embedding_vars
    self._loss = loss
    self._metrics = metrics
    self._session = None
    self._embeddings = {k: None for k in embedding_vars}
    self.minimum_test_loss = None


  @property
  def embeddings(self):
    """The embeddings dictionary."""
    return self._embeddings

  def train(self, num_iterations=100, learning_rate=1.0, plot_results=True,
            optimizer=tf.keras.optimizers.SGD, verbosity=1):  # tf.keras.optimizers.SGD() tensorflow 2 = tf.train.GradientDescentOptimizer  tensorflow 1
    """Trains the model.
    Args:
      iterations: number of iterations to run.
      learning_rate: optimizer learning rate.
      plot_results: whether to plot the results at the end of training.
      optimizer: the optimizer to use. Default to GradientDescentOptimizer.
    Returns:
      The metrics dictionary evaluated at the last iteration.
    """

    U = self._embedding_vars['id']
    V = self._embedding_vars['id_product']
    opt = optimizer(learning_rate=learning_rate)
    var_list = [U, V]
    loss_fn = lambda: sparse_mean_square_error(U, V)
    # log("opt", opt)
    # log("self._loss", loss_fn)
    # log("var_list", var_list)


    # Train and append results.
    for i in tqdm(range(num_iterations + 1)):  # tqdm(range(num_iterations + 1))
        opt.minimize(loss_fn, var_list)
        if (i % 100 == 0 or i == num_iterations) and verbosity == 1:
            log("Training error in iteration %i" % i, sparse_mean_square_error(U, V))

    for k, v in self._embedding_vars.items():
        self._embeddings[k] = v.numpy()
        """log("k", k)
        log("v", v)"""



    return U, V

  def predict(self, user_embeddings, movie_embeddings):


    return tf.matmul(user_embeddings, movie_embeddings, transpose_b=True)


def sparse_mean_square_error(user_embeddings, item_embeddings):
    """
    Args:
    sparse_ratings: A SparseTensor rating matrix, of dense_shape [N, M]
    user_embeddings: A dense Tensor U of shape [N, k] where k is the embedding
      dimension, such that U_i is the embedding of user i.
    item_embeddings: A dense Tensor V of shape [M, k] where k is the embedding
      dimension, such that V_j is the embedding of item j.
    Returns:
    A scalar Tensor representing the MSE between the true ratings and the
      model's predictions.





    predictions = tf.reduce_sum(
      tf.gather(user_embeddings, sparse_ratings.indices[:, 0]) *
      tf.gather(item_embeddings, sparse_ratings.indices[:, 1]),
      axis=1)

    loss = tf.reduce_sum(tf.add(sparse_ratings.values, - predictions) ** 2) / predictions.shape[0]  # mean squared error
    return loss
    """

    global sparse_ratings

    predictions = tf.reduce_sum(  # de los indices usuario movie creatods, los usa para obtener de los datos verdaderos
      tf.gather(user_embeddings, sparse_ratings.indices[:, 0]) *
      tf.gather(item_embeddings, sparse_ratings.indices[:, 1]),
      axis=1)

    loss = tf.reduce_sum(tf.add(sparse_ratings.values, - predictions) ** 2) / tf.cast(predictions.shape[0], tf.float32)  # mean squared error
    return loss

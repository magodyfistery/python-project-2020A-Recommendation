from tensorflow import SparseTensor


def build_rating_sparse_tensor(ratings_df,
                               user_label,
                               item_label,
                               rating_label,
                               users_len,
                               items_len):
    """ ESTA ES LA MATRIZ A a predecir
    Simplifica una enorme matriz en una notación inteligente
    Args:
    ratings_df: a pd.DataFrame with `user_id`, `item_id` and `rating` columns.
    Returns:
    a tf.SparseTensor representing the ratings matrix.
    """
    indices = ratings_df[[user_label, item_label]].values
    values = ratings_df[rating_label].values
    return SparseTensor(
      indices=indices,
      values=values,
      dense_shape=[users_len, items_len])

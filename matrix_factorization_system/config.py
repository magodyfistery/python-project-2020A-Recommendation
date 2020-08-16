import os
from matrix_factorization_system.CFModel import *

class Config:

    def __init__(self, data_name="data"):
        self.data_name = data_name
        self.cf_model = None

        self.id_items = None

        self.model_path = os.path.join('models', data_name + '.model')

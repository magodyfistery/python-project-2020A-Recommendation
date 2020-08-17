import os

class Config:

    def __init__(self, data_name="data"):
        self.data_name = data_name
        self.cf_model = None

        self.id_items = None

        self.model_path = os.path.join('matrix_factorization_system\\model', data_name + '.model')

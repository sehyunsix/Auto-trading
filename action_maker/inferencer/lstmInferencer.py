
from sklearn.preprocessing import StandardScaler, MinMaxScaler



class LSTMInferencer:
    def __init__(self, model):
        self.model = modelz
        self.scaler = MinMaxScaler()


    def predict(self, data):
        return self.model.predict(data)

    def save(self, path)
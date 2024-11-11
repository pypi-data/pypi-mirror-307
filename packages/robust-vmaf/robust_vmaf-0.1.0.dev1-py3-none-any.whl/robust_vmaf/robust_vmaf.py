from importlib import resources
import pickle

from robust_vmaf.common.model import Model


DEFAULT_MODEL_PATH = resources.path('robust_vmaf.models', 'base_neg_model.pkl')

def load_model(path):
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model


class RobustVMAF:
    def __init__(self, model_path=DEFAULT_MODEL_PATH):
        self.model = load_model(model_path)

    def predict(self, reference_path, distorted_path, pool_results=True, return_vmaf=True, return_vmaf_neg=True):
        return self.model.predict(reference_path, distorted_path, pool_results, return_vmaf, return_vmaf_neg)

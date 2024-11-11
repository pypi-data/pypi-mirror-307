import numpy as np

from sklearn.preprocessing import StandardScaler

from robust_vmaf.common.extractor import extract_features
from robust_vmaf.common.utils import get_baseline_predictions, get_raw_features


class Model:
    def __init__(self, predictor, use_vmaf_neg):
        self.predictor = predictor
        self.use_vmaf_neg = use_vmaf_neg

        self.feature_to_idx = None
        self.scaler = None

    def predict(self, ref, dist, pool=True, return_vmaf=True, return_vmaf_neg=True):
        data = extract_features(ref, dist, use_vmaf_neg=self.use_vmaf_neg, use_cached=True)
        X_raw = []
        baselines = []
        for features in data:
            X_raw.append(get_raw_features(features, self.feature_to_idx))
            baselines.append(get_baseline_predictions(features, self.use_vmaf_neg))
        X_raw = self.scaler.transform(X_raw).astype(np.float32)
        corrections = self.predictor.predict(X_raw)
        corrected = [baseline - correction for baseline, correction in zip(baselines, corrections)]

        results = dict()

        results["model"] = corrected
        if return_vmaf:
            results["vmaf"] = [features["vmaf"] for features in data]
        if return_vmaf_neg:
            results["vmaf_neg"] = [features["vmaf_neg"] for features in data]
        
        if pool:
            pooled_results = dict()
            for k, v in results.items():
                pooled_results[k] = sum(v) / len(v)
            return pooled_results
        else:
            return results
        return results

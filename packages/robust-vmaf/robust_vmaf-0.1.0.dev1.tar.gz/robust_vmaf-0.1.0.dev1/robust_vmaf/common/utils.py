import numpy as np


def get_baseline_predictions(features, use_vmaf_neg):
    return features['vmaf'] if not use_vmaf_neg else (features['vmaf'] + features['vmaf_neg']) / 2

def get_raw_features(features, feature_to_idx):
    raw_features = np.zeros(len(feature_to_idx), dtype=np.float32)
    for fname, fvalue in features.items():
        raw_features[feature_to_idx[fname]] = fvalue
    return raw_features

from os import pipe
import pickle
from os.path import join
from urllib import parse
from datetime import datetime
from typing import List

import pandas as pd
import numpy as np
import tldextract
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

RANDOM_SEED = 26
URL_CLASSES = {
    "Safe": 0,
    "Malicious": 1,
    "Phishing": 2,
    "Unsafe click": 3,
}
CLASSIFIER_PARAMS = {
    "n_estimators": 150,
    "n_jobs": -1,
    "random_state": RANDOM_SEED,
}


def encode_target(target: pd.Series) -> pd.Series:
    return target.replace(URL_CLASSES)


def save_model(model: Pipeline, dir_path: str) -> str:
    file_name = join(dir_path, 'model.' + str(datetime.now()))
    with open(file_name, 'wb') as f:
        pickle.dump(model, f)
    return f'Saved as {file_name}'


def load_model(file_path: str) -> Pipeline:
    with open(file_path, 'rb') as f:
        pipeline = pickle.load(f)
    return pipeline


class URLPreprocessing(BaseEstimator, TransformerMixin):
    _schemes = {'http', 'https'}
    _ohe_features = ['scheme']
    
    def __init__(self):
        self._ohe = OneHotEncoder(handle_unknown='ignore')
    
    @staticmethod
    def _validate_ip(domain: str) -> bool:
        tokens = domain.split('.')
        if len(tokens) != 4:
            return False
        for ch in tokens:
            if not ch.isdigit():
                return False
            i = int(ch)
            if i < 0 or i > 255:
                return False
        return True
    
    def _scheme_parse(self, url: str) -> str:
        scheme = parse.urlparse(url).scheme
        return scheme if scheme and scheme in self._schemes else 'other'
    
    def _extract_features(self, data: List[str]) -> pd.DataFrame:
        features = {}
        data = pd.Series(data)
        features['url_len'] = data.apply(len)
        features['scheme'] = data.apply(self._scheme_parse)
        features['digit_cnt'] = data.apply(lambda x: sum(ch.isdigit() for ch in x))
        features['domain_tokens_cnt'] = data.apply(lambda x: len(parse.urlparse(x).netloc.split('.')))
        features['ip_as_domain'] = data.apply(lambda x: self._validate_ip(tldextract.extract(x).domain))
        return pd.DataFrame(features)

    def fit(self, data: List[str], target: pd.Series = None):
        data = self._extract_features(data)
        self._ohe.fit(data[self._ohe_features])
        return self
    
    def transform(self, data: List[str], target: pd.Series = None) -> np.ndarray:
        data = self._extract_features(data)
        ohe_data = self._ohe.transform(data[self._ohe_features])
        data.drop(self._ohe_features, axis=1, inplace=True)
        data = np.column_stack([data, ohe_data.toarray()])
        return data

def create_pipeline() -> Pipeline:
    pipeline = Pipeline([
        ("preprocessing", URLPreprocessing()),
        ("classifier", RandomForestClassifier(**CLASSIFIER_PARAMS))
    ])
    return pipeline

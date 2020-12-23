from ast import literal_eval
import random
import pandas as pd
import pyarrow.lib
from collections import OrderedDict
from sherlock.features.bag_of_characters import extract_bag_of_characters_features
from sherlock.features.bag_of_words import extract_bag_of_words_features
from sherlock.features.word_embeddings import extract_word_embeddings_features
from sherlock.features.paragraph_vectors import infer_paragraph_embeddings_features


def as_py_str(x: pyarrow.lib.StringScalar):
    return x.as_py()


def to_literal(x):
    return literal_eval(x)


def randomise_sample(values):
    n_samples = 1000
    n_values = len(values)

    if n_samples > n_values:
        n_samples = n_values

    random.seed(13)
    return pd.Series(random.choices(values, k=n_samples))


def as_str_series(series: pd.Series):
    return series.astype(str)


def dropna(series: pd.Series):
    return series.dropna()


def extract_features(series: pd.Series):
    features = OrderedDict()

    extract_bag_of_characters_features(series, features)
    extract_word_embeddings_features(series, features)
    extract_bag_of_words_features(series, series.count(), features)
    infer_paragraph_embeddings_features(series, features, dim=400, reuse_model=True)

    return features


# Only return OrderedDict.values. Useful in some benchmarking scenarios.
def values_only(od: OrderedDict):
    return list(od.values())


# Eliminate serialisation overhead for return values. Useful in some benchmarking scenarios.
def black_hole(od: OrderedDict):
    return None
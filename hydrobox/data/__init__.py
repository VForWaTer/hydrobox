import os
import pandas as pd


def __read(fname):
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), fname))
    return df


def pancake():
    return __read('pan_sample.csv')


def sr():
    return __read('sample_sr')


def lr():
    return __read('sample_lr')
import numpy as np
import pandas as pd
import pytest

from cosinorage.dataloaders import AccelerometerDataLoader, ENMODataLoader


@pytest.fixture(scope="function")
def my_AccelerometerDataLoader():
    loader = AccelerometerDataLoader(input_dir_path="tests/data/full/62164/")
    loader.load_data()
    return loader


@pytest.fixture(scope="function")
def my_ENMODataLoader():
    loader = ENMODataLoader(input_file_path="tests/data/full/62164.csv")
    loader.load_data()
    return loader


def test_AccelerometerDataLoader(my_AccelerometerDataLoader, my_ENMODataLoader):
    acc_enmo_df = my_AccelerometerDataLoader.get_enmo_per_minute()
    enmo_enmo_df = my_ENMODataLoader.get_enmo_per_minute()
    # check if data frame has the correct 2 columns
    assert acc_enmo_df.shape[
               1] == 1, ("AccelerometerDataLoader() ENMO Data Frame should "
                         "have 1 column")
    # index should be timestamp
    assert acc_enmo_df.index.name == 'TIMESTAMP', "Index should be 'TIMESTAMP'"
    assert acc_enmo_df.columns[
               0] == 'ENMO', "First column name should be 'ENMO'"

    # check if timestamps are correct
    assert acc_enmo_df.index.min() == pd.Timestamp(
        '2000-01-04 00:00:00'), "Minimum POSIX date does not match"
    assert acc_enmo_df.index.max() == pd.Timestamp(
        '2000-01-08 23:59:00'), "Maximum POSIX date does not match"

    # check if timestamps are minute-level
    assert acc_enmo_df.index.second.max() == 0, ("Seconds "
                                                                    "should be 0")
    assert acc_enmo_df.index.microsecond.max() == 0, \
        ("Microseconds should "
                                                        "be 0")

    # check if difference between timestamps is 1 minute
    assert (acc_enmo_df.index.diff().total_seconds()[
            1:] == 60).all(), "Difference between timestamps should be 1 minute"

    # check if ENMO values are within the expected range
    assert acc_enmo_df['ENMO'].min() >= 0, "ENMO values should be non-negative"

    # determine overlap range of the two dataframes
    startdate = max(acc_enmo_df.index.min(),
                    enmo_enmo_df.index.min())
    enddate = min(acc_enmo_df.index.max(),
                  enmo_enmo_df.index.max())
    # check if there is overlap
    if startdate >= enddate:
        return

    acc_enmo_df = acc_enmo_df[
        (acc_enmo_df.index >= startdate) & (
                    acc_enmo_df.index <= enddate)].reset_index(drop=True)
    enmo_enmo_df = enmo_enmo_df[
        (enmo_enmo_df.index >= startdate) & (
                    enmo_enmo_df.index <= enddate)].reset_index(
        drop=True)
    assert (acc_enmo_df.index == enmo_enmo_df.index).all(), "Timestamps do not match"

    diff = acc_enmo_df['ENMO'] - enmo_enmo_df['ENMO']
    assert np.linalg.norm(diff) < 1e-14, "Minute-level ENMO values do not match"


def test_ENMODataLoader(my_ENMODataLoader):
    # check if data frame has the correct 2 columns
    assert my_ENMODataLoader.get_enmo_per_minute().shape[
               1] == 1, "ENMODataLoader() ENMO Data Frame should have 1 column"

    # index should be timestamp
    assert my_ENMODataLoader.get_enmo_per_minute().index.name == 'TIMESTAMP', "Index should be 'TIMESTAMP'"
    assert my_ENMODataLoader.get_enmo_per_minute().columns[
               0] == 'ENMO', "First column name should be 'ENMO'"

    assert my_ENMODataLoader.get_enmo_per_minute().index.min() == pd.Timestamp(
        '2000-01-03 00:00:00'), "Minimum POSIX date does not match"
    assert my_ENMODataLoader.get_enmo_per_minute().index.max() == pd.Timestamp(
        '2000-01-09 23:59:00'), "Maximum POSIX date does not match"

    # check if timestamps are minute-level
    assert my_ENMODataLoader.get_enmo_per_minute().index.second.max() == 0, "Seconds should be 0"
    assert my_ENMODataLoader.get_enmo_per_minute().index.microsecond.max() == 0, ("Microseconds should "
                                                        "be 0")

    # check if difference between timestamps is 1 minute
    assert (my_ENMODataLoader.get_enmo_per_minute().index.diff().total_seconds()[
            1:] == 60).all(), "Difference between timestamps should be 1 minute"

    # check if ENMO values are within the expected range
    assert my_ENMODataLoader.get_enmo_per_minute()[
               'ENMO'].min() >= 0, "ENMO values should be non-negative"


@pytest.fixture(scope="function")
def my_trunc_AccelerometerDataLoader():
    loader = AccelerometerDataLoader(input_dir_path="tests/data/trunc/62164/")
    loader.load_data()
    return loader


@pytest.fixture(scope="function")
def my_trunc_ENMODataLoader():
    loader = ENMODataLoader(input_file_path="tests/data/trunc/62164.csv")
    loader.load_data()
    return loader


def test_trunc_AccelerometerDataLoader(my_trunc_AccelerometerDataLoader):
    # check if dataframe is empty
    assert my_trunc_AccelerometerDataLoader.get_enmo_per_minute().shape[
               0] == 0, ("AccelerometerDataLoader() ENMO Data Frame should be "
                         "empty")


def test_trunc_ENMODataLoader(my_trunc_ENMODataLoader):
    # check if dataframe is empty
    assert my_trunc_ENMODataLoader.get_enmo_per_minute().shape[
               0] == 0, "ENMODataLoader() ENMO Data Frame should be empty"

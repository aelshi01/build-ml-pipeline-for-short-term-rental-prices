import pandas as pd
import numpy as np
import scipy.stats


def test_column_names(data: pd.DataFrame):

    expected_colums = [
        "id",
        "name",
        "host_id",
        "host_name",
        "neighbourhood_group",
        "neighbourhood",
        "latitude",
        "longitude",
        "room_type",
        "price",
        "minimum_nights",
        "number_of_reviews",
        "last_review",
        "reviews_per_month",
        "calculated_host_listings_count",
        "availability_365",
    ]

    these_columns = data.columns.values

    # This also enforces the same order
    assert list(expected_colums) == list(these_columns)


def test_neighborhood_names(data: pd.DataFrame):

    known_names = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]

    neigh = set(data['neighbourhood_group'].unique())

    # Unordered check
    assert set(known_names) == set(neigh)


def test_proper_boundaries(data: pd.DataFrame):
    """
    Test proper longitude and latitude boundaries for properties in and around NYC
    """
    idx = data['longitude'].between(-74.25, -73.50) & data['latitude'].between(40.5, 41.2)

    assert np.sum(~idx) == 0


def test_similar_neigh_distrib(data: pd.DataFrame, ref_data: pd.DataFrame, kl_threshold: float):
    """
    Apply a threshold on the KL divergence to detect if the distribution of the new data is
    significantly different than that of the reference dataset
    """
    dist1 = data['neighbourhood_group'].value_counts().sort_index()
    dist2 = ref_data['neighbourhood_group'].value_counts().sort_index()

    assert scipy.stats.entropy(dist1, dist2, base=2) < kl_threshold

def test_row_count(data: pd.DataFrame):
    """
    Counting the rows by asserting a specific range the row count must return.

    :param data: pandas data frame being passed through the function

    """
    assert 15000 < data.shape[0] < 1000000

def test_price_range(data: pd.DataFrame, min_price: float, max_price: float):
    """
    Making sure the price of a house is within the expected range for all houses, not only one.
    If one house is outside the range it will flag it up since we are using the function all() that
    will assert the condition on all prices not only one.

    :param data: pandas data frame being passed through the function
    :param min_price: float set for the minimum value a price can be
    :param max_price: float set for the maximum value a price can be

    :return: None if test pass, else will dispolay AssertionError
    """
    assert data['price'].between(min_price,max_price).all()

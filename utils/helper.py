#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/3 15:34
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   helper.py
# @Desc     :   

from numpy.random import random as random_seed, get_state, set_state
from pandas import DataFrame
from plotly.express import scatter, scatter_3d
from time import perf_counter


class Timer(object):
    """ timing code blocks using a context manager """

    def __init__(self, description: str = None, precision: int = 5):
        """ Initialise the Timer class
        :param description: the description of a timer
        :param precision: the number of decimal places to round the elapsed time
        """
        self._description: str = description
        self._precision: int = precision
        self._start: float = 0.0
        self._end: float = 0.0
        self._elapsed: float = 0.0

    def __enter__(self):
        """ Start the timer """
        self._start = perf_counter()
        print("-" * 50)
        print(f"{self._description} has started.")
        print("-" * 50)
        return self

    def __exit__(self, *args):
        """ Stop the timer and calculate the elapsed time """
        self._end = perf_counter()
        self._elapsed = self._end - self._start

    def __repr__(self):
        """ Return a string representation of the timer """
        if self._elapsed != 0.0:
            print("-" * 50)
            return f"{self._description} took {self._elapsed:.{self._precision}f} seconds."
        return f"{self._description} has NOT started."


class SeedSetter(object):
    """ Set a random seed for reproducibility. """

    def __init__(self, seed: int = 9527):
        """ Initialise the RandomSeed class with a seed. """
        self._seed = seed
        self._state_random = None

    def __enter__(self):
        """ Enter the context manager and set the random seed. """
        # Store the current state of random and Faker
        self._state_random = get_state()
        # Set the random seed for reproducibility
        random_seed(self._seed)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit the context manager and reset the random seed. """
        # Reset the random and Faker states to their original values.
        set_state(self._state_random)
        return False

    def __str__(self):
        """ Return a string representation of the random seed. """
        return f"SeedSetter with seed {self._seed}"


def scatter_2d_without_category(data: DataFrame, x_name: str, y_name: str):
    """ Get the unique categories in the target column.
    :param data: the DataFrame containing the data
    :param x_name: the name of the feature column (X)
    :param y_name: the name of the target column (Y)
    :return: a scatter plot with different colours and symbols for each category
    """
    return scatter(
        data,
        x=x_name,
        y=y_name,
        hover_data=[x_name, y_name]
    )


def scatter_2d_with_category(data: DataFrame, x_name: str, y_name: str, category: str):
    """ Get the unique categories in the target column.
    :param data: the DataFrame containing the data
    :param x_name: the name of the feature column (X)
    :param y_name: the name of the target column (Y)
    :param category: the name of the category column
    :return: a scatter plot with different colours and symbols for each category
    """
    return scatter(
        data,
        x=x_name,
        y=y_name,
        color=category,
        symbol=category,
        hover_data=[x_name, y_name, category]
    ).update_layout(coloraxis_showscale=False)


def scatter_3d_without_category(data: DataFrame, x_name: str = "PCA-X", y_name: str = "PCA-Y", z_name: str = "PCA-Z"):
    """ Get the unique categories in the target column.
    :param data: the DataFrame containing the data
    :param x_name: the name of the feature column (X), default is "PCA-X"
    :param y_name: the name of the target column (Y), default is "PCA-Y"
    :param z_name: the name of the target column (Z), default is "PCA-Z"
    :return: a scatter plot with different colours and symbols for each category
    """
    return scatter_3d(
        data,
        x=x_name,
        y=y_name,
        z=z_name,
        height=650,
        hover_data=[x_name, y_name, z_name]
    ).update_layout(coloraxis_showscale=False)


def scatter_3d_with_category(
        data: DataFrame,
        x_name: str = "PCA-X", y_name: str = "PCA-Y", z_name: str = "PCA-Z",
        category_name: str = "Cluster"
):
    """ Get the unique categories in the target column.
    :param data: the DataFrame containing the data
    :param x_name: the name of the feature column (X), default is "PCA-X"
    :param y_name: the name of the target column (Y), default is "PCA-Y"
    :param z_name: the name of the target column (Z), default is "PCA-Z"
    :param category_name: the name of the category column, default is "Cluster"
    :return: a scatter plot with different colours and symbols for each category
    """
    return scatter_3d(
        data,
        x=x_name,
        y=y_name,
        z=z_name,
        color=category_name,
        symbol=category_name,
        height=650,
        hover_data=[x_name, y_name, z_name, category_name]
    ).update_layout(coloraxis_showscale=False)

def multiple_selection_cleaner(selection: list[str]):
    """ Clean the selection list by removing duplicates and empty strings.
    :param selection: the list of selected items
    :return: a cleaned list of selected items
    """
    selection = []
    return selection
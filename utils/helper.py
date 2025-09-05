#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/3 15:34
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   helper.py
# @Desc     :
from numpy.ma.core import shape
from numpy.random import random as random_seed, get_state, set_state
from pandas import DataFrame
from plotly.express import scatter, scatter_3d
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
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


def visualisation_scatter(data: DataFrame, categories: DataFrame):
    """ Visualise the data using scatter plots.
    :param data: the DataFrame containing the data
    :param categories: the DataFrame containing the categories for colouring and symbolising the data points
    :return: a scatter plot with different colours and symbols for each category
    """
    if categories is not None:
        df = data.join(categories)
        category_name = categories.columns[0]
    else:
        df = data
        category_name = None

    cols = data.columns.tolist()
    dimensions = data.shape[1]

    if dimensions == 2:
        fig = scatter(
            df,
            x=cols[0],
            y=cols[1],
            color=category_name,
            symbol=category_name,
            hover_data=[cols[0], cols[1], category_name]
        )
    elif dimensions == 3:
        fig = scatter_3d(
            df,
            x=cols[0],
            y=cols[1],
            z=cols[2],
            color=category_name,
            symbol=category_name,
            hover_data=[cols[0], cols[1], cols[2], category_name]
        )
    else:
        pca = PCA(n_components=3)
        components = pca.fit_transform(data)
        data = DataFrame(components, columns=["PAC-X", "PAC-Y", "PAC-Z"])
        df = data.join(categories) if categories is not None else data
        fig = scatter_3d(
            df,
            x="PAC-X",
            y="PAC-Y",
            z="PAC-Z",
            color=category_name,
            symbol=category_name,
            hover_data=["PAC-X", "PAC-Y", "PAC-Z", category_name]
        )
    return fig


def data_preprocessor(selected_data: DataFrame) -> tuple[DataFrame, StandardScaler]:
    """ Preprocess the data by handling missing values, scaling numerical features, and encoding categorical features.
    :param selected_data: the DataFrame containing the selected features for training
    :return: a DataFrame containing the preprocessed features
    """
    cols_num = selected_data.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cols_type = selected_data.select_dtypes(include=["object", "category"]).columns.tolist()
    # print(f"The cols filed with number: {cols_num}")
    # print(f"The cols filled with category: {cols_type}")

    # Establish a pipe to process numerical features
    pipe_num = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    # Set a list of transformers for the ColumnTransformer
    transformers = [("number", pipe_num, cols_num)]

    # Establish a pipe to process categorical features
    if cols_type:
        pipe_type = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ])
        transformers.append(("category", pipe_type, cols_type))

    # Establish a column transformer to process numerical and categorical features
    preprocessor = ColumnTransformer(transformers=transformers)
    # Fit and transform the data
    processed = preprocessor.fit_transform(selected_data)

    # If the processed data is a sparse matrix, convert it to a dense array
    if hasattr(processed, "toarray"):
        processed = processed.toarray()

    # Set the feature names for the processed data
    cols_names: list[str] = cols_num
    if cols_type:
        # Due to the OneHotEncoder, the feature names will be obtained throughout
        encoder = preprocessor.named_transformers_["category"]["encoder"]
        cols_names += encoder.get_feature_names_out(cols_type).tolist()

    # Convert the processed data to a DataFrame
    return DataFrame(processed, columns=cols_names), preprocessor.named_transformers_["number"]["scaler"]

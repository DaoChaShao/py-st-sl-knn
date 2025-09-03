#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/3 16:23
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   train.py
# @Desc     :

from pandas import DataFrame
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from streamlit import (empty, sidebar, subheader, session_state, selectbox,
                       multiselect, button, rerun)

from utils.helper import Timer


def selection_cleaner():
    session_state.selected = []
    session_state.X = None


empty_messages: empty = empty()
empty_tables: empty = empty()

for key in ["train", "timer", "selected_train", "X"]:
    session_state.setdefault(key, None)
for key in ["selected"]:
    session_state.setdefault(key, [])

with sidebar:
    if session_state.train is None:
        empty_messages.error("Please upload the dataset first on the Data Preparation page.")
    else:
        empty_messages.info(f"{session_state.timer} Model Training is complete.")
        subheader("Model Training Settings")

        cols: list[str] = session_state.train.columns.tolist()
        ids: str = selectbox(
            "Select the target feature to drop (for prediction)",
            cols, index=0, disabled=True, width="stretch",
            help="Select the target feature to drop (for prediction)",
        )
        cols.remove(ids)

        categories: str = selectbox(
            "Select the target feature to drop (for prediction)",
            cols, index=len(cols) - 1, disabled=True, width="stretch",
            help="Select the target feature to drop (for prediction)",
        )
        cols.remove(categories)

        empty_tables.data_editor(session_state.train, hide_index=True, disabled=True, width="stretch")

        selection: list[str] = multiselect(
            "Select the features to use for training",
            cols, width="stretch",
            key="selected",
            help="Select the features to use for training",
        )

        session_state["selected_train"] = session_state["train"][selection]

        if len(selection) < 2:
            empty_messages.warning("Please select at least two feature for training.")
        else:
            empty_messages.info(f"{len(selection)} features selected.")

            cols_num = session_state["selected_train"].select_dtypes(include=["int64", "float64"]).columns.tolist()
            cols_type = session_state["selected_train"].select_dtypes(include=["object", "category"]).columns.tolist()
            # print(f"The cols filed with number: {cols_num}")
            # print(f"The cols filled with category: {cols_type}")

            # Establish a pipe to process numerical features
            pipe_num = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ])
            # Establish a pipe to process categorical features
            pipe_type = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore"))
            ])
            # Establish a column transformer to process numerical and categorical features
            preprocessor = ColumnTransformer(transformers=[
                ("number", pipe_num, cols_num),
                ("category", pipe_type, cols_type)
            ])
            # Fit and transform the data
            processed = preprocessor.fit_transform(session_state.selected_train)
            # Due to the OneHotEncoder, the feature names will be obtained throughout
            cols_name_type = preprocessor.named_transformers_["category"]["encoder"].get_feature_names_out(cols_type)
            cols_names: list[str] = cols_num + cols_name_type.tolist()

            # Convert the processed data to a DataFrame
            session_state["X"] = DataFrame(processed, columns=cols_names)
            # print(session_state.X)
            empty_tables.data_editor(session_state.X, hide_index=True, disabled=True, width="stretch")

            button("Clear the Data", type="secondary", width="stretch", on_click=selection_cleaner)

#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/3 16:23
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   train.py
# @Desc     :

from pandas import DataFrame
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from streamlit import (empty, sidebar, subheader, session_state, selectbox,
                       multiselect, button, rerun, columns, metric)

from utils.helper import Timer, data_preprocessor


def selection_cleaner():
    session_state.selected = []
    session_state.x_train = None
    session_state.y_train = None


empty_messages: empty = empty()
left, _ = columns(2, gap="large")
empty_charts: empty = empty()
empty_train_title: empty = empty()
empty_train_table: empty = empty()
empty_test_title: empty = empty()
empty_test_table: empty = empty()
empty_test_labels_title: empty = empty()
empty_test_labels_table: empty = empty()

for key in [
    "raw_train", "raw_test", "raw_y_test", "timer",
    "selected_train", "selected_test",
    "x_train", "x_test",
    "KNN"
]:
    session_state.setdefault(key, None)
for key in ["selected"]:
    session_state.setdefault(key, [])

with sidebar:
    if session_state.raw_train is None:
        empty_messages.error("Please upload the dataset first on the Data Preparation page.")
    else:
        empty_messages.info(f"{session_state.timer} Model Training is complete.")
        subheader("Model Training Settings")

        cols_raw_train: list[str] = session_state.raw_train.columns.tolist()
        cols_raw_test: list[str] = session_state.raw_test.columns.tolist()
        cols_raw_y_test: list[str] = session_state.raw_y_test.columns.tolist()

        ids: str = selectbox(
            "Select the target feature to drop (for prediction)",
            cols_raw_train, index=0, disabled=True, width="stretch",
            help="Select the target feature to drop (for prediction)",
        )
        cols_raw_train.remove(ids)
        cols_raw_test.remove(ids)
        cols_raw_y_test.remove(ids)

        seg_name: str = selectbox(
            "Select the target feature to drop (for prediction)",
            cols_raw_train, index=len(cols_raw_train) - 1, disabled=True, width="stretch",
            help="Select the target feature to drop (for prediction)",
        )
        cols_raw_train.remove(seg_name)

        cut_train: DataFrame = session_state.raw_train[cols_raw_train]
        cut_test: DataFrame = session_state.raw_test[cols_raw_test]
        y_test: DataFrame = session_state.raw_y_test[cols_raw_y_test]
        empty_train_title.markdown(f"### Training Data {cut_train.shape}")
        empty_train_table.data_editor(cut_train, hide_index=True, disabled=True, width="stretch")
        empty_test_title.markdown(f"### Testing Data {cut_test.shape}")
        empty_test_table.data_editor(cut_test, hide_index=True, disabled=True, width="stretch")
        empty_test_labels_title.markdown(f"### Testing Data Labels {y_test.shape}")
        empty_test_labels_table.data_editor(y_test, hide_index=True, disabled=True, width="stretch")

        selection: list[str] = multiselect(
            "Select the features to use for training",
            cols_raw_train, width="stretch",
            default=session_state.selected,
            help="Select the features to use for training",
        )
        session_state["selected"] = selection

        session_state["selected_train"] = cut_train[selection]
        session_state["selected_test"] = cut_test[selection]

        if len(selection) < 2:
            empty_messages.warning("Please select at least two feature for training.")
        else:
            empty_messages.info(f"{len(selection)} features selected.")

            session_state["x_train"]: DataFrame = data_preprocessor(session_state.selected_train)
            empty_train_table.data_editor(session_state.x_train, hide_index=True, disabled=True, width="stretch")
            session_state["x_test"]: DataFrame = data_preprocessor(session_state.selected_test)
            empty_test_table.data_editor(session_state.x_test, hide_index=True, disabled=True, width="stretch")

            y_train = session_state["raw_train"][seg_name]

            if session_state["KNN"] is None:
                if button("Start Training", type="primary", width="stretch"):
                    with Timer("Model Training") as t:
                        # 3 means the 3 nearest neighbours
                        session_state["KNN"] = KNeighborsClassifier(n_neighbors=3)
                        session_state["KNN"].fit(session_state.x_train, y_train)

                    session_state["timer"] = t
                    rerun()
            else:
                empty_messages.success(f"{session_state.timer} Model Training is complete.")
                y_pre = session_state["KNN"].predict(session_state.x_test)
                acc = accuracy_score(y_test, y_pre)
                percentage = round(acc * 100, 1)

                with left:
                    metric("Accuracy Score", f"{acc:.2%}", delta=f"{percentage - 100:.4f} %", delta_color="normal")

                button("Clear the Model", type="secondary", width="stretch", on_click=selection_cleaner)
                session_state["KNN"] = None

            button("Clear the Data", type="secondary", width="stretch", on_click=selection_cleaner)

#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/3 15:36
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   preparation.py
# @Desc     :

from pandas import DataFrame, read_csv
from streamlit import (empty, sidebar, subheader, session_state, button,
                       rerun)

from utils.helper import Timer

empty_messages: empty = empty()
empty_train_title: empty = empty()
empty_train_table: empty = empty()
empty_test_title: empty = empty()
empty_test_table: empty = empty()
empty_test_labels_title: empty = empty()
empty_test_labels_table: empty = empty()

for key in ["raw_train", "raw_test", "raw_y_test", "timer", "KNN"]:
    session_state.setdefault(key, None)

with sidebar:
    train_path: str = "train.csv"
    test_path: str = "test.csv"
    test_seg_path: str = "test_seg.csv"

    if session_state["raw_train"] is None:
        empty_messages.error("Please upload the dataset first on this page.")
        subheader("Data Preparation")

        if button("Load the Raw Data", type="primary", width="stretch"):
            with Timer("Train & Test Data Loading") as t:
                session_state["raw_train"]: DataFrame = read_csv(train_path)
                session_state["raw_test"]: DataFrame = read_csv(test_path)
                session_state["raw_y_test"]: DataFrame = read_csv(test_seg_path)
                session_state["timer"]: float = t
            rerun()
    else:
        empty_messages.success(f"{session_state.timer} Data Preparation is complete.")
        empty_train_title.markdown(f"### Training Data {session_state.raw_train.shape}")
        empty_train_table.data_editor(session_state.raw_train, hide_index=True, disabled=True, width="stretch")
        empty_test_title.markdown(f"### Testing Data {session_state.raw_test.shape}")
        empty_test_table.data_editor(session_state.raw_test, hide_index=True, disabled=True, width="stretch")
        empty_test_labels_title.markdown(f"### Testing Data Labels {session_state.raw_y_test.shape}")
        empty_test_labels_table.data_editor(session_state.raw_y_test, hide_index=True, disabled=True, width="stretch")

        if button("Clear the Data", type="secondary", width="stretch"):
            session_state["raw_train"] = None
            session_state["raw_test"] = None
            session_state["raw_y_test"] = None
            session_state["timer"] = None
            session_state["KNN"] = None
            rerun()

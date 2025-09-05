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

for key in ["raw_train", "timer", "KNN"]:
    session_state.setdefault(key, None)

with sidebar:
    train_path: str = "train.csv"

    if session_state["raw_train"] is None:
        empty_messages.error("Please upload the dataset first on this page.")
        subheader("Data Preparation")

        if button("Load the Raw Data", type="primary", width="stretch"):
            with Timer("Train & Test Data Loading") as t:
                session_state["raw_train"]: DataFrame = read_csv(train_path)
                session_state["timer"]: float = t
            rerun()
    else:
        empty_messages.success(f"{session_state.timer} Data Preparation is complete.")
        empty_train_title.markdown(f"### Training Data {session_state.raw_train.shape}")
        empty_train_table.data_editor(session_state.raw_train, hide_index=True, disabled=True, width="stretch")

        if button("Clear the Data", type="secondary", width="stretch"):
            session_state["raw_train"] = None
            session_state["timer"] = None
            session_state["KNN"] = None
            rerun()

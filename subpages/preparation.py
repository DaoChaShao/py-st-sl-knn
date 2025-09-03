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
empty_table: empty = empty()

for key in ["train", "timer"]:
    session_state.setdefault(key, None)

with sidebar:
    train_path: str = "train.csv"

    if session_state["train"] is None:
        empty_messages.error("Please upload the dataset first on this page.")
        subheader("Data Preparation")

        if button("Load the Data", type="primary", width="stretch"):
            with Timer("Data Loading") as t:
                session_state["train"]: DataFrame = read_csv(train_path)
                session_state["timer"]: float = t
            rerun()
    else:
        empty_messages.success(f"{session_state.timer} Data Preparation is complete.")
        empty_table.data_editor(
            session_state.train,
            hide_index=True, disabled=True, width="stretch",
        )

        if button("Clear the Data", type="secondary", width="stretch"):
            session_state["train"] = None
            rerun()

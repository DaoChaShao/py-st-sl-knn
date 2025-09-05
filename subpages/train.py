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
                       multiselect, button, rerun, columns, metric,
                       markdown, plotly_chart)

from utils.helper import Timer, data_preprocessor, visualisation_scatter


def selection_cleaner():
    session_state.selected = []
    session_state.x_train = None
    session_state.y_train = None
    session_state.KNN = None
    session_state.timer = None


empty_messages: empty = empty()
score, _ = columns(2, gap="large")
left, right = columns(2, gap="large")
empty_train_title: empty = empty()
empty_train_table: empty = empty()

for key in ["raw_train", "selected_train", "x_train", "timer", "KNN"]:
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

        ids: str = selectbox(
            "Select the target feature to drop (for prediction)",
            cols_raw_train, index=0, disabled=True, width="stretch",
            help="Select the target feature to drop (for prediction)",
        )
        cols_raw_train.remove(ids)

        seg_name: str = selectbox(
            "Select the target feature to drop (for prediction)",
            cols_raw_train, index=len(cols_raw_train) - 1, disabled=True, width="stretch",
            help="Select the target feature to drop (for prediction)",
        )
        cols_raw_train.remove(seg_name)

        cut_train: DataFrame = session_state.raw_train[cols_raw_train]
        empty_train_title.markdown(f"### Training Data {cut_train.shape}")
        empty_train_table.data_editor(cut_train, hide_index=True, disabled=True, width="stretch")

        selection: list[str] = multiselect(
            "Select the features to use for training",
            cols_raw_train, width="stretch",
            default=session_state.selected,
            help="Select the features to use for training",
        )
        session_state["selected"] = selection

        session_state["selected_train"] = cut_train[selection]

        if len(selection) < 2:
            empty_messages.warning("Please select at least two feature for training.")
        else:
            empty_messages.info(f"{len(selection)} features selected.")

            session_state["x_train"], scaler = data_preprocessor(session_state.selected_train)
            empty_train_table.data_editor(session_state.x_train, hide_index=True, disabled=True, width="stretch")

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
                y_pred = session_state["KNN"].predict(session_state.x_train)
                acc = accuracy_score(y_train, y_pred)
                percentage = round(acc * 100, 2)
                with score:
                    metric(
                        "Training Accuracy", f"{percentage} %", delta=f"{percentage - 100:.4f} %", delta_color="normal"
                    )

                if session_state.x_train.shape[1] <= 3:
                    x_inverse = DataFrame(
                        scaler.inverse_transform(session_state.x_train.copy()), columns=session_state.x_train.columns
                    )
                else:
                    x_inverse = session_state.x_train.copy()

                # Align the index for better visualisation
                y_true = DataFrame(y_train, index=session_state.x_train.index, columns=[seg_name])
                y_pred = DataFrame(y_pred, index=session_state.x_train.index, columns=[seg_name])

                with left:
                    markdown("### Testing Data - True Labels")
                    before = visualisation_scatter(x_inverse, y_true)
                    plotly_chart(before, use_container_width=True)

                with right:
                    markdown("### Testing Data - Predicted Labels")
                    after = visualisation_scatter(x_inverse, y_pred)
                    plotly_chart(after, use_container_width=True)

            button("Clear the Data", type="secondary", width="stretch", on_click=selection_cleaner)

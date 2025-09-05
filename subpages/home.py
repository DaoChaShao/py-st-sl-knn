#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/3 15:35
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   home.py
# @Desc     :

from streamlit import title, expander, caption, empty

empty_message = empty()
empty_message.info("Please check the details at the different pages of core functions.")

title("Supervised Learning with K-Nearest Neighbors (KNN) models")
with expander("**INTRODUCTION**", expanded=True):
    caption("- **Dynamic KNN Classification App**: Train and test KNN models interactively with your dataset.")
    caption("- **Simple 2D Mode**: Select up to 3 features and visualise true vs predicted labels in 2D scatter plots.")
    caption("- **Advanced 3D Mode**: Use multiple features, project data with PCA, and visualise in 3D scatter plots.")
    caption("- **Real-Time Prediction**: See predicted labels immediately after training the model.")
    caption("- **Reproducibility**: Random seed and standardization applied automatically for consistent results.")
    caption("- **Data Upload & Preview**: Upload CSV files and inspect both raw and preprocessed data in interactive tables.")

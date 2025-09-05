#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/3 15:35
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   about.py
# @Desc     :

from streamlit import title, expander, caption

title("**Application Information**")
with expander("About this application", expanded=True):
    caption("- **Interactive Feature Selection**: Dynamically choose which features to include for KNN training.")
    caption("- **Automatic Preprocessing**: Handle missing values, scale numerical features, and encode categorical features automatically.")
    caption("- **KNN Model Training**: Train a KNN classifier with customizable number of neighbors and see training accuracy immediately.")
    caption("- **2D/3D Dynamic Visualisation**: True vs predicted labels visualised in 2D or 3D scatter plots; PCA applied for high-dimensional data.")
    caption("- **Side-by-Side Comparison**: Compare true labels and predicted labels in one view, maintaining consistent colors and symbols.")
    caption("- **Real-Time Interaction**: Update features or retrain models and see visualisation results instantly.")
    caption("- **Data Inspection & Table View**: Preview uploaded dataset and preprocessed training data in interactive tables.")
    caption("- **Model Management**: Clear or retrain models with ease, maintaining a clean workflow.")
    caption("- **Designed for Learning & Exploration**: Perfect for students, educators, and data enthusiasts to experiment with KNN classification interactively.")
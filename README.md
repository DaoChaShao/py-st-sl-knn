<p align="right">
  Language Switch / 语言选择：
  <a href="./README.zh-CN.md">🇨🇳 中文</a> | <a href="./README.md">🇬🇧 English</a>
</p>

**INTRODUCTION**
---
This application is built on the [Customer Segmentation dataset](https://www.kaggle.com/datasets/vetrirah/customer) from
Kaggle. It applies the **K-Nearest Neighbours (KNN)** algorithm from **scikit-learn** for supervised learning tasks. The
interactive interface is developed using **Streamlit**, while **Plotly** is used for rich and dynamic data
visualisation. It allows preprocessing, scaling, and encoding of data, and visualises both the true and predicted labels
in interactive 2D or 3D scatter plots.

**FEATURES**
---

- **Interactive Data Selection**  
  Select features for training dynamically, drop target columns, and inspect the dataset before model training.
- **Data Preprocessing**  
  Automatically handles missing values, scales numerical features, and encodes categorical features.
- **KNN Model Training**  
  Train a KNN classifier with customizable neighbours and instantly evaluate training accuracy.
- **Dynamic Visualization**  
  Visualise high-dimensional data in 2D or 3D scatter plots. Automatically applies PCA for dimensions > 3.
- **True vs Predicted Labels**  
  Compare the true labels and predicted labels side by side with consistent colouring and symbols.
- **Streamlit-based Interactive UI**  
  Easy-to-use sidebar controls, tables, and charts for a smooth user experience.

**DATA DESCRIPTION**
---

1. **Files**

- `Train.csv`: 8,068 records, 11 columns (includes the target `Segmentation`).
- `Test.csv`: 2,627 records, 10 columns (does **not** include `Segmentation`, used for prediction/submission).
- `sample_submission.csv`: 2,627 records with `ID` and `Segmentation` (example submission format).

2. **Columns (fields)**

- `ID`: unique customer identifier.
- `Gender`: customer gender (`Male` / `Female`).
- `Ever_Married`: whether married (`Yes` / `No`). (140 missing in train)
- `Age`: age (integer).
- `Graduated`: whether graduated (`Yes` / `No`). (78 missing in train)
- `Profession`: profession category (examples: `Artist`, `Healthcare`, `Entertainment`, `Engineer`, `Doctor`, `Lawyer`,
  `Executive`, `Marketing`, `Homemaker`). (124 missing in train)
- `Work_Experience`: years of work experience (numeric). (829 missing in train)
- `Spending_Score`: spending score category (`Low`, `Average`, `High`).
- `Family_Size`: family size (numeric). (335 missing in train)
- `Var_1`: additional categorical variable (`Cat_1` .. `Cat_7`). (76 missing in train)
- `Segmentation`: target segmentation label (`A` / `B` / `C` / `D`), present only in `Train.csv`.

3. **Target distribution (Train.csv)**

- A: 1972
- B: 1858
- C: 1970
- D: 2268

4. **Missing-value notes**

- Columns such as `Ever_Married`, `Graduated`, `Profession`, `Work_Experience`, `Family_Size`, and `Var_1` contain
  missing values — handle them (imputation/deletion/model-based fill) before encoding and training.

5. **Additional notes**

- `Test.csv` lacks `Segmentation`. After training your KNN model, run predictions on `Test.csv` and save the results in
  the same layout as `sample_submission.csv` for evaluation or submission.

**WEB DEVELOPMENT**
---

1. Install NiceGUI with the command `pip install streamlit`.
2. Run the command `pip show streamlit` or `pip show streamlit | grep Version` to check whether the package has been
   installed and its version.

**PRIVACY NOTICE**
---
This application may require inputting personal information or private data to generate customised suggestions,
recommendations, and necessary results. However, please rest assured that the application does **NOT** collect, store,
or transmit your personal information. All processing occurs locally in the browser or runtime environment, and **NO**
data is sent to any external server or third-party service. The entire codebase is open and transparent — you are
welcome to review the code [here](./) at any time to verify how your data is handled.

**LICENCE**
---
This application is licensed under the [BSD-3-Clause License](LICENSE). You can click the link to read the licence.

**CHANGELOG**
---
This guide outlines the steps to automatically generate and maintain a project changelog using git-changelog.

1. Install the required dependencies with the command `pip install git-changelog`.
2. Run the command `pip show git-changelog` or `pip show git-changelog | grep Version` to check whether the changelog
   package has been installed and its version.
3. Prepare the configuration file of `pyproject.toml` at the root of the file.
4. The changelog style is [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
5. Run the command `git-changelog`, creating the `Changelog.md` file.
6. Add the file `Changelog.md` to version control with the command `git add Changelog.md` or using the UI interface.
7. Run the command `git-changelog --output CHANGELOG.md` committing the changes and updating the changelog.
8. Push the changes to the remote repository with the command `git push origin main` or using the UI interface.

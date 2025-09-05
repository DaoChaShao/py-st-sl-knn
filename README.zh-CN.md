<p align="right">
  Language Switch / 语言选择：
  <a href="./README.zh-CN.md">🇨🇳 中文</a> | <a href="./README.md">🇬🇧 English</a>
</p>

**应用简介**
---
本应用基于 Kaggle 提供的 [Customer Segmentation 数据集](https://www.kaggle.com/datasets/vetrirah/customer)，使用
**scikit-learn** 中的 **KNN (K-Nearest Neighbors)** 算法进行监督学习建模。通过 **Streamlit** 构建交互式网页界面，并结合
**Plotly** 进行可视化分析。 用户可以自由选择特征。应用支持数据预处理、数值缩放和分类编码，并可以通过交互式 2D 或 3D
散点图展示真实标签与预测标签。

**功能特色**
---

- **交互式数据选择**  
  用户可动态选择用于训练的特征，去除目标列，并在训练前检查数据集。
- **数据预处理**  
  自动处理缺失值、数值特征缩放，并对分类特征进行编码。
- **KNN 模型训练**  
  可自定义邻居数量训练 KNN 分类器，并即时评估训练准确率。
- **动态可视化**  
  可视化高维数据为 2D 或 3D 散点图。对于维度 >3 的数据会自动应用 PCA。
- **真实标签与预测标签对比**  
  在同一界面中对比真实标签与预测标签，保证颜色和符号一致。
- **基于 Streamlit 的交互界面**  
  提供便捷的侧边栏控制、表格和图表，提升用户体验。

**数据说明**
---

1. **数据文件**

- `Train.csv`：8068 条记录，11 列（包含目标 `Segmentation`）。
- `Test.csv`：2627 条记录，10 列（不包含 `Segmentation`，用于模型预测/提交）。
- `sample_submission.csv`：2627 条记录，包含 `ID` 与 `Segmentation`（示例提交格式，参照该格式生成提交文件）。

2. **字段说明**

- `ID`：客户唯一标识符。
- `Gender`：性别（`Male` / `Female`）。
- `Ever_Married`：是否结婚（`Yes` / `No`）。（训练集中有 140 个缺失值）
- `Age`：年龄（整数）。
- `Graduated`：是否毕业（`Yes` / `No`）。（训练集中有 78 个缺失值）
- `Profession`：职业类别（示例：`Artist`, `Healthcare`, `Entertainment`, `Engineer`, `Doctor`, `Lawyer`, `Executive`,
  `Marketing`, `Homemaker`）。（训练集中有 124 个缺失值）
- `Work_Experience`：工作经验年数（数值）。（训练集中有 829 个缺失值）
- `Spending_Score`：消费评分类别（`Low`, `Average`, `High`）。
- `Family_Size`：家庭人数（数值）。（训练集中有 335 个缺失值）
- `Var_1`：额外的类别变量（`Cat_1` .. `Cat_7`）。（训练集中有 76 个缺失值）
- `Segmentation`：目标变量（类别标签 `A` / `B` / `C` / `D`），仅存在于 `Train.csv`。

3. **目标分布（Train.csv）**

- A: 1972
- B: 1858
- C: 1970
- D: 2268

4. **缺失值提示**

- 若用于建模，建议对 `Ever_Married`、`Graduated`、`Profession`、`Work_Experience`、`Family_Size`、`Var_1`
  等列先做缺失值处理（如常数/众数填充、基于其他特征的插补或直接删除少量缺失行），然后对类别特征进行编码（One-Hot / Ordinal /
  Target Encoding 等），数值特征可做标准化或归一化，最后再训练 KNN 模型。

5. **其它说明**

- `Test.csv` 不包含 `Segmentation`，请在训练好模型后对 Test 数据进行预测并按 `sample_submission.csv` 格式保存结果以便提交或评估。

**网页开发**
---

1. 使用命令`pip install streamlit`安装`Streamlit`平台。
2. 执行`pip show streamlit`或者`pip show git-streamlit | grep Version`检查是否已正确安装该包及其版本。

**隐私声明**
---
本应用可能需要您输入个人信息或隐私数据，以生成定制建议和结果。但请放心，应用程序 **不会**
收集、存储或传输您的任何个人信息。所有计算和数据处理均在本地浏览器或运行环境中完成，**不会** 向任何外部服务器或第三方服务发送数据。

整个代码库是开放透明的，您可以随时查看 [这里](./) 的代码，以验证您的数据处理方式。

**许可协议**
---
本应用基于 **BSD-3-Clause 许可证** 开源发布。您可以点击链接阅读完整协议内容：👉 [BSD-3-Clause License](./LICENSE)。

**更新日志**
---
本指南概述了如何使用 git-changelog 自动生成并维护项目的变更日志的步骤。

1. 使用命令`pip install git-changelog`安装所需依赖项。
2. 执行`pip show git-changelog`或者`pip show git-changelog | grep Version`检查是否已正确安装该包及其版本。
3. 在项目根目录下准备`pyproject.toml`配置文件。
4. 更新日志遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/) 提交规范。
5. 执行命令`git-changelog`创建`Changelog.md`文件。
6. 使用`git add Changelog.md`或图形界面将该文件添加到版本控制中。
7. 执行`git-changelog --output CHANGELOG.md`提交变更并更新日志。
8. 使用`git push origin main`或 UI 工具将变更推送至远程仓库。

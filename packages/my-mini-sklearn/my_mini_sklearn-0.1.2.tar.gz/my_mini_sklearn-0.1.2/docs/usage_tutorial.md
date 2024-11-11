****使用教程****
欢迎使用 mini_sklearn！本库提供了一些简单易用的机器学习工具，灵感来自于 scikit-learn。本教程将引导你快速上手，了解如何使用本库进行数据预处理、模型训练、评估等。

**目录**
* 数据预处理
* 标准化
* 归一化
* 标签编码
* 模型训练与预测
* 交叉验证
* 网格搜索调优
* 模型评估

**数据预处理**
mini_sklearn 提供了几种常见的数据预处理方法，包括标准化、归一化和标签编码。以下是它们的使用方法。

1. 标准化（Standardization）
标准化是将数据调整为零均值、单位方差。你可以使用 Standardize 类来进行标准化处理。


`from mini_sklearn.data_processing import Standardize`
`import numpy as np`

# 创建一个标准化实例
`scaler = Standardize()`

# 假设 X 是你的特征数据
`X = np.array([[1, 2], [3, 4], [5, 6]])`

# 计算均值和标准差，并进行标准化
`X_standardized = scaler.fit_transform(X)`

`print(X_standardized)`

2. 归一化（Normalization）
归一化将数据缩放到一个指定的范围，默认是 [0, 1]。可以使用 Normalize 类进行归一化。


`from mini_sklearn.data_processing import Normalize`

# 创建归一化实例
`normalizer = Normalize()`

# 假设 X 是你的特征数据
`X_normalized = normalizer.fit_transform(X)`

`print(X_normalized)`

3. 标签编码（Label Encoding）
标签编码用于将类别标签转换为数字。可以使用 LabelEncoderWrapper 来进行标签编码。


`from mini_sklearn.data_processing import LabelEncoderWrapper`

# 创建标签编码实例
`encoder = LabelEncoderWrapper()`

# 假设 y 是你的标签数据
`y = np.array(['cat', 'dog', 'cat', 'dog'])`

# 计算并转换标签
`y_encoded = encoder.fit_transform(y)`

`print(y_encoded)`
**模型训练与预测**
mini_sklearn 提供了多种常见的机器学习模型。你可以使用这些模型进行训练和预测。下面是使用一个简单的分类模型（例如，逻辑回归）的示例。


`from mini_sklearn.models import LinearRegression`
`from mini_sklearn.data_processing import train_test_split_data`

# 假设 X 和 y 是你的数据和标签
`X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])`
`y = np.array([0, 1, 0, 1])`

# 数据拆分
`X_train, X_test, y_train, y_test = train_test_split_data(X, y, test_size=0.2)`

# 创建逻辑回归模型
`model = LinearRegression()`

# 训练模型
`model.fit(X_train, y_train)`

# 进行预测
`y_pred = model.predict(X_test)`

`print("预测结果:", y_pred)`


**交叉验证**
交叉验证是评估模型性能的一种方法，尤其适用于数据量较小的情况。mini_sklearn 提供了 CrossValidation 类来进行交叉验证。


`from mini_sklearn.model_selection import CrossValidation`
`from mini_sklearn.models import LinearRegression`

# 创建交叉验证实例
`cv = CrossValidation(n_splits=3)`

# 创建模型
`model = LinearRegression()`

# 进行交叉验证并获取得分
`scores = cv.cross_val_score(model, X, y, scoring="accuracy")`

`print("交叉验证得分:", scores)`


**网格搜索调优**
网格搜索（Grid Search）可以帮助你找到最佳的超参数组合。你可以使用 GridSearchCV 类来进行超参数调优。


`from mini_sklearn.grid_search import GridSearchCV`
`from mini_sklearn.models import LinearRegression`

# 创建网格搜索实例
`param_grid = {'C': [0.1, 1, 10], 'solver': ['lbfgs', 'saga']}`
`grid_search = GridSearchCV(estimator=LinearRegression, param_grid=param_grid, cv=3)`

# 进行网格搜索
`grid_search.fit(X, y)`

# 输出最佳参数和得分
`print("最佳参数:", grid_search.best_params_)`
`print("最佳得分:", grid_search.best_score_)`


**模型评估**
mini_sklearn 提供了多个评估指标，包括准确率、混淆矩阵、精确率、召回率、F1 分数等。

1. 准确率（Accuracy）

`from mini_sklearn.model_evaluation import accuracy_score`

# 假设 y_true 和 y_pred 是真实标签和预测标签
`y_true = np.array([0, 1, 0, 1])`
`y_pred = np.array([0, 1, 1, 1])`

# 计算准确率
`accuracy = accuracy_score(y_true, y_pred)`

`print("准确率:", accuracy)`
2. 混淆矩阵（Confusion Matrix）

`from mini_sklearn.model_evaluation import confusion_matrix`

# 计算混淆矩阵
`conf_matrix = confusion_matrix(y_true, y_pred)`

`print("混淆矩阵:")`
`print(conf_matrix)`

3. 精确率、召回率、F1 分数

`from mini_sklearn.model_evaluation import precision_recall_f1`

# 计算精确率、召回率和 F1 分数
`precision, recall, f1 = precision_recall_f1(y_true, y_pred)`

`print("精确率:", precision)`
`print("召回率:", recall)`
`print("F1 分数:", f1)`

**结语**
以上就是 mini_sklearn 的基本使用教程。在本教程中，我们介绍了如何进行数据预处理、训练模型、使用交叉验证、网格搜索调优以及模型评估。通过这些基本的功能，你可以轻松实现常见的机器学习任务。

如有更多问题，欢迎参考 API 参考 或查阅 安装指南。

祝你在机器学习项目中取得成功！
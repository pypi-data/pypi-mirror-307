import numpy as np

class GridSearchCV:
    """
    网格搜索交叉验证（Grid Search Cross Validation）用于超参数调优。

    参数：
    - estimator: 需要调优的模型类，如LinearRegression、DecisionTreeClassifier等。
    - param_grid: dict 类型，包含模型超参数的不同候选值。
    - cv: int，表示交叉验证的折数。

    方法：
    - fit(X, y): 根据训练数据和目标值来执行网格搜索。
    - best_params_: 获取网格搜索后的最佳超参数组合。
    - best_score_: 获取网格搜索后的最佳交叉验证得分。
    - best_estimator_: 获取最佳模型。
    """

    def __init__(self, estimator, param_grid, cv=5):
        self.estimator = estimator  # 需要调优的模型
        self.param_grid = param_grid  # 超参数的候选值
        self.cv = cv  # 交叉验证的折数
        self.best_params_ = None  # 最佳超参数
        self.best_score_ = None  # 最佳得分
        self.best_estimator_ = None  # 最佳模型

    def fit(self, X, y):
        """
        执行网格搜索，遍历所有超参数的组合。

        参数：
        - X : ndarray，形状为 (n_samples, n_features)
              训练数据的输入特征。
        - y : ndarray，形状为 (n_samples,)
              训练数据的目标值。
        """
        best_score = -np.inf  # 初始化最佳得分
        best_params = None  # 初始化最佳超参数组合
        best_estimator = None  # 初始化最佳模型

        # 遍历所有超参数组合
        param_grid_list = [dict(zip(self.param_grid, v)) for v in self._dict_product(self.param_grid)]

        for params in param_grid_list:
            model = self.estimator(**params)  # 使用当前参数组合初始化模型
            cv_scores = self._cross_val_score(model, X, y)  # 执行交叉验证
            mean_score = np.mean(cv_scores)  # 计算平均得分

            if mean_score > best_score:
                best_score = mean_score  # 更新最佳得分
                best_params = params  # 更新最佳超参数组合
                best_estimator = model  # 更新最佳模型

        self.best_params_ = best_params
        self.best_score_ = best_score
        self.best_estimator_ = best_estimator

    def _dict_product(self, param_grid):
        """
        生成参数网格的所有可能组合。
        """
        keys = param_grid.keys()
        values = param_grid.values()
        return self._cartesian_product(*values)

    def _cartesian_product(self, *arrays):
        """
        计算多个数组的笛卡尔积，返回所有可能的组合。
        """
        result = [[]]
        for array in arrays:
            result = [x + [y] for x in result for y in array]
        return result

    def _cross_val_score(self, model, X, y):
        """
        使用手动实现的KFold交叉验证评估模型表现。
        """
        n_samples = len(X)
        indices = np.arange(n_samples)
        np.random.shuffle(indices)  # 打乱数据顺序
        fold_sizes = n_samples // self.cv
        scores = []

        for i in range(self.cv):
            test_indices = indices[i * fold_sizes:(i + 1) * fold_sizes]
            train_indices = np.setdiff1d(indices, test_indices)

            X_train, X_test = X[train_indices], X[test_indices]
            y_train, y_test = y[train_indices], y[test_indices]

            model.fit(X_train, y_train)
            score = self._accuracy_score(y_test, model.predict(X_test))
            scores.append(score)

        return scores

    def _accuracy_score(self, y_true, y_pred):
        """
        计算预测结果的准确率。

        Parameters:
        - y_true : ndarray, 真实标签
        - y_pred : ndarray, 预测标签

        Returns:
        - accuracy : float, 准确率
        """
        correct = np.sum(y_true == y_pred)
        accuracy = correct / len(y_true)
        return accuracy

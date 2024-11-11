import numpy as np
from collections import Counter


class DecisionTreeClassifier:
    def __init__(self, max_depth=None):
        """
        初始化决策树分类器。

        参数:
        max_depth (int): 树的最大深度，默认为 None 表示没有限制。
        """
        self.max_depth = max_depth
        self.tree = None

    def fit(self, X, y):
        """
        训练决策树模型。

        参数:
        X (numpy.ndarray): 特征数据，形状为 (n_samples, n_features)。
        y (numpy.ndarray): 标签数据，形状为 (n_samples,)。
        """
        self.tree = self._build_tree(X, y)

    def predict(self, X):
        """
        使用决策树进行预测。

        参数:
        X (numpy.ndarray): 待预测的数据，形状为 (n_samples, n_features)。

        返回:
        numpy.ndarray: 预测标签，形状为 (n_samples,)。
        """
        return np.array([self._predict_single(x, self.tree) for x in X])

    def _entropy(self, y):
        """
        计算信息熵。

        参数:
        y (numpy.ndarray): 标签数据。

        返回:
        float: 信息熵。
        """
        counts = np.bincount(y)
        probabilities = counts / len(y)
        entropy = -np.sum([p * np.log2(p) for p in probabilities if p > 0])
        return entropy

    def _information_gain(self, X_column, y, threshold):
        """
        计算信息增益。

        参数:
        X_column (numpy.ndarray): 特征列。
        y (numpy.ndarray): 标签数据。
        threshold (float): 阈值。

        返回:
        float: 信息增益。
        """
        # 分割数据
        left_indices = X_column <= threshold
        right_indices = X_column > threshold
        left_y, right_y = y[left_indices], y[right_indices]

        # 计算信息增益
        if len(left_y) == 0 or len(right_y) == 0:
            return 0

        parent_entropy = self._entropy(y)
        n = len(y)
        n_left, n_right = len(left_y), len(right_y)
        child_entropy = (n_left / n) * self._entropy(left_y) + (n_right / n) * self._entropy(right_y)

        info_gain = parent_entropy - child_entropy
        return info_gain

    def _best_split(self, X, y):
        """
        找到最佳分割特征和阈值。

        参数:
        X (numpy.ndarray): 特征数据。
        y (numpy.ndarray): 标签数据。

        返回:
        tuple: (最佳特征索引，最佳阈值，最大信息增益)。
        """
        best_gain = -1
        split_index, split_threshold = None, None

        for i in range(X.shape[1]):
            X_column = X[:, i]
            thresholds = np.unique(X_column)

            for threshold in thresholds:
                gain = self._information_gain(X_column, y, threshold)
                if gain > best_gain:
                    best_gain = gain
                    split_index = i
                    split_threshold = threshold

        return split_index, split_threshold, best_gain

    def _build_tree(self, X, y, depth=0):
        """
        递归地构建决策树。

        参数:
        X (numpy.ndarray): 特征数据。
        y (numpy.ndarray): 标签数据。
        depth (int): 当前树的深度。

        返回:
        dict: 表示决策树的节点。
        """
        num_samples, num_features = X.shape
        num_labels = len(np.unique(y))

        # 停止条件
        if depth == self.max_depth or num_labels == 1 or num_samples == 0:
            leaf_value = Counter(y).most_common(1)[0][0]
            return leaf_value

        # 找到最佳分割
        split_index, split_threshold, best_gain = self._best_split(X, y)

        if best_gain == 0:
            leaf_value = Counter(y).most_common(1)[0][0]
            return leaf_value

        # 构建子树
        left_indices = X[:, split_index] <= split_threshold
        right_indices = X[:, split_index] > split_threshold
        left_subtree = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right_subtree = self._build_tree(X[right_indices], y[right_indices], depth + 1)
        return {
            "feature_index": split_index,
            "threshold": split_threshold,
            "left": left_subtree,
            "right": right_subtree
        }

    def _predict_single(self, x, tree):
        """
        对单个样本进行预测。

        参数:
        x (numpy.ndarray): 单个样本。
        tree (dict): 决策树。

        返回:
        int: 预测的标签。
        """
        if not isinstance(tree, dict):
            return tree

        feature_index = tree["feature_index"]
        threshold = tree["threshold"]

        if x[feature_index] <= threshold:
            return self._predict_single(x, tree["left"])
        else:
            return self._predict_single(x, tree["right"])

    def score(self, X, y):
        """
        计算模型的准确率。

        参数:
        X (numpy.ndarray): 测试数据。
        y (numpy.ndarray): 测试标签。

        返回:
        float: 准确率。
        """
        y_pred = self.predict(X)
        return np.mean(y_pred == y)

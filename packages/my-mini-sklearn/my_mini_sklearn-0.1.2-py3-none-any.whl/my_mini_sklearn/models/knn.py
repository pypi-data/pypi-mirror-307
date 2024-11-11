import numpy as np
from collections import Counter


class KNearestNeighbors:
    def __init__(self, k=3):
        """
        初始化 KNN 模型。

        参数:
        k (int): 使用的邻居数量，默认为3。
        """
        self.k = k

    def fit(self, X, y):
        """
        训练模型。对于 KNN，仅需存储训练数据。

        参数:
        X (numpy.ndarray): 特征数据，形状为 (n_samples, n_features)。
        y (numpy.ndarray): 标签数据，形状为 (n_samples,)。
        """
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        """
        使用 KNN 进行预测。

        参数:
        X (numpy.ndarray): 待预测的数据，形状为 (n_samples, n_features)。

        返回:
        numpy.ndarray: 预测标签，形状为 (n_samples,)。
        """
        predictions = [self._predict_single(x) for x in X]
        return np.array(predictions)

    def _predict_single(self, x):
        """
        对单个样本进行预测。

        参数:
        x (numpy.ndarray): 单个样本数据，形状为 (n_features,)。

        返回:
        int: 预测的标签。
        """
        # 计算所有训练样本与 x 的距离
        distances = np.linalg.norm(self.X_train - x, axis=1)

        # 找到距离最近的 k 个邻居
        k_indices = distances.argsort()[:self.k]

        # 提取这 k 个邻居的标签
        k_nearest_labels = self.y_train[k_indices]

        # 返回出现次数最多的标签
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]

    def score(self, X, y):
        """
        计算模型的准确率。

        参数:
        X (numpy.ndarray): 测试数据，形状为 (n_samples, n_features)。
        y (numpy.ndarray): 测试标签，形状为 (n_samples,)。

        返回:
        float: 准确率，0 到 1 之间。
        """
        y_pred = self.predict(X)
        return np.mean(y_pred == y)

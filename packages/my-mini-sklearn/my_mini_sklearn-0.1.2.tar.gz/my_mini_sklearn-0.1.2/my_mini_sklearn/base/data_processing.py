import numpy as np


# 数据标准化
class Standardize:
    """
    标准化数据（零均值，单位方差）
    """

    def __init__(self):
        self.mean = None
        self.std = None

    def fit(self, X):
        """
        计算数据的均值和标准差
        """
        self.mean = np.mean(X, axis=0)
        self.std = np.std(X, axis=0)
        return self

    def transform(self, X):
        """
        标准化数据（减去均值，除以标准差）
        """
        if self.mean is None or self.std is None:
            raise ValueError("fit method must be called before transform.")
        return (X - self.mean) / self.std

    def fit_transform(self, X):
        """
        计算均值和标准差并进行标准化
        """
        self.fit(X)
        return self.transform(X)


# 数据归一化
class Normalize:
    """
    将数据归一化到指定的范围（默认是0到1）
    """

    def __init__(self, feature_range=(0, 1)):
        self.min = None
        self.max = None
        self.feature_range = feature_range

    def fit(self, X):
        """
        计算数据的最小值和最大值
        """
        self.min = np.min(X, axis=0)
        self.max = np.max(X, axis=0)
        return self

    def transform(self, X):
        """
        将数据归一化到指定范围
        """
        if self.min is None or self.max is None:
            raise ValueError("fit method must be called before transform.")
        # 按公式进行归一化
        return (X - self.min) / (self.max - self.min) * (self.feature_range[1] - self.feature_range[0]) + \
            self.feature_range[0]

    def fit_transform(self, X):
        """
        计算最小值和最大值并进行归一化
        """
        self.fit(X)
        return self.transform(X)


# 标签编码
class LabelEncoderWrapper:
    """
    将类别标签转化为数字编码
    """

    def __init__(self):
        self.classes_ = None
        self.class_map_ = None

    def fit(self, y):
        """
        计算标签的唯一值，并映射到整数
        """
        self.classes_ = np.unique(y)
        self.class_map_ = {cls: idx for idx, cls in enumerate(self.classes_)}
        return self

    def transform(self, y):
        """
        将类别标签转化为数字编码
        """
        if self.class_map_ is None:
            raise ValueError("fit method must be called before transform.")
        return np.array([self.class_map_[label] for label in y])

    def fit_transform(self, y):
        """
        计算标签的唯一值，并将其转化为数字编码
        """
        self.fit(y)
        return self.transform(y)


# 数据拆分
def train_test_split_data(X, y, test_size=0.2, random_state=None):
    """
    将数据集拆分为训练集和测试集
    :param X: 特征数据
    :param y: 标签数据
    :param test_size: 测试集的比例
    :param random_state: 随机种子，确保每次拆分一致
    :return: 训练集和测试集的拆分
    """
    if random_state is not None:
        np.random.seed(random_state)

    # 随机打乱数据
    indices = np.random.permutation(len(X))
    test_size = int(len(X) * test_size)
    train_indices = indices[test_size:]
    test_indices = indices[:test_size]

    # 拆分数据
    X_train, X_test = X[train_indices], X[test_indices]
    y_train, y_test = y[train_indices], y[test_indices]

    return X_train, X_test, y_train, y_test

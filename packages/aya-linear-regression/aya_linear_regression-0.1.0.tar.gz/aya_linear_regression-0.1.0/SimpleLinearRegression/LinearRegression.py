# regression.py
class SimpleLinearRegression:
    def __init__(self):
        self.slope = None
        self.intercept = None

    def fit(self, X, y):
        n = len(X)
        mean_x, mean_y = sum(X) / n, sum(y) / n
        numerator = sum((X[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((X[i] - mean_x) ** 2 for i in range(n))
        self.slope = numerator / denominator
        self.intercept = mean_y - self.slope * mean_x

    def predict(self, X):
        if self.slope is None or self.intercept is None:
            raise ValueError("Model has not been fitted yet!")
        return [self.slope * x + self.intercept for x in X]

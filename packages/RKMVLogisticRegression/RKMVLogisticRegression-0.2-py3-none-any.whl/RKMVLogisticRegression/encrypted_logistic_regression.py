# RKMVLogisticRegression/encrypted_logistic_regression.py

import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class EncryptedLogisticRegression:
    def __init__(self, learning_rate=0.001, max_iterations=500):
        self.weights = None
        self.bias = None
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations

    def fit(self, X_encrypted, y_encrypted):
        n_samples = len(y_encrypted)  # Number of samples
        n_features = len(X_encrypted)  # Number of features
        
        # Initialize weights and bias
        self.weights = np.zeros(n_features)  # Initialize weights for each feature
        self.bias = 0.0

        for _ in range(self.max_iterations):
            # Calculate the predictions
            linear_output = np.zeros(n_samples)

            # Compute linear output
            for i in range(n_samples):
                dot_product = sum(X_encrypted[col][i].decrypt()[0] * self.weights[j]
                                  for j, col in enumerate(X_encrypted.keys()))
                linear_output[i] = dot_product + self.bias
            
            predictions = 1 / (1 + np.exp(-linear_output))  # Sigmoid function

            # Calculate gradients
            errors = predictions - np.array([y_encrypted[i].decrypt()[0] for i in range(n_samples)])
            dw = (1 / n_samples) * np.array([sum(errors[i] * X_encrypted[col][i].decrypt()[0] for i in range(n_samples))
                                              for col in X_encrypted.keys()])
            db = (1 / n_samples) * np.sum(errors)

            # Update weights and bias
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self, X_encrypted):
        predictions = []
        for i in range(len(X_encrypted[next(iter(X_encrypted))])):  # For each encrypted data point
            dot_product = sum(X_encrypted[col][i].decrypt()[0] * self.weights[j]
                              for j, col in enumerate(X_encrypted.keys()))
            dot_product += self.bias  # Add bias

            # Apply sigmoid function
            sigmoid_value = 1 / (1 + np.exp(-dot_product))  # Sigmoid function
            predictions.append(1 if sigmoid_value >= 0.5 else 0)  # Use threshold of 0.5
        return predictions

    def evaluate(self, X_encrypted, y_true):
        predictions = self.predict(X_encrypted)
        accuracy = accuracy_score(y_true, predictions)
        precision = precision_score(y_true, predictions)
        recall = recall_score(y_true, predictions)
        f1 = f1_score(y_true, predictions)
        return accuracy, precision, recall, f1

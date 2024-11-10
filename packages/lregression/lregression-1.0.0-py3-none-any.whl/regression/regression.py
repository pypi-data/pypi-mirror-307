# Import required modules
import numpy as np
 
# Defining the class
class LinearRegression:
    def __init__(self, x, y):
        self.data = x
        self.label = y
        self.m = 0  # slope
        self.b = 0  # intercept
        self.n = len(x)
         
    def fit(self, epochs, lr):
        # Implementing Gradient Descent
        for i in range(epochs):
            y_pred = self.m * self.data + self.b
             
            # Calculating derivatives w.r.t Parameters
            D_m = (-2 / self.n) * sum(self.data * (self.label - y_pred))
            D_b = (-2 / self.n) * sum(self.label - y_pred)
             
            # Updating Parameters
            self.m = self.m - lr * D_m
            self.b = self.b - lr * D_b
             
    def predict(self, inp):
        y_pred = self.m * inp + self.b 
        return y_pred

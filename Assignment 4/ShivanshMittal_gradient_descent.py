import numpy as np
import matplotlib.pyplot as plt

X = np.arange(-20, 20, 0.1)
np.random.shuffle(X)
eps = np.random.rand(400) * 10
y = 23 * X + 43 + eps

b = 0.5
w = 1.0 
iter = 100

alpha = 0.0145  # learning rate- obtained this vale after many runs. This value gives a very good result.

for i in range(iter):
    pred = w * X + b
    err = pred - y

    w = w - alpha * np.mean(err * X)
    b = b - alpha * np.mean(err)

print('w = {:.2f}, b = {:.2f}'.format(w,b))


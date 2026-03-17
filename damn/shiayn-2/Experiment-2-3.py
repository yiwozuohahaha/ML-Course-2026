import torch

x = torch.tensor([5.0],requires_grad=True)
lr = 0.1

for i in range(20):
    y = x**2+2*x+1
    y.backward()

    with torch.no_grad():
        x -= lr*x.grad

    x.grad.zero_()

print(x.item(),y.item())


#观察损失的变化
import matplotlib.pyplot as plt

loss = []
x = torch.tensor([5.0],requires_grad=True)

for i in range(20):
    y = x**2+2*x+1
    loss.append(y.item())

    y.backward()
    with torch.no_grad():
        x -= 0.1*x.grad
    x.grad.zero_()

plt.plot(loss,marker='o')
plt.title("Loss Curve")
plt.grid()
plt.show()

#优化路径

import numpy as np

x_vals = np.linspace(-5,5,100)
y_vals = x_vals**2+2*x_vals+1

x_path = []
x = torch.tensor([5.0],requires_grad=True)

for i in range(10):
    y = x**2+2*x+1
    x_path.append(x.item())

    y.backward()
    with torch.no_grad():
        x -= 0.3*x.grad
    x.grad.zero_()

plt.plot(x_vals,y_vals)
plt.scatter(x_path,[xx**2+2*xx+1 for xx in x_path],color='r')
plt.title("Gradient Descent Path")
plt.grid()
plt.show()
import torch

import numpy as np
import matplotlib.pyplot as plt
import scipy

print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 是否可用: {torch.cuda.is_available()}")
# 创建一个随机张量
x = torch.rand(5, 3)
print(x)

# 定义矩阵 A 和 B
A = torch.tensor([[1.0, 2.0],
                  [3.0, 4.0]])

B = torch.tensor([[5.0, 6.0],
                  [7.0, 8.0]])

# 计算矩阵乘法 (Matrix Multiplication)
C = torch.matmul(A, B)

# 打印结果
print("矩阵 A:\n", A)
print("矩阵 B:\n", B)
print("运算结果 C = A * B:\n", C)


# 1. 在 [0, 2*pi] 之间生成 100 个等间距的点
# 数学表达: x \in [0, 2\pi]
x = np.linspace(0, 2 * np.pi, 100)
# 2. 计算对应的 y 值
# 数学公式: y = sin(x)
y = np.sin(x)
# 3. 创建绘图
plt.figure(figsize=(8, 5))  # 设置画布大小
plt.plot(x, y, label='y = sin(x)', color='blue', linewidth=2)
# 4. 添加图像装饰（支持 LaTeX 数学公式）
plt.title('Visualization Test: Sine Wave', fontsize=14)
plt.xlabel('x (radians)', fontsize=12)
plt.ylabel('y', fontsize=12)
# 在图表中显示数学公式
plt.text(1, 0.5, r'$y = \sin(x)$', fontsize=15, color='red')
plt.grid(True, linestyle='--', alpha=0.7) # 添加虚线网格
plt.legend() # 显示图例
# 5. 显示图像
print("正在生成图像，请查看弹出的窗口...")
plt.show()
import torch
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
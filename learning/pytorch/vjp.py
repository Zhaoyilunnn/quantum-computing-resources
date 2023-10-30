import torch
from torch.autograd import grad

# 定义网络层和输入
linear = torch.nn.Linear(3, 2)
x = torch.randn(4, 3)

# 前向传播
y = linear(x)
print(linear.weight.shape)

# 获取权重的梯度
# y.sum().backward()
# dw = linear.weight.grad

# 定义vjp函数
def vjp(v):
    return grad(y, linear.weight, grad_outputs=v)

# 测试vjp
v = torch.ones(4, 2)
dw_vjp = vjp(v)
print(dw_vjp[0].shape)

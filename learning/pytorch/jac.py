import torch
from torch import nn

fc = nn.Linear(3, 2)

# # x = torch.tensor([1., 2., 3.], requires_grad=True)
# x = torch.rand(16, 3, requires_grad=True)
#
# out = fc(x)
#
# jac = torch.autograd.functional.jacobian(fc, x)
#
# # v = torch.tensor([1., 0.])
# v = torch.randn([16, 2])
# vjp = torch.autograd.functional.vjp(fc, x, v)[1]
#
# print(jac.shape)
# print(vjp.shape)

# 获取fc层参数
w = fc.weight
b = fc.bias

# 输入x
x = torch.rand(16, 3, requires_grad=True)

# 前向传播
out = fc(x)

# 求w的vjp
vw = torch.rand_like(w)
vjp_w = torch.autograd.functional.vjp(fc, x, vw, strict=False)[1]

# 求b的vjp
vb = torch.rand_like(b)
vjp_b = torch.autograd.functional.vjp(fc, x, vb, strict=False)[1]

print(vjp_w.shape)
print(vjp_b.shape)

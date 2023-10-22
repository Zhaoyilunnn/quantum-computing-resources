"""
torch                    2.1.0+cpu
torchaudio               2.1.0+cpu
torchvision              0.16.0+cpu
"""

import numpy as np
from math import cos, sin
import torch
from torch.autograd import Function

Z = np.array([[1, 0], [0, 1]])


def RX(input: torch.Tensor, theta: torch.Tensor):
    theta = np.double(theta)
    mat = np.array(
        [
            [np.cos(0.5 * theta), -1.0j * np.sin(0.5 * theta)],
            [-1.0j * np.sin(0.5 * theta), np.cos(0.5 * theta)],
        ],
        dtype=complex,
    )
    return mat @ input.numpy()


def expectation_z(statevector):
    return np.double(np.matmul(np.matmul(statevector, Z), statevector.conj()))


def param_shift(input, theta):
    theta = np.double(theta)
    theta_plus = theta + np.pi / 2
    theta_minus = theta - np.pi / 2
    expectation_plus = expectation_z(RX(input, theta_plus))
    expectation_minus = expectation_z(RX(input, theta_minus))
    return (expectation_plus - expectation_minus) / 2


class MyRxFunction(Function):
    @staticmethod
    def forward(ctx, input, theta):
        ctx.save_for_backward(input, theta)
        sv = RX(input, theta)
        output = expectation_z(sv)
        return torch.from_numpy(np.array(output))

    @staticmethod
    def backward(ctx, grad_output):
        input, theta = ctx.saved_tensors
        grad_theta = param_shift(input, theta)
        grad_theta = torch.from_numpy(np.array(grad_theta))
        grad_theta = torch.tensor(grad_theta * grad_output)
        return None, grad_theta.reshape(1, 1)


class LinearFunction(Function):
    @staticmethod
    # ctx is the first argument to forward
    def forward(ctx, input, weight, bias=None):
        # The forward pass can use ctx.
        ctx.save_for_backward(input, weight, bias)
        output = input.mm(weight.t())
        if bias is not None:
            output += bias.unsqueeze(0).expand_as(output)
        return output

    @staticmethod
    def backward(ctx, grad_output):
        input, weight, bias = ctx.saved_tensors
        grad_input = grad_weight = grad_bias = None

        if ctx.needs_input_grad[0]:
            grad_input = grad_output.mm(weight)
        if ctx.needs_input_grad[1]:
            grad_weight = grad_output.t().mm(input)
        if bias is not None and ctx.needs_input_grad[2]:
            grad_bias = grad_output.sum(0)

        return grad_input, grad_weight, grad_bias


# # 创建输入和参数
# x = torch.randn(3, 4, requires_grad=True)
# w = torch.randn(6, 4, requires_grad=True)
# b = torch.randn(6, requires_grad=True)
#
# # 前向传播
# y = LinearFunction.apply(x, w, b)
#
# # 构建损失函数
# target = torch.randn(3, 6)
# criterion = torch.nn.MSELoss()
# loss = criterion(y, target)
#
# # 反向传播
# loss.backward()
#
# # 检查梯度
# print(x.grad)
# print(w.grad)
# print(b.grad)

x = torch.randn(2)
norm = torch.norm(x)
x_norm = x / norm
theta = torch.randn(1, requires_grad=True)

y = MyRxFunction.apply(x_norm, theta)

target = torch.tensor(0.5, dtype=torch.double)
criterion = torch.nn.MSELoss()
loss = criterion(y, target)
loss.backward()
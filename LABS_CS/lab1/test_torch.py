import numpy as np
import torch
import torch.nn as nn

from layers import (
    Linear, SoftMax, LogSoftMax, BatchNormalization,
    Dropout, LeakyReLU, Conv2d, MaxPool2d,
)


def compare_conv_lrelu_pool():
    np.random.seed(0)
    torch.manual_seed(0)

    x = np.random.randn(4, 3, 8, 8).astype(np.float32)
    g = np.random.randn(4, 6, 3, 3).astype(np.float32)

    cnp = Conv2d(3, 6, 3)
    lnp = LeakyReLU(0.05)
    pnp = MaxPool2d(2)

    xt = torch.tensor(x, requires_grad=True)
    ctp = nn.Conv2d(3, 6, 3)
    with torch.no_grad():
        ctp.weight.copy_(torch.from_numpy(cnp.W))
        ctp.bias.copy_(torch.from_numpy(cnp.b))
    ltp = nn.LeakyReLU(0.05)
    ptp = nn.MaxPool2d(2)

    y_np = pnp.forward(lnp.forward(cnp.forward(x)))
    y_pt = ptp(ltp(ctp(xt)))

    g1 = pnp.backward(lnp.output, g)
    g2 = lnp.backward(cnp.output, g1)
    dx_np = cnp.backward(x, g2)
    y_pt.backward(torch.tensor(g))

    print("=== Conv + LeakyReLU + MaxPool vs PyTorch ===")
    print("Forward diff     :", np.max(np.abs(y_np - y_pt.detach().numpy())))
    print("Backward dX diff :", np.max(np.abs(dx_np - xt.grad.numpy())))
    print("Backward dW diff :", np.max(np.abs(cnp.gradW - ctp.weight.grad.numpy())))


def compare_linear():
    np.random.seed(0)
    torch.manual_seed(0)

    x = np.random.randn(8, 16).astype(np.float32)
    g = np.random.randn(8, 5).astype(np.float32)

    lin = Linear(16, 5)
    xt = torch.tensor(x, requires_grad=True)
    ltp = nn.Linear(16, 5)
    with torch.no_grad():
        ltp.weight.copy_(torch.from_numpy(lin.W))
        ltp.bias.copy_(torch.from_numpy(lin.b))

    y_np = lin.forward(x)
    y_pt = ltp(xt)
    y_pt.backward(torch.tensor(g))
    lin.backward(x, g)

    print("\n=== Linear vs PyTorch ===")
    print("Forward diff     :", np.max(np.abs(y_np - y_pt.detach().numpy())))
    print("Backward dX diff :", np.max(np.abs(lin.gradInput - xt.grad.numpy())))
    print("Backward dW diff :", np.max(np.abs(lin.gradW - ltp.weight.grad.numpy())))
    print("Backward db diff :", np.max(np.abs(lin.gradb - ltp.bias.grad.numpy())))


def compare_softmax():
    np.random.seed(0)
    torch.manual_seed(0)

    x = np.random.randn(8, 5).astype(np.float32)
    g = np.random.randn(8, 5).astype(np.float32)

    sm = SoftMax()
    y_sm = sm.forward(x)
    sm.backward(x, g)

    xt = torch.tensor(x, requires_grad=True)
    y_pt = nn.Softmax(1)(xt)
    y_pt.backward(torch.tensor(g))

    print("\n=== SoftMax vs PyTorch ===")
    print("Forward diff     :", np.max(np.abs(y_sm - y_pt.detach().numpy())))
    print("Backward dX diff :", np.max(np.abs(sm.gradInput - xt.grad.numpy())))

    lsm = LogSoftMax()
    y_lsm = lsm.forward(x)
    lsm.backward(x, g)

    xt2 = torch.tensor(x, requires_grad=True)
    y_pt2 = nn.LogSoftmax(1)(xt2)
    y_pt2.backward(torch.tensor(g))

    print("\n=== LogSoftMax vs PyTorch ===")
    print("Forward diff     :", np.max(np.abs(y_lsm - y_pt2.detach().numpy())))
    print("Backward dX diff :", np.max(np.abs(lsm.gradInput - xt2.grad.numpy())))


def compare_bn():
    np.random.seed(0)
    torch.manual_seed(0)

    x = np.random.randn(16, 6).astype(np.float32)
    g = np.random.randn(16, 6).astype(np.float32)

    bn = BatchNormalization(alpha=0.9)
    bn.train()
    bn.forward(x)
    bn.backward(x, g)

    xt = torch.tensor(x, requires_grad=True)
    btp = nn.BatchNorm1d(6, momentum=0.1, eps=1e-3)
    btp.train()
    y_pt = btp(xt)
    y_pt.backward(torch.tensor(g))

    print("\n=== BatchNorm vs PyTorch ===")
    print("Forward diff     :", np.max(np.abs(bn.output - y_pt.detach().numpy())))
    print("Backward dX diff :", np.max(np.abs(bn.gradInput - xt.grad.numpy())))


def check_dropout():
    np.random.seed(0)
    x = np.random.randn(16, 6).astype(np.float32)

    d = Dropout(0.3)
    d.train()
    out = d.forward(x)
    print("\n=== Dropout ===")
    print("frac zeros train :", np.mean(out == 0))
    d.evaluate()
    print("test == input    :", np.allclose(d.forward(x), x))


if __name__ == "__main__":
    compare_conv_lrelu_pool()
    compare_linear()
    compare_softmax()
    compare_bn()
    check_dropout()

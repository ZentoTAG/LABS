import numpy as np
import torch
import torch.nn as nn
 
from layers import Linear, SoftMax, LogSoftMax, BatchNormalization, Dropout, LeakyReLU
 
 
def diff(a, b):
    # максимальная разница между моим результатом (numpy) и результатом PyTorch
    return np.max(np.abs(a - b.detach().numpy()))
 
 
def test_linear():
    x = np.random.randn(8, 16)
    g = np.random.randn(8, 5)
 
    mine = Linear(16, 5)
    ref = nn.Linear(16, 5).double()
    # берём те же веса, что у моего слоя
    with torch.no_grad():
        ref.weight.copy_(torch.from_numpy(mine.W))
        ref.bias.copy_(torch.from_numpy(mine.b))
 
    xt = torch.tensor(x, requires_grad=True)
 
    out = mine.forward(x)
    mine.backward(x, g)
 
    out_t = ref(xt)
    out_t.backward(torch.tensor(g))
 
    print("Linear")
    print("  forward :", diff(out, out_t))
    print("  grad x  :", diff(mine.gradInput, xt.grad))
    print("  grad W  :", diff(mine.gradW, ref.weight.grad))
    print("  grad b  :", diff(mine.gradb, ref.bias.grad))
 
 
def test_softmax():
    x = np.random.randn(8, 5)
    g = np.random.randn(8, 5)
 
    mine = SoftMax()
    out = mine.forward(x)
    mine.backward(x, g)
 
    xt = torch.tensor(x, requires_grad=True)
    out_t = nn.Softmax(dim=1)(xt)
    out_t.backward(torch.tensor(g))
 
    print("SoftMax")
    print("  forward :", diff(out, out_t))
    print("  grad x  :", diff(mine.gradInput, xt.grad))
 
 
def test_logsoftmax():
    x = np.random.randn(8, 5)
    g = np.random.randn(8, 5)
 
    mine = LogSoftMax()
    out = mine.forward(x)
    mine.backward(x, g)
 
    xt = torch.tensor(x, requires_grad=True)
    out_t = nn.LogSoftmax(dim=1)(xt)
    out_t.backward(torch.tensor(g))
 
    print("LogSoftMax")
    print("  forward :", diff(out, out_t))
    print("  grad x  :", diff(mine.gradInput, xt.grad))
 
 
def test_batchnorm():
    x = np.random.randn(16, 6)
    g = np.random.randn(16, 6)
 
    mine = BatchNormalization()
    mine.train()
    out = mine.forward(x)
    mine.backward(x, g)
 
    xt = torch.tensor(x, requires_grad=True)
    # eps такой же, как EPS в моём слое; affine=False, т.к. масштабирования у меня нет
    ref = nn.BatchNorm1d(6, eps=1e-3, affine=False).double()
    ref.train()
    out_t = ref(xt)
    out_t.backward(torch.tensor(g))
 
    print("BatchNorm")
    print("  forward :", diff(out, out_t))
    print("  grad x  :", diff(mine.gradInput, xt.grad))
 
    # режим теста: берутся накопленные moving_mean / moving_variance
    # (при alpha=0 это статистики последнего батча), проверим по формуле вручную
    mine.evaluate()
    x2 = np.random.randn(16, 6)
    expected = (x2 - x.mean(0)) / np.sqrt(x.var(0) + 1e-3)
    print("  eval    :", np.max(np.abs(mine.forward(x2) - expected)))
 
 
def test_dropout():
    x = np.random.randn(1000, 20)
 
    mine = Dropout(0.3)
    mine.train()
    out = mine.forward(x)
    print("Dropout")
    print("  доля нулей (ожидаем ~0.3):", np.mean(out == 0))
    print("  среднее до / после       :", x.mean(), out.mean())
 
    mine.evaluate()
    print("  на тесте выход == вход   :", np.allclose(mine.forward(x), x))
 
 
def test_leaky_relu():
    x = np.random.randn(8, 5)
    g = np.random.randn(8, 5)
 
    mine = LeakyReLU(0.05)
    out = mine.forward(x)
    mine.backward(x, g)
 
    xt = torch.tensor(x, requires_grad=True)
    out_t = nn.LeakyReLU(0.05)(xt)
    out_t.backward(torch.tensor(g))
 
    print("LeakyReLU")
    print("  forward :", diff(out, out_t))
    print("  grad x  :", diff(mine.gradInput, xt.grad))
 
 
if __name__ == "__main__":
    np.random.seed(0)
    torch.manual_seed(0)
 
    test_linear()
    test_softmax()
    test_logsoftmax()
    test_batchnorm()
    test_dropout()
    test_leaky_relu()
 

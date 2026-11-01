import numpy as np

from modules import Module


class Linear(Module):
    def __init__(self, n_in, n_out):
        super().__init__()
        stdv = 1. / np.sqrt(n_in)
        self.W = np.random.uniform(-stdv, stdv, (n_out, n_in))
        self.b = np.random.uniform(-stdv, stdv, n_out)
        self.gradW = np.zeros_like(self.W)
        self.gradb = np.zeros_like(self.b)

    def updateOutput(self, x):
        self.output = x @ self.W.T + self.b
        return self.output

    def updateGradInput(self, x, g):
        self.gradInput = g @ self.W
        return self.gradInput

    def accGradParameters(self, x, g):
        self.gradW += g.T @ x
        self.gradb += g.sum(0)

    def zeroGradParameters(self):
        self.gradW.fill(0)
        self.gradb.fill(0)

    def getParameters(self):
        return [self.W, self.b]

    def getGradParameters(self):
        return [self.gradW, self.gradb]

    def __repr__(self):
        s = self.W.shape
        return "Linear %d -> %d" % (s[1], s[0])


class SoftMax(Module):
    def updateOutput(self, x):
        z = x - x.max(1, keepdims=True)
        e = np.exp(z)
        self.output = e / e.sum(1, keepdims=True)
        return self.output

    def updateGradInput(self, x, g):
        s = (g * self.output).sum(1, keepdims=True)
        self.gradInput = self.output * (g - s)
        return self.gradInput

    def __repr__(self):
        return "SoftMax"


class LogSoftMax(Module):
    def updateOutput(self, x):
        z = x - x.max(1, keepdims=True)
        self.output = z - np.log(np.exp(z).sum(1, keepdims=True))
        return self.output

    def updateGradInput(self, x, g):
        sm = np.exp(self.output)
        self.gradInput = g - sm * g.sum(1, keepdims=True)
        return self.gradInput

    def __repr__(self):
        return "LogSoftMax"


class BatchNormalization(Module):
    EPS = 1e-3

    def __init__(self, alpha=0.):
        super().__init__()
        self.alpha = alpha
        self.moving_mean = None
        self.moving_variance = None

    def updateOutput(self, x):
        if self.training:
            self.batch_mean = x.mean(0)
            self.batch_var = x.var(0)
            if self.moving_mean is None:
                self.moving_mean = self.batch_mean.copy()
                self.moving_variance = self.batch_var.copy()
            else:
                self.moving_mean = self.alpha * self.moving_mean + (1 - self.alpha) * self.batch_mean
                self.moving_variance = self.alpha * self.moving_variance + (1 - self.alpha) * self.batch_var
            self.output = (x - self.batch_mean) / np.sqrt(self.batch_var + self.EPS)
        else:
            self.output = (x - self.moving_mean) / np.sqrt(self.moving_variance + self.EPS)
        return self.output

    def updateGradInput(self, x, g):
        N = x.shape[0]
        if self.training:
            inv = 1. / np.sqrt(self.batch_var + self.EPS)
            xh = (x - self.batch_mean) * inv
            self.gradInput = (inv / N) * (N * g - g.sum(0) - xh * (g * xh).sum(0))
        else:
            self.gradInput = g / np.sqrt(self.moving_variance + self.EPS)
        return self.gradInput

    def __repr__(self):
        return "BatchNormalization"


class Dropout(Module):
    def __init__(self, p=0.5):
        super().__init__()
        self.p = p
        self.mask = None

    def updateOutput(self, x):
        if self.training:
            self.mask = (np.random.uniform(size=x.shape) >= self.p) / (1 - self.p)
            self.output = x * self.mask
        else:
            self.output = x
        return self.output

    def updateGradInput(self, x, g):
        self.gradInput = g * self.mask if self.training else g
        return self.gradInput

    def __repr__(self):
        return "Dropout"


class ReLU(Module):
    def updateOutput(self, x):
        self.output = np.maximum(x, 0)
        return self.output

    def updateGradInput(self, x, g):
        self.gradInput = g * (x > 0)
        return self.gradInput

    def __repr__(self):
        return "ReLU"


class LeakyReLU(Module):
    def __init__(self, slope=0.03):
        super().__init__()
        self.slope = slope

    def updateOutput(self, x):
        self.output = np.where(x > 0, x, x * self.slope)
        return self.output

    def updateGradInput(self, x, g):
        self.gradInput = g * np.where(x > 0, 1.0, self.slope)
        return self.gradInput

    def __repr__(self):
        return "LeakyReLU"


class Conv2d(Module):
    def __init__(self, c_in, c_out, k, stride=1, pad=0):
        super().__init__()
        self.c_in = c_in
        self.c_out = c_out
        self.k = k
        self.stride = stride
        self.pad = pad

        stdv = 1. / np.sqrt(c_in * k * k)
        self.W = np.random.uniform(-stdv, stdv, (c_out, c_in, k, k))
        self.b = np.random.uniform(-stdv, stdv, c_out)
        self.gradW = np.zeros_like(self.W)
        self.gradb = np.zeros_like(self.b)

    def _im2col(self, xp, oh, ow):
        B, C, _, _ = xp.shape
        s0, s1, s2, s3 = xp.strides
        shape = (B, oh, ow, C, self.k, self.k)
        strides = (s0, s2 * self.stride, s3 * self.stride, s1, s2, s3)
        v = np.lib.stride_tricks.as_strided(xp, shape=shape, strides=strides)
        return v.reshape(B * oh * ow, C * self.k * self.k)

    def updateOutput(self, x):
        B, C, H, W = x.shape
        oh = (H + 2 * self.pad - self.k) // self.stride + 1
        ow = (W + 2 * self.pad - self.k) // self.stride + 1

        self.xp = np.pad(
            x,
            ((0, 0), (0, 0), (self.pad, self.pad), (self.pad, self.pad))
        )
        self.Xcol = self._im2col(self.xp, oh, ow)

        out = self.Xcol @ self.W.reshape(self.c_out, -1).T + self.b
        self.output = out.reshape(B, oh, ow, self.c_out).transpose(0, 3, 1, 2)
        return self.output

    def updateGradInput(self, x, g):
        B, C, _, _ = x.shape
        _, _, oh, ow = g.shape

        gf = g.transpose(0, 2, 3, 1).reshape(-1, self.c_out)
        dX = (gf @ self.W.reshape(self.c_out, -1)).reshape(B, oh, ow, C, self.k, self.k)

        dxp = np.zeros_like(self.xp)
        for i in range(self.k):
            for j in range(self.k):
                dxp[:, :, i:i + oh * self.stride:self.stride,
                         j:j + ow * self.stride:self.stride] += \
                    dX[:, :, :, :, i, j].transpose(0, 3, 1, 2)

        self.gradInput = (
            dxp[:, :, self.pad:-self.pad, self.pad:-self.pad]
            if self.pad else dxp
        )
        return self.gradInput

    def accGradParameters(self, x, g):
        gf = g.transpose(0, 2, 3, 1).reshape(-1, self.c_out)
        self.gradW += (gf.T @ self.Xcol).reshape(self.W.shape)
        self.gradb += gf.sum(0)

    def zeroGradParameters(self):
        self.gradW.fill(0)
        self.gradb.fill(0)

    def getParameters(self):
        return [self.W, self.b]

    def getGradParameters(self):
        return [self.gradW, self.gradb]

    def __repr__(self):
        return "Conv2d %d -> %d, k=%d, s=%d, p=%d" % (
            self.c_in, self.c_out, self.k, self.stride, self.pad
        )


class MaxPool2d(Module):
    def __init__(self, k=2):
        super().__init__()
        self.k = k

    def updateOutput(self, x):
        B, C, H, W = x.shape
        oh, ow = H // self.k, W // self.k
        r = x[:, :, :oh * self.k, :ow * self.k].reshape(B, C, oh, self.k, ow, self.k)
        self.output = r.max(axis=(3, 5))
        return self.output

    def updateGradInput(self, x, g):
        B, C, H, W = x.shape
        oh, ow = H // self.k, W // self.k
        r = x[:, :, :oh * self.k, :ow * self.k].reshape(B, C, oh, self.k, ow, self.k)
        mask = (r == self.output[:, :, :, None, :, None])
        self.gradInput = np.zeros_like(x)
        self.gradInput[:, :, :oh * self.k, :ow * self.k] = \
            (mask * g[:, :, :, None, :, None]).reshape(B, C, oh * self.k, ow * self.k)
        return self.gradInput

    def __repr__(self):
        return "MaxPool2d k=%d" % self.k

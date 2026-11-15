import numpy as np


class Module(object):
    def __init__(self):
        self.output = None
        self.gradInput = None
        self.training = True

    def forward(self, input):
        return self.updateOutput(input)

    def backward(self, input, gradOutput):
        self.updateGradInput(input, gradOutput)
        self.accGradParameters(input, gradOutput)
        return self.gradInput

    def updateOutput(self, input):
        pass

    def updateGradInput(self, input, gradOutput):
        pass

    def accGradParameters(self, input, gradOutput):
        pass

    def zeroGradParameters(self):
        pass

    def getParameters(self):
        return []

    def getGradParameters(self):
        return []

    def train(self):
        self.training = True

    def evaluate(self):
        self.training = False

    def __repr__(self):
        return "Module"


class Sequential(Module):
    def __init__(self):
        super(Sequential, self).__init__()
        self.modules = []

    def add(self, module):
        self.modules.append(module)

    def updateOutput(self, input):
        y = input
        for m in self.modules:
            y = m.forward(y)
        self.output = y
        return self.output

    def backward(self, input, gradOutput):
        # inputs of every layer, as they were during the forward pass
        t = []
        y = input
        t.append(y)
        for m in self.modules:
            y = m.forward(y)
            t.append(y)

        y = gradOutput
        for i in range(len(self.modules)):
            k = len(self.modules) - i - 1
            y = self.modules[k].backward(t[k], y)
        self.gradInput = y
        return self.gradInput

    def zeroGradParameters(self):
        for module in self.modules:
            module.zeroGradParameters()

    def getParameters(self):
        return [x.getParameters() for x in self.modules]

    def getGradParameters(self):
        return [x.getGradParameters() for x in self.modules]

    def __repr__(self):
        string = "".join([str(x) + '\n' for x in self.modules])
        return string

    def __getitem__(self, x):
        return self.modules.__getitem__(x)

    def train(self):
        self.training = True
        for module in self.modules:
            module.train()

    def evaluate(self):
        self.training = False
        for module in self.modules:
            module.evaluate()


class Linear(Module):
    def __init__(self, n_in, n_out):
        super(Linear, self).__init__()

        stdv = 1. / np.sqrt(n_in)
        self.W = np.random.uniform(-stdv, stdv, size=(n_out, n_in))
        self.b = np.random.uniform(-stdv, stdv, size=n_out)

        self.gradW = np.zeros_like(self.W)
        self.gradb = np.zeros_like(self.b)

    def updateOutput(self, input):
        # y = x W^T + b
        self.output = np.dot(input, self.W.T) + self.b
        return self.output

    def updateGradInput(self, input, gradOutput):
        # dL/dx = dL/dy * W
        self.gradInput = np.dot(gradOutput, self.W)
        return self.gradInput

    def accGradParameters(self, input, gradOutput):
        # dL/dW = (dL/dy)^T * x,  dL/db = sum over the batch
        self.gradW += np.dot(gradOutput.T, input)
        self.gradb += gradOutput.sum(axis=0)

    def zeroGradParameters(self):
        self.gradW.fill(0)
        self.gradb.fill(0)

    def getParameters(self):
        return [self.W, self.b]

    def getGradParameters(self):
        return [self.gradW, self.gradb]

    def __repr__(self):
        s = self.W.shape
        q = 'Linear %d -> %d' % (s[1], s[0])
        return q


class SoftMax(Module):
    def __init__(self):
        super(SoftMax, self).__init__()

    def updateOutput(self, input):
        # normalization for numerical stability
        self.output = np.subtract(input, input.max(axis=1, keepdims=True))

        e = np.exp(self.output)
        self.output = e / e.sum(axis=1, keepdims=True)
        return self.output

    def updateGradInput(self, input, gradOutput):
        # dL/dx_j = s_j * (g_j - sum_i g_i * s_i)
        s = (gradOutput * self.output).sum(axis=1, keepdims=True)
        self.gradInput = self.output * (gradOutput - s)
        return self.gradInput

    def __repr__(self):
        return "SoftMax"


class LogSoftMax(Module):
    def __init__(self):
        super(LogSoftMax, self).__init__()

    def updateOutput(self, input):
        # normalization for numerical stability
        self.output = np.subtract(input, input.max(axis=1, keepdims=True))

        self.output = self.output - np.log(np.exp(self.output).sum(axis=1, keepdims=True))
        return self.output

    def updateGradInput(self, input, gradOutput):
        # dL/dx_j = g_j - softmax_j * sum_i g_i
        softmax = np.exp(self.output)
        self.gradInput = gradOutput - softmax * gradOutput.sum(axis=1, keepdims=True)
        return self.gradInput

    def __repr__(self):
        return "LogSoftMax"


class BatchNormalization(Module):
    EPS = 1e-3

    def __init__(self, alpha=0.):
        super(BatchNormalization, self).__init__()
        self.alpha = alpha
        self.moving_mean = None
        self.moving_variance = None

    def updateOutput(self, input):
        if self.training:
            self.mean = input.mean(axis=0)
            self.var = input.var(axis=0)

            if self.moving_mean is None:
                self.moving_mean = self.mean.copy()
                self.moving_variance = self.var.copy()
            else:
                self.moving_mean = self.moving_mean * self.alpha + self.mean * (1 - self.alpha)
                self.moving_variance = self.moving_variance * self.alpha + self.var * (1 - self.alpha)

            self.output = (input - self.mean) / np.sqrt(self.var + self.EPS)
        else:
            self.output = (input - self.moving_mean) / np.sqrt(self.moving_variance + self.EPS)
        return self.output

    def updateGradInput(self, input, gradOutput):
        if self.training:
            N = input.shape[0]
            inv_std = 1. / np.sqrt(self.var + self.EPS)
            x_hat = (input - self.mean) * inv_std
            self.gradInput = inv_std / N * (
                N * gradOutput
                - gradOutput.sum(axis=0)
                - x_hat * (gradOutput * x_hat).sum(axis=0)
            )
        else:
            self.gradInput = gradOutput / np.sqrt(self.moving_variance + self.EPS)
        return self.gradInput

    def __repr__(self):
        return "BatchNormalization"


class Dropout(Module):
    def __init__(self, p=0.5):
        super(Dropout, self).__init__()

        self.p = p
        self.mask = None

    def updateOutput(self, input):
        if self.training:
            # keep an element with probability 1 - p, rescale the survivors
            self.mask = (np.random.rand(*input.shape) >= self.p) / (1 - self.p)
            self.output = input * self.mask
        else:
            self.output = input
        return self.output

    def updateGradInput(self, input, gradOutput):
        if self.training:
            self.gradInput = gradOutput * self.mask
        else:
            self.gradInput = gradOutput
        return self.gradInput

    def __repr__(self):
        return "Dropout"


class ReLU(Module):
    def __init__(self):
        super(ReLU, self).__init__()

    def updateOutput(self, input):
        self.output = np.maximum(input, 0)
        return self.output

    def updateGradInput(self, input, gradOutput):
        self.gradInput = np.multiply(gradOutput, input > 0)
        return self.gradInput

    def __repr__(self):
        return "ReLU"


class LeakyReLU(Module):
    def __init__(self, slope=0.03):
        super(LeakyReLU, self).__init__()

        self.slope = slope

    def updateOutput(self, input):
        self.output = np.where(input > 0, input, input * self.slope)
        return self.output

    def updateGradInput(self, input, gradOutput):
        self.gradInput = gradOutput * np.where(input > 0, 1, self.slope)
        return self.gradInput

    def __repr__(self):
        return "LeakyReLU"

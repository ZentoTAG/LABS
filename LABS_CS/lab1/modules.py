import numpy as np


class Module:
    def __init__(self):
        self.output = None
        self.gradInput = None
        self.training = True

    def forward(self, x):
        return self.updateOutput(x)

    def backward(self, x, g):
        self.updateGradInput(x, g)
        self.accGradParameters(x, g)
        return self.gradInput

    def updateOutput(self, x): pass
    def updateGradInput(self, x, g): pass
    def accGradParameters(self, x, g): pass
    def zeroGradParameters(self): pass
    def getParameters(self): return []
    def getGradParameters(self): return []
    def train(self): self.training = True
    def evaluate(self): self.training = False

    def __repr__(self):
        return "Module"


class Sequential(Module):
    def __init__(self):
        super().__init__()
        self.modules = []

    def add(self, m):
        self.modules.append(m)

    def updateOutput(self, x):
        for m in self.modules:
            x = m.forward(x)
        self.output = x
        return x

    def backward(self, x, g):
        ys = [x]
        for m in self.modules:
            x = m.forward(x)
            ys.append(x)
        for i in range(len(self.modules) - 1, -1, -1):
            g = self.modules[i].backward(ys[i], g)
        self.gradInput = g
        return g

    def zeroGradParameters(self):
        for m in self.modules:
            m.zeroGradParameters()

    def getParameters(self):
        return [m.getParameters() for m in self.modules]

    def getGradParameters(self):
        return [m.getGradParameters() for m in self.modules]

    def train(self):
        super().train()
        for m in self.modules:
            m.train()

    def evaluate(self):
        super().evaluate()
        for m in self.modules:
            m.evaluate()

    def __repr__(self):
        return "".join(str(m) + "\n" for m in self.modules)

    def __getitem__(self, i):
        return self.modules[i]

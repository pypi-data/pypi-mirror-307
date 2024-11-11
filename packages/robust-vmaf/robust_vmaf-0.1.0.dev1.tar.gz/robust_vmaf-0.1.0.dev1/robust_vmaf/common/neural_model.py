import torch

class NeuralPredictor(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.lin1 = torch.nn.LazyLinear(100, bias=True)
        self.lin2 = torch.nn.LazyLinear(100, bias=True)
        self.lin3 = torch.nn.LazyLinear(1, bias=True)

    def forward(self, X):
        X = torch.nn.functional.relu(self.lin1(X))
        X = torch.nn.functional.relu(self.lin2(X))
        X = self.lin3(X)
        return X

    def predict(self, raw_features):
        return self.forward(torch.from_numpy(raw_features)).detach().numpy().flatten()

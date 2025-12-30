import math
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
class NN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, depth, act=torch.nn.Tanh):
        super(NN, self).__init__()
        layers = [('input', torch.nn.Linear(input_size, hidden_size))]
        layers.append(('input_activation', act()))
        for i in range(depth):
            layers.append(('hidden_%d' % i, torch.nn.Linear(hidden_size, hidden_size)))
            layers.append(('activation_%d' % i, act()))
        layers.append(('output', torch.nn.Linear(hidden_size, output_size)))
        layerDict = OrderedDict(layers)
        self.layers = torch.nn.Sequential(layerDict)
    def forward(self, x):
        out = self.layers(x)
        return out
class Net:
    def __init__(self):
        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.model = NN(input_size=2, hidden_size=20, output_size=1, depth=4, act=torch.nn.Tanh).to(device)
        self.h = 0.1
        self.k = 0.1
        x = torch.arange(-1 + self.h, 1, self.h)
        t = torch.arange(0 + self.k, 1 + self.k, self.k)
        self.X = torch.stack(torch.meshgrid(x, t)).reshape(2, -1).T
        bc1 = torch.stack(torch.meshgrid(torch.tensor([-1], dtype=t.dtype), t)).reshape(2, -1).T
        bc2 = torch.stack(torch.meshgrid(torch.tensor([1], dtype=t.dtype), t)).reshape(2, -1).T
        x0 = torch.cat([torch.tensor([-1]), x, torch.tensor([1])])
        ic = torch.stack(torch.meshgrid(x0, torch.tensor([0], dtype=x.dtype))).reshape(2, -1).T
        self.X_train = torch.cat([bc1, bc2, ic])
        y_bc1 = torch.zeros(len(bc1))
        y_bc2 = torch.zeros(len(bc2))
        y_ic = torch.cos(math.pi/2 * ic[:, 0])
        self.y_train = torch.cat([y_bc1, y_bc2, y_ic]).unsqueeze(1)
        self.X = self.X.to(device)
        self.X_train = self.X_train.to(device)
        self.y_train = self.y_train.to(device)
        self.X.requires_grad = True
        self.criterion = torch.nn.MSELoss()
        self.iter = 1
        self.optimizer = torch.optim.LBFGS(
            self.model.parameters(),
            lr=1.0,
            max_iter=50000,
            max_eval=50000,
            history_size=50,
            tolerance_grad=1e-7,
            tolerance_change=1.0 * np.finfo(float).eps,
            line_search_fn="strong_wolfe",
        )
        self.adam = torch.optim.Adam(self.model.parameters())

    def loss_func(self):
        self.adam.zero_grad()
        self.optimizer.zero_grad()
        y_pred = self.model(self.X_train)
        loss_data = self.criterion(y_pred, self.y_train)
        u = self.model(self.X)
        du_dX = torch.autograd.grad(
            inputs=self.X,
            outputs=u,
            grad_outputs=torch.ones_like(u),
            retain_graph=True,
            create_graph=True
        )[0]
        du_dt = du_dX[:, 1]
        du_dx = du_dX[:, 0]
        du_dxx = torch.autograd.grad(
            inputs=self.X,
            outputs=du_dX,
            grad_outputs=torch.ones_like(du_dX),
            retain_graph=True,
            create_graph=True
        )[0][:, 0]
        loss_pde = self.criterion(du_dt + u.squeeze() * du_dx, 0.01 / math.pi * du_dxx)
        loss = loss_pde + loss_data
        loss.backward()
        if self.iter % 100 == 0:
            print(self.iter, loss.item())
        self.iter += 1
        return loss

    def train(self):
        self.model.train()
        for i in range(1000):
            self.adam.step(self.loss_func)
        self.optimizer.step(self.loss_func)

    def eval_(self):
        self.model.eval()
net = Net()
net.train()
h = 0.01
k = 0.01
xx = torch.arange(-1, 1 + h, h)
tt = torch.arange(0, 1 + k, k)
X = torch.stack(torch.meshgrid(xx, tt)).reshape(2, -1).T
X = X.to(net.X.device)
model = net.model
model.eval()
with torch.no_grad():
    u_pred = model(X).reshape(len(xx), len(tt)).cpu().numpy()
plt.figure(figsize=(12, 6))
plt.contourf(X[:, 1].reshape(len(xx), len(tt)), X[:, 0].reshape(len(xx), len(tt)), u_pred, levels=200, cmap='jet')
plt.colorbar()
plt.title('u(x,t)')
plt.xlabel('t (s)')
plt.ylabel('x (m)')
plt.show()
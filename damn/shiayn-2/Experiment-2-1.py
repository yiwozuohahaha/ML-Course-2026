import torch
data = torch.tensor([1.,1.,0.,1.,0.])
p_mle = torch.mean(data)
alpha = 2
beta = 2
p_map = (torch.sum(data)+alpha-1)/(len(data)+alpha+beta-2)
print("MLE =",p_mle.item())
print("MAP =",p_map.item())

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta
data = np.array([1,1,0,1,0])
N = len(data)
sum_x = np.sum(data)
p = np.linspace(0,1,100)
likelihood = p**sum_x*(1-p)**(N-sum_x)
prior = beta.pdf(p,2,2)
posterior = p**(sum_x+1)*(1-p)**(N-sum_x+1)
p_mle = sum_x/N
p_map = (sum_x+1)/(N+2)
plt.plot(p,likelihood,label="Likelihood")
plt.plot(p,prior,label="Prior")
plt.plot(p,posterior,label="Posterior")
plt.axvline(p_mle,color='r',linestyle='--',label="MLE")
plt.axvline(p_map,color='g',linestyle='--',label="MAP")
plt.legend()
plt.title("MLE vs MAP")
plt.grid()
plt.show()


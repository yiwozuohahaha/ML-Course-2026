import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

X = np.array([[1,2],[2,3],[3,3],[6,5],[7,7],[8,6]])
y = np.array([0,0,0,1,1,1])

xx,yy = np.meshgrid(np.linspace(0,10,200),
                    np.linspace(0,10,200))
for k in [1,3,5]:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X,y)

    Z = model.predict(np.c_[xx.ravel(),yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure()
    plt.contourf(xx,yy,Z,alpha=0.3)
    plt.scatter(X[:,0],X[:,1],c=y)
    plt.title(f"K = {k}")
plt.show()
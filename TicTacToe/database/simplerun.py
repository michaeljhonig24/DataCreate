import numpy.linalg as la
import numpy as np
x = np.array([[3, 1, 1], [2,4,2], [-1,-1, 1]])

eigenvalues, eigenvectors = la.eig(x)

print("Eigenvalues:")
print(eigenvalues)

print("Eigenvectors:")
print(eigenvectors)


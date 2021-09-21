import numpy as np
import imageio


def power_iteration(A, Omega, power_iter=3):
    Y = A @ Omega
    for q in range(power_iter):
        Y = A @ (A.T @ Y)
    Q, _ = np.linalg.qr(Y)
    return Q


def rsvd(A, Omega):
    Q = power_iteration(A, Omega)
    B = Q.T @ A
    u_tilde, s, v = np.linalg.svd(B, full_matrices=0)
    u = Q @ u_tilde
    return u, s, v


image = imageio.imread('./images-dataset/sub1/11.jpg')
A = image[:, :, 1]

rank = 1000

Omega = np.random.randn(A.shape[1], rank)
u, s, v = rsvd(A, Omega)

a = u[:, : rank] @ np.diag(s[: rank]) @ v[: rank, :]
imageio.imwrite('resultest.jpg', a.astype(np.uint8))




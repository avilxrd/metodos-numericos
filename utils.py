import numpy as np

# Resolve o sistema triangular inferior L * x = b.
def resolver_triangular_inferior(L, b):
    L = np.asarray(L, dtype=float)
    b = np.asarray(b, dtype=float)
    if L.ndim != 2 or L.shape[0] != L.shape[1] or b.ndim != 1 or b.size != L.shape[0]:
        raise ValueError("L deve ser quadrada e compatível com b.")
    if not np.isfinite(L).all() or not np.isfinite(b).all():
        raise ValueError("L e b devem conter apenas valores finitos.")

    n = len(b)
    x = np.zeros(n)
    
    for i in range(n):
        soma = sum(L[i, j] * x[j] for j in range(i))
        
        if np.isclose(L[i, i], 0.0, atol=1e-12):
            raise ValueError("Pivô nulo ou muito próximo de zero.")
        
        x[i] = (b[i] - soma) / L[i, i]

    return x

# Resolve o sistema triangular superior U * x = b.
def resolver_triangular_superior(U, b):
    U = np.asarray(U, dtype=float)
    b = np.asarray(b, dtype=float)
    if U.ndim != 2 or U.shape[0] != U.shape[1] or b.ndim != 1 or b.size != U.shape[0]:
        raise ValueError("U deve ser quadrada e compatível com b.")
    if not np.isfinite(U).all() or not np.isfinite(b).all():
        raise ValueError("U e b devem conter apenas valores finitos.")

    n = len(b)
    x = np.zeros(n)
    
    for i in range(n - 1, -1, -1):
        soma = sum(U[i, j] * x[j] for j in range(i + 1, n))
        
        if np.isclose(U[i, i], 0.0, atol=1e-12):
            raise ValueError("Pivô nulo ou muito próximo de zero.")
        
        x[i] = (b[i] - soma) / U[i, i]
    
    return x

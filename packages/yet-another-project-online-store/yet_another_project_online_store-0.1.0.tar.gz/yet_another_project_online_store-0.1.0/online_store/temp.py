import numpy as np
from sympy import Matrix

def basis_of_nullspace(A):
    """
    Находит базис нуль-пространства матрицы A.

    Args:
        A: Матрица NumPy или SymPy.

    Returns:
        Список векторов NumPy, образующих базис нуль-пространства. 
        Возвращает пустой список, если нуль-пространство содержит только нулевой вектор.
    """

    try:
        # Проверяем, является ли A матрицей SymPy. Если да, преобразуем в NumPy.
        A = np.array(A).astype(float)
    except TypeError:
        pass  # A уже матрица NumPy

    _, s, vh = np.linalg.svd(A)
    
    # Определяем ранг матрицы (число ненулевых сингулярных значений)
    rank = np.sum(s > 1e-10) # используем небольшой порог для учета ошибок округления
    
    null_space_dim = A.shape[1] - rank

    if null_space_dim == 0:
        return []  # Нуль-пространство содержит только нулевой вектор
    else:
        basis = vh[rank:].conj().T
        return [b for b in basis]




A = np.array([[2, 1, 3, 0, 7],
              [1, 2, 0, 1, 4],
              [0, 1, -1, 1, 0]])

basis = basis_of_nullspace(A)

if basis:
    print("Базис нуль-пространства:")
    for vector in basis:
        print(vector)
else:
    print("Нуль-пространство содержит только нулевой вектор.")

#  Проверка через SymPy для более точного результата, особенно с дробными числами
A_sympy = Matrix(A)
nullspace_sympy = A_sympy.nullspace()

if nullspace_sympy:
    print("\nБазис нуль-пространства (SymPy):")
    for vector in nullspace_sympy:
        print(np.array(vector).astype(float).flatten()) # Преобразуем в NumPy array
else:
    print("\nНуль-пространство содержит только нулевой вектор (SymPy).")
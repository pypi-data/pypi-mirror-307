import numpy as np
from sklearn.covariance import MinCovDet
from math import comb
from scipy import stats

def detec_outliers(hw_matrix, percentil):
    """
    Detecta outliers en una matriz de datos utilizando la distancia de Mahalanobis.

    Args:
        hw_matrix (np.array): Matriz de datos (numpy array) donde se buscan outliers.
        percentil (float): Percentil para determinar el umbral de distancia de Mahalanobis. Por defecto es 95.

    Returns:
        np.array: Índices de los outliers en la matriz.
    """
    mcd = MinCovDet().fit(hw_matrix)
    dist = mcd.mahalanobis(hw_matrix)
    umbral = np.percentile(dist, percentil)
    outliers = np.where(dist > umbral)[0]
    return outliers

def cal_random_probability(m,n, u_):
    C = comb(m+n,m) # CORREGIDO
    u_ += 1

    # Calcula la suma en la fórmula de la probabilidad de aleatoriedad
    sum_f = 0
    for u in range(2, u_):
        if u % 2 == 0:
            k = u // 2
            f_u = 2 * comb(m-1, k-1) * comb(n-1, k-1)
        else:
            k = (u+1) // 2
            f_u = comb(m-1, k-1) * comb(n-1, k-2) + comb(m-1, k-2) * comb(n-1, k-1)
        sum_f += f_u

    # Calcula la probabilidad de aleatoriedad
    p = 1/C * sum_f

    return 

def durbin_watson(residuales):
    diff_residuales = np.diff(residuales)
    numerador = np.sum(diff_residuales ** 2)
    denominador = np.sum(residuales ** 2)
    d = numerador / denominador
    return d

def calculate_dL(residuos, k):
    n = len(residuos)
    alpha = 0.05
    critical_value = stats.f.ppf(1 - alpha/2, k, n - k - 1)
    return 2 - 2 * critical_value

def calculate_dU(residuos, k):
    n = len(residuos)
    alpha = 0.05
    critical_value = stats.f.ppf(alpha/2, k, n - k - 1)
    return 2 - 2 * critical_value


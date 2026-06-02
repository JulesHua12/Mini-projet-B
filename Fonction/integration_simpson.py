"""
Module : integration_simpson.py
MGA 802 - Mini-Projet B

Implémentation de la méthode d'intégration numérique de Simpson
en Python de base et avec NumPy.
"""

import numpy as np
import timeit


# ─────────────────────────────────────────────
#  Définition de la fonction et solution exacte
# ─────────────────────────────────────────────

def f(x, p1, p2, p3, p4):
    """Évalue le polynôme f(x) = p1 + p2*x + p3*x^2 + p4*x^3."""
    return p1 + p2 * x + p3 * x**2 + p4 * x**3


def solution_analytique(a, b, p1, p2, p3, p4):
    """
    Calcule la solution analytique (exacte) de l'intégrale de f sur [a, b].

    Intégrale de (p1 + p2*x + p3*x^2 + p4*x^3) dx
      = p1*x + p2/2 * x^2 + p3/3 * x^3 + p4/4 * x^4  + C

    Paramètres
    ----------
    a, b : bornes d'intégration
    p1, p2, p3, p4 : coefficients du polynôme

    Retourne
    --------
    float : valeur exacte de l'intégrale
    """
    def antiderivee(x):
        return p1 * x + (p2 / 2) * x**2 + (p3 / 3) * x**3 + (p4 / 4) * x**4

    return antiderivee(b) - antiderivee(a)


def calcul_erreur(I_numerique, I_exact):
    """
    Calcule l'erreur absolue entre l'intégrale numérique et la solution exacte.

    Paramètres
    ----------
    I_numerique : valeur approchée
    I_exact : valeur de référence analytique

    Retourne
    --------
    float : erreur absolue |I_numerique - I_exact|
    """
    return abs(I_numerique - I_exact)


# ─────────────────────────────────────────────
#  Méthode de Simpson — Python de base
# ─────────────────────────────────────────────

def simpson_python(a, b, n, p1, p2, p3, p4):
    """
    Intégration numérique par la méthode de Simpson (Python de base).

    La formule pour chaque segment [x_i, x_{i+1}] est :
        T = (h/6) * [f(x_i) + 4*f((x_i + x_{i+1})/2) + f(x_{i+1})]

    Paramètres
    ----------
    a, b : bornes d'intégration
    n    : nombre de segments
    p1, p2, p3, p4 : coefficients du polynôme

    Retourne
    --------
    float : approximation de l'intégrale
    """
    h = (b - a) / n          # largeur d'un segment
    somme = 0.0

    for i in range(n):
        x_gauche = a + i * h
        x_droite = x_gauche + h
        x_milieu = (x_gauche + x_droite) / 2.0

        somme += (h / 6.0) * (
            f(x_gauche, p1, p2, p3, p4)
            + 4.0 * f(x_milieu, p1, p2, p3, p4)
            + f(x_droite,  p1, p2, p3, p4)
        )

    return somme


def erreur_simpson_python(n, a, b, p1, p2, p3, p4):
    """
    Retourne l'erreur absolue de la méthode de Simpson (Python) pour n segments.

    Paramètres
    ----------
    n : nombre de segments
    a, b, p1, p2, p3, p4 : paramètres de la fonction et de l'intervalle

    Retourne
    --------
    float : erreur absolue
    """
    I_exact = solution_analytique(a, b, p1, p2, p3, p4)
    I_num   = simpson_python(a, b, n, p1, p2, p3, p4)
    return calcul_erreur(I_num, I_exact)


# ─────────────────────────────────────────────
#  Méthode de Simpson — NumPy vectorisé
# ─────────────────────────────────────────────

def simpson_numpy(a, b, n, p1, p2, p3, p4):
    """
    Intégration numérique par la méthode de Simpson (NumPy vectorisé).

    Vectorisation : tous les segments sont traités simultanément avec
    des tableaux NumPy, ce qui évite la boucle Python explicite.

    Paramètres
    ----------
    a, b : bornes d'intégration
    n    : nombre de segments
    p1, p2, p3, p4 : coefficients du polynôme

    Retourne
    --------
    float : approximation de l'intégrale
    """
    h = (b - a) / n

    # Bornes gauches et droites de chaque segment
    x_gauche = np.linspace(a, b - h, n)          # shape (n,)
    x_droite = x_gauche + h                       # shape (n,)
    x_milieu = (x_gauche + x_droite) / 2.0       # shape (n,)

    # Évaluation vectorisée du polynôme
    f_g = p1 + p2 * x_gauche + p3 * x_gauche**2 + p4 * x_gauche**3
    f_m = p1 + p2 * x_milieu + p3 * x_milieu**2 + p4 * x_milieu**3
    f_d = p1 + p2 * x_droite + p3 * x_droite**2 + p4 * x_droite**3

    # Somme vectorisée
    return np.sum((h / 6.0) * (f_g + 4.0 * f_m + f_d))


def erreur_simpson_numpy(n, a, b, p1, p2, p3, p4):
    """
    Retourne l'erreur absolue de la méthode de Simpson (NumPy) pour n segments.

    Paramètres
    ----------
    n : nombre de segments
    a, b, p1, p2, p3, p4 : paramètres de la fonction et de l'intervalle

    Retourne
    --------
    float : erreur absolue
    """
    I_exact = solution_analytique(a, b, p1, p2, p3, p4)
    I_num   = simpson_numpy(a, b, n, p1, p2, p3, p4)
    return calcul_erreur(I_num, I_exact)


# ─────────────────────────────────────────────
#  Méthode de Simpson — scipy (pré-programmée)
# ─────────────────────────────────────────────

def simpson_scipy(a, b, n, p1, p2, p3, p4):
    """
    Intégration numérique avec scipy.integrate.simpson (méthode pré-programmée).

    scipy.integrate.simpson attend un vecteur de valeurs y évaluées sur
    des points uniformément espacés.

    Paramètres
    ----------
    a, b : bornes d'intégration
    n    : nombre de segments (nombre d'intervalles ; nb de points = n+1)
    p1, p2, p3, p4 : coefficients du polynôme

    Retourne
    --------
    float : approximation de l'intégrale
    """
    from scipy.integrate import simpson as scipy_simpson

    # n+1 points pour n segments
    x = np.linspace(a, b, n + 1)
    y = p1 + p2 * x + p3 * x**2 + p4 * x**3

    return float(scipy_simpson(y, x=x))


def erreur_simpson_scipy(n, a, b, p1, p2, p3, p4):
    """
    Retourne l'erreur absolue de la méthode de Simpson (scipy) pour n segments.

    Paramètres
    ----------
    n : nombre de segments
    a, b, p1, p2, p3, p4 : paramètres de la fonction et de l'intervalle

    Retourne
    --------
    float : erreur absolue
    """
    I_exact = solution_analytique(a, b, p1, p2, p3, p4)
    I_num   = simpson_scipy(a, b, n, p1, p2, p3, p4)
    return calcul_erreur(I_num, I_exact)


# ─────────────────────────────────────────────
#  Mesure du temps d'exécution
# ─────────────────────────────────────────────

def mesurer_temps_simpson(methode, n_values, a, b, p1, p2, p3, p4,
                          nb_repetitions=100):
    """
    Mesure le temps d'exécution moyen (timeit) d'une méthode Simpson
    pour une liste de valeurs de n.

    Paramètres
    ----------
    methode        : fonction d'intégration à tester (callable)
    n_values       : liste/array du nombre de segments à tester
    a, b           : bornes d'intégration
    p1, p2, p3, p4 : coefficients du polynôme
    nb_repetitions : nombre de répétitions pour timeit

    Retourne
    --------
    list[float] : temps moyen en secondes pour chaque n
    """
    temps = []
    for n in n_values:
        t = timeit.timeit(
            lambda: methode(a, b, n, p1, p2, p3, p4),
            number=nb_repetitions
        ) / nb_repetitions
        temps.append(t)
    return temps
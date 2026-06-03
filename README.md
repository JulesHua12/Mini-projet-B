# Mini-projet-B# MGA 802 — Mini-Projet B : Intégration numérique

Réalisé par l'équipe 1 : M. Dubois, J. Hua, A. Hallonet

---

## Description

Ce projet compare trois méthodes d'intégration numérique appliquées à un polynôme du 3e ordre :

```
f(x) = p1 + p2·x + p3·x² + p4·x³
```

Chaque méthode est implémentée en **Python de base** et avec **NumPy** (vectorisé).
Les méthodes des trapèzes et de Simpson incluent aussi une version **SciPy** (pré-programmée).

---

## Structure du projet

```
Mini-projet-B/
├── main.py                        # Point d'entrée — lance tous les calculs et génère les graphiques
├── README.md
├── rapport/
│   └── Equipe_1_MGA802_ProjetB.pdf
└── Fonction/
    ├── __init__.py
    ├── integration_rectangle.py   # Méthode des rectangles (point milieu)
    ├── integration_trapeze.py     # Méthode des trapèzes
    └── integration_simpson.py     # Méthode de Simpson + SciPy
```

---

## Prérequis

Python 3.9 ou plus récent, avec les bibliothèques suivantes :

```
numpy
matplotlib
scipy
timeit  (module standard, inclus avec Python)
```

Installation des dépendances :

```bash
pip install numpy matplotlib scipy
```

---

## Utilisation

Depuis la racine du projet :

```bash
python main.py
```

Le script affiche dans le terminal les résultats numériques pour `n = 10` segments, puis génère et sauvegarde quatre graphiques :

| Fichier généré                  | Contenu                                              |
|---------------------------------|------------------------------------------------------|
| `convergence_toutes_methodes.png` | Erreur absolue en fonction de n (log-log)          |
| `temps_toutes_methodes.png`       | Temps de calcul en fonction de n (log-log)         |
| `erreur_par_methode.png`          | Erreur par méthode et implémentation (n=10,100,1000)|
| `illustration_simpson.png`        | Visualisation des paraboles de Simpson (n=4,10,40) |

---

## Paramètres

Les paramètres du polynôme et de l'intervalle sont définis en haut de `main.py` :

```python
P1, P2, P3, P4 = 1.0, -2.0, 0.5, 0.3   # coefficients du polynôme
A, B           = -2.0, 3.0              # bornes d'intégration
N_BASE         = 10                     # nombre de segments de référence
NB_REPS        = 200                    # répétitions timeit
```

---

## Description des modules

### `Fonction/integration_rectangle.py`
Méthode des rectangles (point milieu). L'intervalle est divisé en `n` segments, la fonction est évaluée au centre de chaque segment.

Fonctions principales :
- `rectangles_python(a, b, n, p1, p2, p3, p4)` — implémentation boucle `for`
- `rectangles_numpy(a, b, n, p1, p2, p3, p4)` — implémentation vectorisée NumPy
- `solution_analytique(a, b, p1, p2, p3, p4)` — solution exacte par la primitive
- `erreur_rect_python / erreur_rect_numpy` — erreur absolue pour un `n` donné
- `mesurer_temps_rect(methode, n_values, ...)` — mesure `timeit` sur une liste de `n`
- `demo_rectangles(a, b, p1, p2, p3, p4, n)` — affichage formaté des résultats

### `Fonction/integration_trapeze.py`
Méthode des trapèzes. Chaque segment est approché par un trapèze reliant `f(x_i)` à `f(x_{i+1})`.

Fonctions principales :
- `trapeze_python(a, b, n, p1, p2, p3, p4)` — implémentation boucle `for`
- `trapeze_numpy(a, b, n, p1, p2, p3, p4)` — implémentation vectorisée NumPy
- `erreur_trapeze_python / erreur_trapeze_numpy` — erreur absolue pour un `n` donné
- `mesurer_temps_trapeze(methode, a, b, n, ...)` — mesure `timeit`
- `demo_trapeze(a, b, n, p1, p2, p3, p4, nb_repetitions)` — affichage formaté

### `Fonction/integration_simpson.py`
Méthode de Simpson. Une parabole de degré 2 est ajustée sur chaque segment via trois points (gauche, milieu, droite).

Fonctions principales :
- `simpson_python(a, b, n, p1, p2, p3, p4)` — implémentation boucle `for`
- `simpson_numpy(a, b, n, p1, p2, p3, p4)` — implémentation vectorisée NumPy
- `simpson_scipy(a, b, n, p1, p2, p3, p4)` — via `scipy.integrate.simpson`
- `erreur_simpson_python / erreur_simpson_numpy / erreur_simpson_scipy`
- `mesurer_temps_simpson(methode, n_values, ...)` — mesure `timeit` sur une liste de `n`

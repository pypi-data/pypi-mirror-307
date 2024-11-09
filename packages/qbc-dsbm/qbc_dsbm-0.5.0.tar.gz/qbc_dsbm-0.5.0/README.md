# Quasi bi-clique and the densest sub-binary matrix problem modelling

## Installation

For now, we don't have a PyPI package, we must install it manually.

1. Clone from GitLab

    ```sh
    git clone git@gitlab.com:vepain/quasiblique_dsbm.git
    cd quasiblique_dsbm
    ```

2. *(Optionally)* Install [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
3. Create the virtual environment:

    ```sh
    conda env create -f config/condaenv_310.yml --prefix ./.condaenv_310
    ```

4. Source the virtual environment:

    ```sh
    conda activate ./.condaenv_310
    ```

### Upgrade the package

1. First pull the GIT modifications
2. Make sure you are in your virtual environment:

    ```sh
    conda activate ./.condaenv_310
    ```

3. Upgrade the python package:

    ```sh
    pip install . --upgrade
    ```

## Usage

Require: All the matrices must have row and column headers

### Get helped

```sh
qbc-dsbm --help  # global help
qbc-dsbm unique --help  # help for the unique strategy
qbc-dsbm divcqr --help  # help for the divide-and-conquer strategy
```

### To test

The results are in generated directories.
Some stats are found in the `YAML` file.

#### Testing the unique strategy

It creates the output directory: `tests/example_unique_result`, where in there are the files:

* `unique_strategy.yaml` for the stats;
* `result_bin_matrix.csv` that contains the resulting sub-bin matrix.

```sh
./tests/example_unique.sh
```

#### Testing the divide-and-conquer strategy

It creates the output directory: `tests/example_divcqr_result`, where in there are the files:

* `divcqr_strategy.yaml` for the stats;
* `result_bin_matrix.csv` that contains the resulting sub-bin matrix.

```sh
./tests/example_divcqr.sh
```

#### Testing unique comparison benchmark

It creates an output directory in `benchmarks` (e.g. `benchmark-2024-04-03T18:48:18`).

```sh
./benchmarks/unique_comparison/run_4_8_2_04_01_grb.sh
```

To format the stats in CSV files!

```sh
python3.10 benchmarks/unique_comparison/yaml_to_csv.py benchmarks/unique_comparison/benchmark-2024-04-03T18:48:18/
```

### Useful scripts

You can find all these scripts in the `scripts` directory.
Please make sure you have installed `qbc_dsbm` in your current virtual environment.

#### Python script to get stats of a binary matrix

```sh
python3.10 scripts/stats_of_bin_matrix.py matrix.csv output_directory_path
python3.10 scripts/stats_of_bin_matrix.py -h  # Help
```

#### Python script to transform non-binary matrix to binary matrix

```sh
python3.10 scripts/to_bin_matrix.py matrix.csv bin_matrix.csv "{-1: 1, -2: 0}"
python3.10 scripts/to_bin_matrix.py -h  # Help
```

#### Produce the binary matrix column-difference between two binary matrices

```sh
python3.10 scripts/binmatrix_coldiff.py binmatrix.csv sub_binmatrix.csv coldiff_binmatrix.csv
python3.10 scripts/binmatrix_coldiff.py -h  # Help
```

#### Produce the binary matrix row-intersection between two binary matrices

```sh
python3.10 scripts/binmatrix_rowinter.py binmatrix.csv sub_binmatrix.csv rowinter_binmatrix.csv
python3.10 scripts/binmatrix_rowinter.py -h  # Help
```

#### Python script to generate a binary matrix (The matrix name is `bin_matrix.csv`)

```sh
python3.10 scripts/generate_bin_matrix.py n_rows n_cols sparsity output_directory_path
python3.10 scripts/generate_bin_matrix.py -h  # Help
```

### Benchmarks

#### Unique

See `benchmarks/unique_comparison/run_4_8_2_04_01_grb.sh` for example.

To get helped:

```sh
python3.10 benchmarks/unique_comparison/run.py --help  # global help
python3.10 benchmarks/unique_comparison/run.py new --help  # help for a new benchmark
python3.10 benchmarks/unique_comparison/run.py continue --help  # help to continue an existing benchmark
```

<!-- LTeX: language=fr -->

## Contexte

* Problème bioinfo
* Problème optimal sans bruit
* Bruit bioinfo, donc quasibiclique
* Mais trop lourd
* Donc heuristique
* Déjà fait : réduction des données avec HCC, puis optimal

## Problème de la sous-matrice binaire complète (all-ones sub-matrix) (SMBC)

Deux variantes :

1. la sous-matrice avec suppression minimale de lignes et colonnes confondues
2. la sous-matrice avec suppression de poids minimal de lignes et colonnes
    * le poids d'une ligne resp. d'une colonne est la somme de ses coefficients égaux à 1
    * voir équivalence avec Egerváry's theorem for edge-weighted graphs

### Observations

#### Il n'y a pas d'équivalence entre le maximum matching/minimum vertex cover dans un bigraphe et le problème SMBC

L'approche de König semble fonctionner pour un sous-ensemble de matrices.
Il s'agirait de décrire ce sous-ensemble.

König peut renvoyer une matrice sans lignes ou sans colonnes (donc pas une matrice).
Cela s'explique par la modélisation

Le modèle de König complété avec des contraintes

## Analysing practically heuristic reducing approach

### Propositions

1. Utiliser large epsilon pour réduire taille des instances en essayant de garder la solution optimal dans les sous-instances pour appliquer problème optimal sur les sous-instances.
    1. Comment bien choisir l'epsilon plus large ? S'appuyer sur l'absence de correctif dans la fonction objective (car on peut compter deux fois la même cellule, car même ligne même colonne)
2. Utiliser solution-heuristique pour appliquer sur instance complète pour solver

### Méthodes et tâches

* [x] **VIC 1** Implémenter générateur Matrices binaires `fn(nrows, ncols, sparsicity)`
* [ ] **RUMEN** Adapter König avec ajout contraintes pour obtenir modèle exact
  * [ ] Vérifier expérimentalement si les variables restent entières (unimodularité)
  * [ ] Si semble garder unimodularité alors faire preuve
* [x] **VIC 2** Implémenter suite heuristique -> modèle exact
* [ ] Utiliser heuristique KNP
  * [ ] Accélérer heuristique KNP avec heuristique algo dédié
    * [ ] **VIC 4** Itérativement refaire KNP jusqu'à ce que l'epsilon *réel* soit inférieur à l'attendue
  * [ ] **VIC 3** ILP : obtenir borne inférieur en comptant les zeros qu'une demie-fois ou fois la sparsité des lignes et des colonnes dans contraintes (17)
  * [ ] Le but : obtenir rapidement une solution avec un epsilon réel >= epsilon opti voulu et résoudre le problème optimal avec la sous-instance (on s'attend à ce que cette sous-instance renvoie la solution optimale de l'instance complète)
  * [ ] Voir efficacité algo dédié sac à dos qui compterait les zeros comptés deux fois lors de la suppression lignes et colonne (faire en rust)
* [ ] Comparer Hiearchical Clustering (rearrangement des colonnes) avec les méthodes de suppression de colonnes

### Résultats

* Comparaison des ratios nombre de 0 sur nombre de 1 (sparsité/densité)
* Comparer les tailles
  * Nombre de lignes
  * Nombre de colonnes
  * nb lignes x nb colonnes (surface) : correspond au nombre d'arêtes dans la biclique pondérée-arrêtes associée à la matrice résultante (pondération équivaut à la valeur des cellules)
  * nb lignes + nb colonnes (semi-perimètre) : correspond au nombre de sommets dans la biclique pondérée-arrêtes associées à la matrice résultante
* Si mêmes tailles, nombre de mêmes lignes et nombre de mêmes colonnes sélectionnées ?
  * Ça pose la question de l'unicité de la solution du problème exacte

### Perspectives

* [ ] Comparer SAT formulation avec ILP pour cas binaire quasibiclique
  * [ ] QUID poids : SAT semble ne pas le gérer

### Production scientifique

* [ ] Papier journal/conf
  * [ ] Se comparer avec quasi-biclique
    * [ ] Quelle différence avec clique ?
  * [ ] Comparer méthode exact
    * [ ] c.f. <https://www.researchgate.net/publication/370946817_Optimization_problems_related_to_quasi-cliques?enrichId=rgreq-94751e1a95f42d6c0366ab147d09f6d5-XXX&enrichSource=Y292ZXJQYWdlOzM3MDk0NjgxNztBUzoxMTQzMTI4MTE2MDU5NDY2NEAxNjg0Nzg1ODAyMzY2&el=1_x_3&_esc=publicationCoverPdf>
  * [ ] Quels sont les champs d'application quasi-biclique ?

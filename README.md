# Projet d'Optimisation : Problème du Voyageur de Commerce (TSP)

Ce projet implémente et compare plusieurs algorithmes de métaheuristiques pour résoudre le Problème du Voyageur de Commerce (TSP - Traveling Salesperson Problem). 

Les algorithmes développés visent à minimiser la distance totale d'un parcours reliant un ensemble de villes, en revenant au point de départ.

## Architecture du Projet

Le code a été découpé de manière modulaire pour séparer la logique des algorithmes, la manipulation des données et le protocole de test :

* `experiment.py` : Le point d'entrée du programme. Il exécute le protocole expérimental complet (30 runs indépendants) et affiche les statistiques (Meilleur coût, moyenne, écart-type, temps CPU).
* `algorithms.py` : Contient les classes orientées objet des algorithmes de résolution (`HillClimbing`, `MultiStartHillClimbing`, `SimulatedAnnealing`).
* `utils.py` : La boîte à outils contenant les fonctions d'évaluation (calcul de distance) et de génération de voisinages (Swap).
* `data_loader.py` : Le script chargé de lire et parser les fichiers de coordonnées au format standard TSPLIB.
* `data/` : Le dossier contenant les instances de test (ex: `berlin52.tsp`).

## Prérequis

* **Python 3.x** installé sur votre machine.
* Aucune bibliothèque externe n'est requise pour l'exécution principale (seuls les modules natifs `math`, `random`, `time`, `os` et `statistics` sont utilisés).

## Comment exécuter le projet

1.  Ouvrez un terminal ou une invite de commande.
2.  Naviguez jusqu'au dossier racine de ce projet.
3.  Assurez-vous que le dossier `data/` contient bien l'instance que vous souhaitez tester (par défaut `berlin52.tsp`).
4.  Lancez la commande suivante :

    ```bash
    python experiment.py
    ```

## Protocole Expérimental

Le script `experiment.py` va automatiquement tester les algorithmes suivants sur l'instance configurée :
1.  **Hill-Climbing (First Improvement)**
2.  **Hill-Climbing (Best Improvement)**
3.  **Multi-Start Hill-Climbing** (Budget : 10 départs par run)
4.  **Recuit Simulé (Simulated Annealing)** (Température initiale : 5000, alpha : 0.9995)

Pour garantir la fiabilité scientifique des résultats, chaque algorithme est lancé **30 fois de manière indépendante**. Le programme affichera ensuite dans la console le meilleur coût absolu, le coût moyen, l'écart-type et le temps de calcul moyen pour chaque approche.

## Changer d'instance de test

Si vous souhaitez tester une autre carte de villes (par exemple `ulysses22.tsp`), il vous suffit de :
1.  Placer le fichier `.tsp` dans le dossier `data/`.
2.  Ouvrir le fichier `experiment.py`.
3.  Modifier la variable `filename` au début de la fonction `main()` :
    ```python
    filename = "data/ulysses22.tsp"
    ```
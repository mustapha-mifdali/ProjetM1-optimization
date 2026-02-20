# main.py
import os
import time
import statistics
from utils import create_initial_tour
from algorithms import HillClimbing, MultiStartHillClimbing, SimulatedAnnealing
from data_loader import load_tsplib_data, calculate_distance_matrix_from_coords

def evaluer_algorithme(nom_algo, classe_algo, distance_matrix, num_villes, kwargs_algo, num_runs=30):
    """
    Exécute un algorithme 'num_runs' fois de manière indépendante et calcule les statistiques.
    """
    couts = []
    temps_exec = []
    
    print(f"--- Lancement de {nom_algo} ({num_runs} runs indépendants) ---")
    
    for i in range(num_runs):
        # 1. Générer un nouveau point de départ aléatoire pour CE run
        tour_initial = create_initial_tour(num_villes)
        
        # 2. Préparer l'algorithme (Multi-Start gère son propre tour initial)
        if nom_algo == "Multi-Start Hill-Climbing":
            algo = classe_algo(distance_matrix, num_villes, **kwargs_algo)
        else:
            algo = classe_algo(distance_matrix, tour_initial, **kwargs_algo)
            
        # 3. Chronométrer l'exécution (Temps CPU)
        debut = time.time()
        tour_final, cout_final = algo.run()
        fin = time.time()
        
        # 4. Sauvegarder les résultats de ce run
        couts.append(cout_final)
        temps_exec.append(fin - debut)

    # 5. Calculer les statistiques demandées par le professeur
    meilleur_cout = min(couts)
    cout_moyen = statistics.mean(couts)
    ecart_type = statistics.stdev(couts) if num_runs > 1 else 0
    temps_moyen = statistics.mean(temps_exec)
    
    # 6. Afficher les résultats formatés
    print(f"Résultats pour {nom_algo} :")
    print(f"  -> Meilleur coût  : {meilleur_cout}")
    print(f"  -> Coût moyen     : {cout_moyen:.2f}")
    print(f"  -> Écart-type     : {ecart_type:.2f}")
    print(f"  -> Temps moyen    : {temps_moyen:.4f} secondes\n")
    
    return meilleur_cout, cout_moyen, ecart_type, temps_moyen

def main():
    # === 1. CHARGEMENT DE L'INSTANCE ===
    filename = "data/berlin52.tsp" 
    if not os.path.exists(filename):
        print(f"Erreur : Fichier {filename} introuvable.")
        return

    print(f"=== PROTOCOLE EXPÉRIMENTAL : Instance {filename} ===")
    coordinates = load_tsplib_data(filename)
    distance_matrix = calculate_distance_matrix_from_coords(coordinates)
    num_villes = len(coordinates)
    
    # Le budget de calcul est défini par les paramètres : 
    # - SA : Température et alpha définissent le nombre d'itérations.
    # - Multi-Start : num_starts=30 définit le budget.
    # - Le protocole impose 30 runs indépendants pour chaque.
    NB_RUNS = 30 
    
    # === 2. ÉVALUATION DES ALGORITHMES ===
    
    # 1. Hill-Climbing (First Improvement)
    evaluer_algorithme(
        nom_algo="HC (First Improvement)",
        classe_algo=HillClimbing,
        distance_matrix=distance_matrix,
        num_villes=num_villes,
        kwargs_algo={"mode": "first"},
        num_runs=NB_RUNS
    )
    
    # 2. Hill-Climbing (Best Improvement)
    evaluer_algorithme(
        nom_algo="HC (Best Improvement)",
        classe_algo=HillClimbing,
        distance_matrix=distance_matrix,
        num_villes=num_villes,
        kwargs_algo={"mode": "best"},
        num_runs=NB_RUNS
    )
    
    # 3. Multi-Start Hill-Climbing
    # evaluer_algorithme(
    #     nom_algo="Multi-Start Hill-Climbing",
    #     classe_algo=MultiStartHillClimbing,
    #     distance_matrix=distance_matrix,
    #     num_villes=num_villes,
    #     kwargs_algo={"num_starts": 10, "mode": "best"}, # Budget interne : 10 départs par run
    #     num_runs=NB_RUNS
    # )
    
    # 4. Recuit Simulé (Simulated Annealing)
    evaluer_algorithme(
        nom_algo="Recuit Simulé (SA)",
        classe_algo=SimulatedAnnealing,
        distance_matrix=distance_matrix,
        num_villes=num_villes,
        # On change alpha à 0.9995 pour qu'il tourne des milliers de fois !
        kwargs_algo={"T0": 5000, "alpha": 0.9995, "T_min": 0.1}, 
        num_runs=NB_RUNS
    )

if __name__ == "__main__":
    main()
# IA et Jeux - Robots réactifs, optimisation et Paintwars

Ce dépôt regroupe plusieurs travaux réalisés en Python autour de la robotique simulée et du jeu multi-agents.
L’objectif était d’explorer différents comportements de robots, depuis des stratégies réactives simples jusqu’à des approches d’optimisation et d’évaluation en tournoi.

## Contenu du projet

Le projet s’articule autour de trois axes principaux :

- **Comportements réactifs inspirés de Braitenberg**
  - attraction / évitement
  - interaction avec les murs
  - interaction avec les autres robots
  - architecture par subsomption

- **Optimisation de comportements**
  - recherche aléatoire
  - variantes de random search
  - algorithmes génétiques

- **Évaluation de stratégies dans un cadre de type Paintwars**
  - confrontation entre plusieurs agents
  - exécution sur différentes arènes
  - tournois automatiques

## Fichiers principaux

- `tetracomposibot.py` : simulateur principal
- `config_TP1.py` : configuration pour les comportements réactifs
- `config_TP2.py` : configuration pour les approches d’optimisation
- `config_Paintwars.py` : configuration pour un match Paintwars
- `config_Paintwars_eval.py` : configuration pour l’évaluation automatique
- `go_tournament` : script de lancement de plusieurs matchs
- `go_tournament_eval` : script d’évaluation sur plusieurs cartes
- `robot_*.py` : différentes stratégies / différents robots

## Prérequis

- Python 3
- `pygame`
- `numpy`
- `matplotlib`
- `numba`

## Installation

Cloner le dépôt puis installer les dépendances nécessaires :

```bash
pip3 install pygame numpy matplotlib numba
```

## Lancer le projet

### 1) Tester les comportements réactifs

Pour lancer une simulation avec les robots de type Braitenberg :

```bash
python3 tetracomposibot.py config_TP1
```

### 2) Tester les approches d’optimisation

Pour lancer une simulation orientée recherche / optimisation :

```bash
python3 tetracomposibot.py config_TP2
```

### 3) Lancer une confrontation Paintwars

Pour exécuter un match entre les agents définis dans la configuration Paintwars :

```bash
python3 tetracomposibot.py config_Paintwars
```

### 4) Lancer un tournoi automatique

Donner les droits d’exécution aux scripts si nécessaire :

```bash
chmod +x go_tournament
chmod +x go_tournament_eval
```

Puis lancer :

```bash
./go_tournament
```

ou

```bash
./go_tournament_eval
```

## Ce que ce projet met en avant

- mise en place de **robots réactifs** dans un environnement simulé
- comparaison de plusieurs **stratégies de déplacement et d’interaction**
- expérimentation de méthodes d’**optimisation de comportements**
- travail sur la **modularité du code**, avec séparation entre simulateur, configurations et agents

## Remarques

Selon la configuration choisie, l’affichage peut être plus ou moins rapide.  
Certaines exécutions sont pensées pour la visualisation, d’autres pour l’évaluation automatique.

## Auteure

**Belkiss Tiss**

Projet réalisé dans un cadre universitaire autour de l’IA, des agents et de la robotique simulée.

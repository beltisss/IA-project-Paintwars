# IA et Jeux — Robots réactifs, optimisation et Paintwars

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

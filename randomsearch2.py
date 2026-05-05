# randomsearch2.py
from robot import *
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "RandomSearch2"
    robot_id = -1
    iteration = 0

    param = []
    bestParam = []
    it_per_evaluation = 400
    trial = 0

    # Budget d'évaluations (nombre de stratégies différentes testées)
    max_trials = 500

    # Après la recherche, on rejoue le meilleur comportement pendant 1000 itérations, en boucle
    replay_it = 1000

    # Sauvegarde du meilleur individu trouvé
    best_score = -10**9
    best_trial = -1

    # --- Score incrémental (somme sur les itérations) ---
    prev_sum_t = 0.0
    prev_sum_r = 0.0
    current_score = 0.0

    # --- Exo2: 3 conditions initiales (orientations fixées et identiques pour tous les candidats) ---
    orientations = [0, 120, 240]     # tu peux changer ces valeurs, mais elles doivent rester fixes
    eval_index = 0                  # 0,1,2 : quelle orientation on est en train d'évaluer
    score_sum_3 = 0.0               # score total d'un comportement = somme des 3 évaluations

    # Mode replay
    replay_mode = False

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=400):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1

        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0

        self.it_per_evaluation = it_per_evaluation

        # Paramètres du perceptron: 8 poids/biais, chaque paramètre ∈ {-1,0,1}
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.bestParam = self.param[:]

        # Init score
        self.prev_sum_t = 0.0
        self.prev_sum_r = 0.0
        self.current_score = 0.0

        # Init exo2
        self.eval_index = 0
        self.score_sum_3 = 0.0

        self.replay_mode = False

        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        # reset du simulateur + remise à zéro des accumulateurs locaux de score
        super().reset()

        # Remise à zéro des compteurs utilisés pour le score incrémental
        self.prev_sum_t = 0.0
        self.prev_sum_r = 0.0
        self.current_score = 0.0

        # Exo2: on impose une orientation initiale dépendant de l'évaluation en cours
        # IMPORTANT: les 3 orientations restent les mêmes pour toutes les stratégies candidates.
        self.theta0 = self.orientations[self.eval_index]
        self.theta = self.theta0

    def _new_random_param(self):
        # Génère un nouveau comportement aléatoire
        self.param = [random.randint(-1, 1) for i in range(8)]

        # Petite contrainte utile: éviter les stratégies "rotation toujours nulle"
        if self.param[4] == 0 and self.param[5] == 0 and self.param[6] == 0 and self.param[7] == 0:
            self.param[6] = random.choice([-1, 1])

    def _update_score_incremental(self):
        dt = self.log_sum_of_translation - self.prev_sum_t
        dr = self.log_sum_of_rotation - self.prev_sum_r
        self.current_score += dt * (1 - abs(dr))
        self.prev_sum_t = self.log_sum_of_translation
        self.prev_sum_r = self.log_sum_of_rotation

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
        # Remarques:
        # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
        # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres (c'est un "Perceptron")

        self._update_score_incremental()

        # =========================
        # Phase REPLAY du meilleur
        # =========================
        if self.replay_mode == True:
            self.param = self.bestParam[:]
            if self.iteration > 0 and self.iteration % self.replay_it == 0:
                print("REPLAY BEST (infinite loop)")
                print("\tbest_trial          =", self.best_trial)
                print("\tbest_score          =", self.best_score)
                print("\tbest_parameters     =", self.bestParam)
                self.iteration += 1
                return 0, 0, True  # ask for reset

        # ==========================================
        # Phase RANDOM SEARCH avec 3 orientations
        # ==========================================
        if self.iteration % self.it_per_evaluation == 0:

            if self.iteration > 0:
                # Fin d'une des 3 évaluations: on ajoute au score total du candidat
                print("\tparameters           =", self.param)
                print("\ttranslations         =", self.log_sum_of_translation, "; rotations =", self.log_sum_of_rotation)
                print("\tdistance from origin =", math.sqrt((self.x - self.x_0) ** 2 + (self.y - self.y_0) ** 2))
                print("\tscore (this eval)    =", self.current_score)
                self.score_sum_3 += self.current_score

            # On passe à l'évaluation suivante (0->1->2)
            self.eval_index += 1

            # Si on n'a pas encore fait les 3 évaluations, on reset avec la prochaine orientation
            if self.eval_index < 3:
                self.iteration += 1
                return 0, 0, True  # ask for reset (reset mettra theta0 correctement)

            # Sinon, on a terminé les 3 évaluations pour ce candidat
            total_score = self.score_sum_3
            print("\ttotal score (3 eval) =", total_score)

            # Mise à jour du meilleur
            if total_score > self.best_score:
                self.best_score = total_score
                self.bestParam = self.param[:]
                self.best_trial = self.trial
                print("NEW BEST FOUND!")
                print("\tbest_trial          =", self.best_trial)
                print("\tbest_score          =", self.best_score)
                print("\tbest_parameters     =", self.bestParam)

            # On prépare le prochain candidat si budget pas épuisé
            if self.trial < self.max_trials:
                self._new_random_param()
                self.trial += 1
                print("Trying strategy no.", self.trial)

                # IMPORTANT: on réinitialise les compteurs exo2 pour le prochain candidat
                self.eval_index = 0
                self.score_sum_3 = 0.0

                self.iteration += 1
                return 0, 0, True  # ask for reset

            # Budget épuisé: mode replay
            self.replay_mode = True
            self.param = self.bestParam[:]

            # En replay, on peut choisir une orientation fixe (par ex. la première)
            self.eval_index = 0
            self.score_sum_3 = 0.0

            self.iteration += 1
            return 0, 0, True  # ask for reset

        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        translation = math.tanh(
            self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right]
        )
        rotation = math.tanh(
            self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right]
        )

        # (optionnel) empêche le recul, pratique pour éviter l'oscillation avant/arrière
        translation = max(0.0, translation)

        if debug == True:
            if self.iteration % 100 == 0:
                print("Robot", self.robot_id, " (team " + str(self.team_name) + ")", "at step", self.iteration, ":")
                print("\tsensors (distance, max is 1.0)  =", sensors)
                print("\ttype (0:empty, 1:wall, 2:robot) =", sensor_view)
                print("\trobot's name (if relevant)      =", sensor_robot)
                print("\trobot's team (if relevant)      =", sensor_team)

        self.iteration += 1
        return translation, rotation, False


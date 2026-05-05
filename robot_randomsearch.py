# robot_randomsearch.py
from robot import * 
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "RandomSearch"
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

    # --- Variables pour calculer le score "au fil de l'eau" (somme sur toutes les itérations) ---
    # On mémorise les valeurs précédentes des logs pour récupérer les "deltas" par pas de temps.
    prev_sum_t = 0.0
    prev_sum_r = 0.0
    current_score = 0.0

    # --- Etat du robot ---
    # False: on est en phase d'exploration (random search)
    # True : on est en phase de démonstration (replay du meilleur)
    replay_mode = False

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=400):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0

        # Paramètres du perceptron: 8 poids/biais, chaque paramètre ∈ {-1,0,1}
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.bestParam = self.param[:]

        self.it_per_evaluation = it_per_evaluation

        # Initialisation des variables de score
        self.prev_sum_t = 0.0
        self.prev_sum_r = 0.0
        self.current_score = 0.0

        self.replay_mode = False

        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        # reset du simulateur + remise à zéro des accumulateurs locaux de score
        super().reset()
        self.prev_sum_t = 0.0
        self.prev_sum_r = 0.0
        self.current_score = 0.0

    def _new_random_param(self):
        # Génère un nouveau comportement aléatoire
        self.param = [random.randint(-1, 1) for i in range(8)]

        # Petite contrainte utile: éviter les stratégies "rotation toujours nulle"
        # (sinon le robot fonce tout droit, se bloque sur un mur, et le score plafonne vite)
        if self.param[4] == 0 and self.param[5] == 0 and self.param[6] == 0 and self.param[7] == 0:
            self.param[6] = random.choice([-1, 1])  # force au moins une influence capteur->rotation

    def _update_score_incremental(self):
        # Calcul du score comme demandé dans l'énoncé:
        # score = somme_sur_toutes_les_iterations ( translation_eff * (1 - abs(rotation_eff)) )
        #
        # IMPORTANT: translation_eff et rotation_eff sont des valeurs "effectives" (mesurées),
        # stockées dans log_sum_of_translation et log_sum_of_rotation.
        # On n'a pas l'historique complet, donc on calcule le delta à chaque pas:
        dt = self.log_sum_of_translation - self.prev_sum_t
        dr = self.log_sum_of_rotation - self.prev_sum_r

        # mise à jour du score cumulé
        self.current_score += dt * (1 - abs(dr))

        # mémorisation pour la prochaine itération
        self.prev_sum_t = self.log_sum_of_translation
        self.prev_sum_r = self.log_sum_of_rotation

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
        # Remarques:
        # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
        # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres (c'est un "Perceptron")

        # --- Mise à jour du score à chaque pas de temps (somme sur toutes les itérations) ---
        self._update_score_incremental()

        # =========================
        # Phase 2: REPLAY du meilleur
        # =========================
        # IMPORTANT: on gère le reset toutes les 1000 itérations ICI, en dehors du bloc "toutes les 400",
        # sinon 1000 ne tombe quasiment jamais pile sur un multiple de 400.
        if self.replay_mode == True:
            self.param = self.bestParam[:]  # on force le meilleur comportement

            # Toutes les replay_it itérations: reset pour rejouer proprement depuis la position initiale
            if self.iteration > 0 and self.iteration % self.replay_it == 0:
                print ("REPLAY BEST (infinite loop)")
                print ("\tbest_trial          =",self.best_trial)
                print ("\tbest_score          =",self.best_score)
                print ("\tbest_parameters     =",self.bestParam)
                self.iteration = self.iteration + 1
                return 0, 0, True # ask for reset

            # Sinon, on exécute normalement le contrôleur en bas du fichier
            # (pas besoin de repasser par l'évaluation toutes les 400 itérations)

        # ==========================================
        # Phase 1: RANDOM SEARCH (évaluations de 400)
        # ==========================================

        # toutes les X itérations: le robot est remis à sa position initiale de l'arène avec une orientation aléatoire
        if self.iteration % self.it_per_evaluation == 0:

                # --- Fin d'une évaluation: on calcule le score et on compare au meilleur ---
                if self.iteration > 0:

                    # Affichage des infos de fin d'évaluation (comme robot_optimize.py)
                    print ("\tparameters           =",self.param)
                    print ("\ttranslations         =",self.log_sum_of_translation,"; rotations =",self.log_sum_of_rotation) # *effective* translation/rotation (ie. measured from displacement)
                    print ("\tdistance from origin =",math.sqrt((self.x-self.x_0)**2+(self.y-self.y_0)**2))
                    print ("\tscore                =",self.current_score)

                    # Mise à jour du meilleur individu trouvé
                    if self.current_score > self.best_score:
                        self.best_score = self.current_score
                        self.bestParam = self.param[:]
                        self.best_trial = self.trial
                        print ("NEW BEST FOUND!")
                        print ("\tbest_trial          =",self.best_trial)
                        print ("\tbest_score          =",self.best_score)
                        print ("\tbest_parameters     =",self.bestParam)

                # --- Tant qu'on n'a pas épuisé le budget, on teste une nouvelle stratégie ---
                if self.trial < self.max_trials:
                    self._new_random_param()
                    self.trial = self.trial + 1
                    print ("Trying strategy no.",self.trial)

                    # Le reset remettra current_score/prev_sum_* à zéro via reset()
                    self.iteration = self.iteration + 1
                    return 0, 0, True # ask for reset

                # --- Budget épuisé: on passe en mode REPLAY ---
                self.replay_mode = True
                self.param = self.bestParam[:]  # on force le meilleur tout de suite
                self.iteration = self.iteration + 1
                return 0, 0, True # on reset pour repartir proprement au début du replay

        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        # Ici on utilise 3 senseurs (front_left, front, front_right) comme dans robot_optimize.py
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)

        self.iteration = self.iteration + 1

        return translation, rotation, False




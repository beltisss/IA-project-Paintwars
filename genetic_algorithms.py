# genetic_algorithms.py
from robot import * 
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "GeneticAlgo"
    robot_id = -1
    iteration = 0

    param = []
    bestParam = []
    it_per_evaluation = 400
    trial = 0   # ici "trial" = compteur de générations / évaluations (pour garder le style des prints)

    # Budget (nombre de générations / enfants évalués)
    max_trials = 500

    # Après la recherche, on rejoue le meilleur comportement pendant 1000 itérations, en boucle
    replay_it = 1000

    # --- Exo2: 3 conditions initiales (orientations fixées et identiques pour tous les candidats) ---
    orientations = [0, 120, 240]   # doivent rester les mêmes pour comparer les candidats
    eval_index = 0                 # 0,1,2 : quelle orientation on est en train d'évaluer
    score_sum_3 = 0.0              # score total d'un candidat = somme des 3 évaluations

    # --- Variables pour calculer le score "au fil de l'eau" (somme sur toutes les itérations) ---
    # On mémorise les valeurs précédentes des logs pour récupérer les "deltas" par pas de temps.
    prev_sum_t = 0.0
    prev_sum_r = 0.0
    current_score = 0.0

    # --- Algorithme génétique (mu=1 + lambda=1) ---
    # parent = individu courant
    parentParam = []
    parentScore = -10**9

    # enfant = mutation(parent) (un seul gène modifié)
    childParam = []
    evaluating_child = False  # False: on évalue le parent (au début), True: on évalue l'enfant

    # Sauvegarde du meilleur individu trouvé (ici ça sera le parent courant, mais on garde les variables explicites)
    best_score = -10**9
    best_trial = -1

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

        # Paramètres initiaux aléatoires (parent)
        self.parentParam = [random.randint(-1, 1) for i in range(8)]
        self.parentScore = -10**9

        # On commence en évaluant le parent
        self.evaluating_child = False
        self.param = self.parentParam[:]   # param est l'individu actuellement en cours d'évaluation

        # Meilleur (au début: inconnu)
        self.bestParam = self.parentParam[:]
        self.best_score = -10**9
        self.best_trial = -1

        # Init exo2
        self.eval_index = 0
        self.score_sum_3 = 0.0

        # Init score incrémental
        self.prev_sum_t = 0.0
        self.prev_sum_r = 0.0
        self.current_score = 0.0

        self.replay_mode = False
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        # reset du simulateur + remise à zéro des accumulateurs locaux de score
        super().reset()

        # Remise à zéro des compteurs utilisés pour le score incrémental
        self.prev_sum_t = 0.0
        self.prev_sum_r = 0.0
        self.current_score = 0.0

        # Exo2: orientation initiale imposée (comparabilité entre candidats)
        # En replay, on fixe une orientation unique (ici la première) pour "montrer" le meilleur.
        if self.replay_mode:
            self.theta0 = self.orientations[0]
        else:
            self.theta0 = self.orientations[self.eval_index]
        self.theta = self.theta0

    def _update_score_incremental(self):
        # score = somme_sur_toutes_les_iterations ( translation_eff * (1 - abs(rotation_eff)) )
        dt = self.log_sum_of_translation - self.prev_sum_t
        dr = self.log_sum_of_rotation - self.prev_sum_r
        self.current_score += dt * (1 - abs(dr))
        self.prev_sum_t = self.log_sum_of_translation
        self.prev_sum_r = self.log_sum_of_rotation

    def _mutate_one_gene(self, parent):
        # Mutation: choisir un paramètre au hasard, et le remplacer par une valeur différente (sans retirage)
        child = parent[:]
        idx = random.randint(0, 7)
        old = child[idx]
        # nouvelle valeur dans {-1,0,1} mais différente de old
        choices = [-1, 0, 1]
        choices.remove(old)
        child[idx] = random.choice(choices)
        return child

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
        # Remarques:
        # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
        # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres (c'est un "Perceptron")

        # --- Mise à jour du score à chaque pas de temps (somme sur toutes les itérations) ---
        self._update_score_incremental()

        # =========================
        # Phase REPLAY du meilleur
        # =========================
        if self.replay_mode == True:
            self.param = self.bestParam[:]  # on force le meilleur
            if self.iteration > 0 and self.iteration % self.replay_it == 0:
                print ("REPLAY BEST (infinite loop)")
                print ("\tbest_trial          =",self.best_trial)
                print ("\tbest_score          =",self.best_score)
                print ("\tbest_parameters     =",self.bestParam)
                self.iteration = self.iteration + 1
                return 0, 0, True # ask for reset

        # ==========================================
        # Phase apprentissage (GA mu=1, lambda=1) + exo2 (3 orientations)
        # ==========================================

        # toutes les X itérations: le robot est remis à sa position initiale de l'arène avec une orientation aléatoire
        if self.iteration % self.it_per_evaluation == 0:

                # --- Fin d'une des 3 évaluations ---
                if self.iteration > 0:
                    # Affichage type robot_optimize.py + score de cette évaluation
                    print ("\tparameters           =",self.param)
                    print ("\ttranslations         =",self.log_sum_of_translation,"; rotations =",self.log_sum_of_rotation) # *effective* translation/rotation (ie. measured from displacement)
                    print ("\tdistance from origin =",math.sqrt((self.x-self.x_0)**2+(self.y-self.y_0)**2))
                    print ("\tscore (this eval)    =",self.current_score)

                    # On ajoute le score de CETTE évaluation au total du candidat
                    self.score_sum_3 += self.current_score

                # On passe à l'évaluation suivante (0->1->2)
                self.eval_index += 1

                # Si on n'a pas encore fait les 3 évaluations, on reset avec la prochaine orientation
                if self.eval_index < 3:
                    self.iteration = self.iteration + 1
                    return 0, 0, True # ask for reset

                # --- Ici: on a fini les 3 évaluations du candidat courant ---
                total_score = self.score_sum_3
                print ("\ttotal score (3 eval) =",total_score)

                # Cas 1: on vient d'évaluer le parent (au tout début)
                if self.evaluating_child == False:
                    self.parentScore = total_score

                    # parent = meilleur connu pour l'instant
                    self.best_score = self.parentScore
                    self.bestParam = self.parentParam[:]
                    self.best_trial = self.trial

                    # On crée le premier enfant par mutation d'un seul paramètre
                    self.childParam = self._mutate_one_gene(self.parentParam)
                    self.param = self.childParam[:]           # on va évaluer l'enfant
                    self.evaluating_child = True

                    self.trial = self.trial + 1
                    print ("Evaluating child (generation)", self.trial)

                else:
                    # Cas 2: on vient d'évaluer l'enfant
                    childScore = total_score

                    # (mu=1 + lambda=1) : si l'enfant est meilleur, il remplace le parent
                    if childScore > self.parentScore:
                        self.parentParam = self.childParam[:]
                        self.parentScore = childScore
                        print ("CHILD REPLACES PARENT")

                        # mise à jour du meilleur global
                        if self.parentScore > self.best_score:
                            self.best_score = self.parentScore
                            self.bestParam = self.parentParam[:]
                            self.best_trial = self.trial
                            print ("NEW BEST FOUND!")
                            print ("\tbest_trial          =",self.best_trial)
                            print ("\tbest_score          =",self.best_score)
                            print ("\tbest_parameters     =",self.bestParam)
                    else:
                        print ("PARENT KEPT (child discarded)")

                    # Budget épuisé ? -> replay
                    if self.trial >= self.max_trials:
                        self.replay_mode = True
                        self.param = self.bestParam[:]

                        # reset des indices d'évaluation (on n'en a plus besoin en replay)
                        self.eval_index = 0
                        self.score_sum_3 = 0.0

                        self.iteration = self.iteration + 1
                        return 0, 0, True # ask for reset

                    # Sinon: génération suivante -> nouveau child = mutation(parent)
                    self.childParam = self._mutate_one_gene(self.parentParam)
                    self.param = self.childParam[:]
                    self.trial = self.trial + 1
                    print ("Evaluating child (generation)", self.trial)

                # IMPORTANT: on réinitialise les compteurs exo2 pour le prochain candidat (parent/enfant)
                self.eval_index = 0
                self.score_sum_3 = 0.0

                self.iteration = self.iteration + 1
                return 0, 0, True # ask for reset

        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        # Ici on utilise 3 senseurs (front_left, front, front_right) comme dans robot_optimize.py
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )

        # optionnel (comme dans les fichiers précédents): on interdit la marche arrière
        translation = max(0.0, translation)

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)

        self.iteration = self.iteration + 1        

        return translation, rotation, False 


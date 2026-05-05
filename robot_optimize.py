from robot import * 
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):
    team_name = "randomSearch"
    robot_id = -1

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a", evaluations=0, it_per_evaluation=400, *args, **kwargs):
        """
        Initialisation du robot.
        evaluations: non utilisé ici mais laissé pour compatibilité
        it_per_evaluation: nombre d'itérations pour tester chaque stratégie
        """
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1

        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0

        self.param = [random.randint(-1, 1) for _ in range(8)]
        self.bestScore = -math.inf
        self.bestTrial = 0
        self.bestParam = []
        self.trial = 0
        self.replay_iteration = 0
        self.iteration = 0
        self.max_trials = 500
        self.it_per_evaluation = it_per_evaluation if it_per_evaluation > 0 else 400

        self.log_sum_of_translation = 0.0
        self.log_sum_of_rotation = 0.0

        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        """
        Reset du robot entre deux évaluations
        """
        super().reset()
        self.log_sum_of_translation = 0.0
        self.log_sum_of_rotation = 0.0

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        """
        Fonction de contrôle du robot: Perceptron simple
        Chaque  it_per_evaluation itérations, le score est évalué
        """
        # Calcul du mouvement selon les paramètres et capteurs
        translation = math.tanh(
            self.param[0] + self.param[1] * sensors[sensor_front_left] +
            self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right]
        )
        rotation = math.tanh(
            self.param[4] + self.param[5] * sensors[sensor_front_left] +
            self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right]
        )

        # Cumuler translation et rotation pour le score
        self.log_sum_of_translation += abs(translation)
        self.log_sum_of_rotation += abs(rotation)

        self.iteration += 1  # incrément à chaque step

        # Evaluation toutes les it_per_evaluation itérations
        if self.iteration % self.it_per_evaluation == 0:
            score = self.log_sum_of_translation * max(0, 1 - abs(self.log_sum_of_rotation))
            print("Trial", self.trial + 1, "score:", score)

            # Sauvegarder si meilleur score
            if score > self.bestScore:
                self.bestScore = score
                self.bestParam = self.param[:]
                self.bestTrial = self.trial + 1
                print(">> Nouveau meilleur score :", self.bestScore, "avec paramètres", self.bestParam)

            # Générer nouvelle stratégie si pas encore toutes testées
            if self.trial < self.max_trials:
                self.trial += 1
                self.param = [random.randint(-1, 1) for _ in range(8)]
                self.reset()
                return 0, 0, True  # demander reset
            else:
                # Rejouer la meilleure stratégie
                self.param = self.bestParam[:]
                self.reset()
                self.replay_iteration += 1
                return 0, 0, True  # demander reset

        if debug and self.iteration % 100 == 0:
            print("Robot", self.robot_id, "at step", self.iteration)
            print("Sensors:", sensors)
            print("Translation:", translation, "Rotation:", rotation)

        return translation, rotation, False


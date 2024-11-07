#Code permettant de lancer des taches asynchrones avec celery
# Importation de la classe Celery depuis le module celery
from celery import Celery

from . import json_builder, utils
import time  # On importe le module time pour simuler des délais dans les tâches

# Création d'une instance de Celery
# 'tasks' est le nom de l'application Celery.
# 'broker' définit l'URL de Redis où Celery va envoyer et recevoir des messages.
# 'backend' est utilisé pour stocker le résultat des tâches.
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


# Décorateur pour définir une tâche Celery
# bind=True permet d'accéder à l'instance de la tâche via self, ce qui est utile pour mettre à jour l'état de la tâche.
@app.task(bind=True)
def make_generic(self, root_directory, dataset_name, test_case_number, nnvvppp_algoname, verbose=False, computing_block_size=2500):
    """
    Tâche Celery pour calculer les métriques et générer un JSON.

    Cette tâche simule un processus de calcul en plusieurs étapes. Elle peut être utilisée
    pour lancer des calculs de métriques de qualité pour les produits d'observation de la Terre.

    Args:
        self: Référence à l'instance de la tâche, utilisée pour mettre à jour son état.
        params: Paramètres nécessaires à la génération des métriques et du JSON. Ils peuvent inclure
                des informations spécifiques aux produits ou aux algorithmes utilisés.

    Returns:
        str: Un message indiquant que le JSON a été généré avec succès ou une erreur.
    """
    total_steps = 10  # Exemple : Nombre total d'étapes à effectuer pour simuler le calcul
    for i in range(total_steps):
        time.sleep(1)  # Simule une tâche prenant du temps (1 seconde par étape)
        # Met à jour l'état de la tâche avec le nombre d'étapes déjà complétées
        self.update_state(state='PROGRESS', meta={'current': i + 1, 'total': total_steps})

    # Appel à la fonction pour générer le JSON avec les mêmes paramètres
    result = json_builder.make_generic(root_directory, dataset_name, test_case_number, nnvvppp_algoname, verbose, computing_block_size)

    if result == 1:
        return "JSON généré avec succès."  # Retourne un message de succès
    else:
        return "Échec de la génération du JSON."  # Message d'erreur en cas d'échec

# Décorateur pour définir une tâche Celery
# bind=True permet d'accéder à l'instance de la tâche via self, ce qui est utile pour mettre à jour l'état de la tâche.
@app.task(bind=True)
def get_json_file_name(self, root_directory, dataset_name, test_case_number, verbose=False):
    # Appel à la fonction pour générer le JSON avec les mêmes paramètres
    result = utils.get_original_full_path(root_directory, dataset_name, test_case_number,verbose)

    return result

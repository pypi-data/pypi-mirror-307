import os

from flask import Flask, request, jsonify
import COPEX_high_rate_compression_quality_metrics.tasks as tasks  # Importation de la tâche Celery

app = Flask(__name__)  # Création d'une instance de l'application Flask

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Point d'entrée de l'API pour lancer le calcul des métriques et générer le JSON.

    Returns:
        dict: Un dictionnaire contenant l'ID de tâche Celery pour le suivi.
    """
    params = request.json  # Récupération des paramètres envoyés dans la requête JSON
    task = tasks.make_generic.apply_async(args=[params])  # Lancement de la tâche Celery en arrière-plan
    return jsonify({"task_id": task.id}), 202  # Retourne l'ID de la tâche et un code HTTP 202 (Accepté)

@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    """
    Point d'entrée de l'API pour vérifier le statut d'une tâche Celery.

    Args:
        task_id (str): L'ID de la tâche à vérifier.

    Returns:
        dict: Un dictionnaire contenant le statut de la tâche.
    """
    task = tasks.make_generic.AsyncResult(task_id)  # Récupération de l'objet de la tâche à partir de l'ID
    if task.state == 'PENDING':
        # Tâche en attente
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'result': None,
        }
    elif task.state != 'FAILURE':
        # Tâche en cours d'exécution
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),  # Nombre d'étapes complétées
            'total': task.info.get('total', 1),  # Nombre total d'étapes
            'result': task.result,  # Résultat (ou None si pas encore terminé)
        }
    else:
        # En cas d'échec
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'result': str(task.info),  # Récupère le message d'erreur
        }
    return jsonify(response)  # Retourne le statut de la tâche sous forme de JSON

# Route pour lancer la tâche make_generic
@app.route('/make_generic', methods=['POST'])
def run_make_generic():
    data = request.get_json()
    print("Received data:", data)  # Ajoute cette ligne pour voir les données reçues

    # Assure-toi que les données sont correctement extraites
    root_directory = data.get('root_directory')
    dataset_name = data.get('dataset_name')
    test_case_number = data.get('test_case_number')
    nnvvppp_algoname = data.get('nnvvppp_algoname')
    verbose = data.get('verbose', False)
    computing_block_size = data.get('computing_block_size', 2500)

    try:
        task = tasks.make_generic.delay(
            root_directory=root_directory,
            dataset_name=dataset_name,
            test_case_number=test_case_number,
            nnvvppp_algoname=nnvvppp_algoname,
            verbose=verbose,
            computing_block_size=computing_block_size
        )
        return jsonify({"task_id": task.id}), 202
    except Exception as e:
        print("Error:", str(e))  # Ajoute cette ligne pour capturer les erreurs
        return jsonify({"error": str(e)}), 500
@app.route('/get_path', methods=['POST'])
def run_get_path():
    print("\n get path function activated with post resquest...")
    print("ps : we are currently in working dir : ",os.getcwd())
    data = request.get_json()
    print("Received data:", data)  # Ajoute cette ligne pour voir les données reçues

    # Assure-toi que les données sont correctement extraites
    root_directory = data.get('root_directory')
    dataset_name = data.get('dataset_name')
    test_case_number = data.get('test_case_number')
    verbose = data.get('verbose', False)

    try:
        task = tasks.get_json_file_name(
            root_directory=root_directory,
            dataset_name=dataset_name,
            test_case_number=test_case_number,
            verbose=verbose,
        )
        return jsonify({"task_id": task.id}), 202
    except Exception as e:
        print("Error:", str(e))  # Ajoute cette ligne pour capturer les erreurs
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Lance l'application Flask en mode debug

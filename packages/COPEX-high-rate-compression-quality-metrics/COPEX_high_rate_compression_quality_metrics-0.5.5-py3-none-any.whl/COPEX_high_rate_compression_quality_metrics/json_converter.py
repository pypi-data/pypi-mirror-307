# module permettant la conversion, le passage de json a des graphs de visualisation par exemple
import json
import csv
import os.path

from . import global_variables, utils, json_builder


def json_to_csv_band_and_metric(json_input_path: str, csv_output_path: str, band: str, metric: str, verbose=False,
                                show_output=False):
    """
    Prend un fichier JSON, récupère les informations spécifiques à une bande et une métrique,
    et les ordonne dans un fichier CSV.

    :param json_input_path: Chemin vers le fichier JSON d'entrée.
    :param csv_output_path: Chemin vers le fichier CSV de sortie.
    :param band: Bande spécifique à récupérer (par exemple : "B01", "B02", "VV").
    :param metric: Métrique spécifique à récupérer (par exemple : "SSIM", "PSNR", "RMSE", "LPIPS").
    :param verbose: afficher les prints de debug.
    :param show_output: plot les png de sortie avant de les enregistrer.
    """
    if verbose: print("json_to_csv_band_and_metric ...")

    # Ouvre le fichier JSON et le charge en tant que dictionnaire
    with open(json_input_path, 'r') as json_file:
        data = json.load(json_file)
    if verbose: print(json_input_path, "loaded ...")

    # Vérifie si la métrique existe dans les données
    if metric not in data['metrics']:
        raise ValueError(f"La métrique '{metric}' n'existe pas dans le fichier JSON.")

    # Récupère les données de la métrique demandée
    metric_data = data['metrics'][metric]['per_band']
    if verbose: print("metric_data = [", metric_data, "] ...")

    # Filtre les données pour ne garder que celles concernant la bande spécifique
    filtered_band_data = {}
    for band_key in metric_data:
        if band in band_key:
            filtered_band_data = metric_data[band_key]
            break

    # Si aucune bande n'a été trouvée, lever une erreur
    if not filtered_band_data:
        raise ValueError(f"La bande '{band}' n'a pas été trouvée dans le fichier JSON.")

    # Liste pour stocker les données avant le tri
    data_list = []

    # Récupère les informations de chaque algorithme, sa métrique et son facteur de compression
    for algorithm, value in filtered_band_data.items():
        # Récupère le facteur de compression associé à l'algorithme
        if algorithm in data['compression_algorithms']:
            compression_factor = data['compression_algorithms'][algorithm]['compression_factor']
        else:
            compression_factor = float(
                'inf')  # Si le facteur est manquant, utiliser 'inf' pour éviter les erreurs lors du tri

        # Ajoute les informations sous forme de tuple : (algorithme, valeur de la métrique, facteur de compression)
        data_list.append((algorithm, value, compression_factor))

    # Trie la liste par facteur de compression (du plus petit au plus grand)
    data_list_sorted = sorted(data_list, key=lambda x: x[2])

    # Crée une liste avec les en-têtes pour le CSV
    csv_header = ['Algorithm', metric, 'Compression Factor']

    # Écrit les données dans un fichier CSV
    with open(csv_output_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Écrire l'en-tête
        writer.writerow(csv_header)

        # Écrire les données triées par facteur de compression
        for algorithm, value, compression_factor in data_list_sorted:
            # Écrire la ligne avec l'algorithme, la métrique et le facteur de compression
            writer.writerow([algorithm, value, compression_factor])

    print(f"Les données ont été exportées dans le fichier CSV '{csv_output_path}'.")


def json_to_csv_per_band_all_metrics(json_input_path: str, csv_output_path: str, band: str, verbose=False):
    """
    Prend un fichier JSON, récupère les informations spécifiques à une bande pour toutes les métriques,
    et les ordonne dans un fichier CSV.

    :param json_input_path: Chemin vers le fichier JSON d'entrée.
    :param csv_output_path: Chemin vers le fichier CSV de sortie.
    :param band: Bande spécifique à récupérer (par exemple : "B01", "B02", "VV").
    :param verbose: Affiche des informations supplémentaires si True.
    """
    if verbose: print("json_to_csv_band_all_metrics ...")

    # Ouvre le fichier JSON et le charge en tant que dictionnaire
    with open(json_input_path, 'r') as json_file:
        data = json.load(json_file)
    if verbose: print(f"{json_input_path} loaded ...")

    # Récupère toutes les métriques disponibles dans le JSON
    available_metrics = data['metrics'].keys()
    if verbose: print(f"Métriques disponibles : {available_metrics}")

    # Filtre les données pour ne garder que celles concernant la bande spécifique
    band_data_per_metric = {}
    for metric in available_metrics:
        metric_data = data['metrics'][metric]['per_band']
        for band_key in metric_data:
            if band in band_key:
                if metric not in band_data_per_metric:
                    band_data_per_metric[metric] = {}
                band_data_per_metric[metric] = metric_data[band_key]
                break

    # Si aucune bande n'a été trouvée, lever une erreur
    if not band_data_per_metric:
        raise ValueError(f"La bande '{band}' n'a pas été trouvée dans le fichier JSON.")

    # Liste pour stocker les données avant le tri
    data_list = []

    # Pour chaque algorithme, collecte toutes les métriques disponibles
    for algorithm in data['compression_algorithms']:
        row = [algorithm]
        compression_factor = data['compression_algorithms'][algorithm]['compression_factor']
        row.append(compression_factor)

        # Récupère la valeur de chaque métrique pour l'algorithme et la bande
        for metric in available_metrics:
            if metric in band_data_per_metric:
                metric_value = band_data_per_metric[metric].get(algorithm, None)
                row.append(metric_value)
            else:
                row.append(None)

        # Ajoute la ligne complète (algorithme, facteur de compression, valeurs des métriques)
        data_list.append(row)

    # Trie la liste par facteur de compression (du plus petit au plus grand)
    data_list_sorted = sorted(data_list, key=lambda x: x[1])

    # Crée une liste avec les en-têtes pour le CSV
    csv_header = ['Algorithm', 'Compression Factor'] + list(available_metrics)

    # Écrit les données dans un fichier CSV
    with open(csv_output_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Écrire l'en-tête
        writer.writerow(csv_header)

        # Écrire les données triées par facteur de compression
        for row in data_list_sorted:
            writer.writerow(row)

    print(f"Les données ont été exportées dans le fichier CSV '{csv_output_path}'.")


def json_to_csv_stdev_or_average_all_metrics(json_input_path: str, csv_output_path: str, stdev_or_average: str,
                                             verbose=False):
    """
    Prend un fichier JSON, récupère les informations spécifiques à une bande pour toutes les métriques,
    et les ordonne dans un fichier CSV.

    :param json_input_path: Chemin vers le fichier JSON d'entrée.
    :param csv_output_path: Chemin vers le fichier CSV de sortie.
    :param stdev_or_average:  "stdev" ou "average"
    :param verbose: Affiche des informations supplémentaires si True.
    """
    if verbose: print("json_to_csv_stdev_or_average_all_metrics ...")

    # Ouvre le fichier JSON et le charge en tant que dictionnaire
    with open(json_input_path, 'r') as json_file:
        data = json.load(json_file)
    if verbose: print(f"{json_input_path} chargé avec succès ...")

    # Récupère toutes les métriques disponibles dans le JSON
    available_metrics = data['metrics'].keys()
    if verbose: print(f"Métriques disponibles : {available_metrics}")

    # Initialisation d'une structure pour stocker les métriques par algorithme
    data_per_algo = {}

    # Parcours de chaque métrique
    for metric in available_metrics:
        metric_data = data['metrics'][metric][stdev_or_average]
        if verbose: print(f"metric_data pour {metric} : {metric_data}")

        # Pour chaque algorithme dans la métrique
        for algo_name, metric_value in metric_data.items():
            if algo_name not in data_per_algo:
                data_per_algo[algo_name] = {
                    'Compression Factor': None}  # Initialiser si l'algorithme n'est pas encore dans le dictionnaire
            data_per_algo[algo_name][metric] = metric_value
            if verbose: print(f"Algo : {algo_name}, Metric : {metric}, Value : {metric_value}")

    # Récupération du facteur de compression pour chaque algorithme
    for algo_name in data['compression_algorithms']:
        compression_factor = data['compression_algorithms'][algo_name]['compression_factor']
        data_per_algo[algo_name]['Compression Factor'] = compression_factor
        if verbose: print(f"Algo : {algo_name}, Compression Factor : {compression_factor}")

    # Préparation des données pour l'export CSV
    data_list = []
    for algo_name, metrics in data_per_algo.items():
        row = [algo_name]  # Commence la ligne avec le nom de l'algorithme
        row.append(metrics['Compression Factor'])  # Ajoute le facteur de compression

        # Ajoute les valeurs des métriques dans l'ordre des métriques disponibles
        for metric in available_metrics:
            row.append(metrics.get(metric, None))  # Si la métrique est manquante, ajoute 'None'

        data_list.append(row)

    # Trie les données par facteur de compression
    data_list_sorted = sorted(data_list, key=lambda x: x[1])

    # Préparation de l'en-tête pour le fichier CSV
    csv_header = ['Algorithm', 'Compression Factor'] + list(available_metrics)

    # Écriture des données dans le fichier CSV
    with open(csv_output_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Écrit l'en-tête
        writer.writerow(csv_header)

        # Écrit les données triées
        for row in data_list_sorted:
            writer.writerow(row)

    print(f"Les données ont été exportées dans le fichier CSV '{csv_output_path}'.")


def get_csv_name_from_wanted_band_and_wanted_metric(wanted_band, wanted_metric):
    return str(wanted_band) + "_" + str(wanted_metric) + ".csv"


def get_csv_name_from_wanted_band(wanted_band):
    return str(wanted_band) + ".csv"


def get_csv_name_from_wanted_bands(wanted_bands):
    """
       Crée un nom de fichier CSV à partir d'une liste d'éléments.

       Args:
           wanted_bands (list): Une liste d'éléments à inclure dans le nom du fichier.

       Returns:
           str: Le nom de fichier au format 'elem1_elem2_..._elemN.csv'.
       """
    # Vérifie que la liste d'éléments n'est pas vide
    if not wanted_bands:
        raise ValueError("La liste d'éléments ne peut pas être vide.")

    # Joint les éléments avec un underscore et ajoute l'extension .csv
    filename = "_".join(wanted_bands) + ".csv"

    return filename


def make_one_csv_per_band_and_metric_from_decompressed_folder_generic_metrics(root_directory: str, dataset_name: str,
                                                                              test_case_number,
                                                                              create_json_summary_if_do_not_exist=False,
                                                                              verbose=True):
    """
    Génère des fichiers CSV contenant des métriques séparées par bande et par métrique à partir d'un répertoire décompressé.

    Ce script vérifie d'abord si un fichier JSON récapitulatif existe pour le cas de test spécifié. Si ce fichier n'existe pas,
    et que le paramètre `create_json_summary_if_do_not_exist` est activé, il crée ce fichier JSON en fonction des données disponibles.
    Ensuite, pour chaque bande et chaque métrique associée au jeu de données spécifié, il génère un fichier CSV correspondant.

    :param root_directory: Répertoire racine où les fichiers décompressés sont stockés.
    :param dataset_name: Nom du jeu de données (qui détermine le satellite et les bandes associées).
    :param test_case_number: Numéro du cas de test pour lequel les métriques seront générées.
    :param create_json_summary_if_do_not_exist: Si True, crée un fichier récapitulatif JSON si aucun n'est trouvé.
    :param verbose: Si True, affiche des informations supplémentaires sur le processus.
    """
    decompressed_folder_path = utils.get_decompressed_folder_path(root_directory, dataset_name, test_case_number,
                                                                  verbose=verbose)
    json_summary_path = utils.get_latest_json_summary_file_path(decompressed_folder_path)
    print(json_summary_path)
    if json_summary_path == None:
        print(
            "no json summary path found, try to make one before using make_csv_from_decompressed_folder or use proper root directory, dataset name and test case number, or put create_json_summary_if_do_not_exist to true")
        if create_json_summary_if_do_not_exist:
            json_builder.create_summary_json_at_use_case_level_from_use_case_path(root_directory, dataset_name, test_case_number)
            json_summary_path = utils.get_latest_json_summary_file_path(decompressed_folder_path)

    output_per_band_folder_path = os.path.join(decompressed_folder_path, global_variables.summary_output_folder_name,
                                               global_variables.summary_output_csv_folder_name,
                                               global_variables.summary_output_per_band_folder_name)

    utils.create_folder_if_do_not_exist(output_per_band_folder_path)

    for band_number, band_name in global_variables.bands_per_satellite_type[dataset_name].items():
        print(band_name)
        for metric_name, _ in global_variables.metrics_dictionary.items():
            print(metric_name)
            output_csv_path = os.path.join(output_per_band_folder_path,
                                           get_csv_name_from_wanted_band_and_wanted_metric(band_name, metric_name))
            json_to_csv_band_and_metric(json_summary_path, output_csv_path, band_name, metric_name, verbose=verbose)

    output_agregation_folder_path = os.path.join(decompressed_folder_path, global_variables.summary_output_folder_name,
                                                 global_variables.summary_output_csv_folder_name,
                                                 global_variables.summary_output_all_bands_folder_name)

    utils.create_folder_if_do_not_exist(output_agregation_folder_path)
    for agregation in global_variables.metrics_all_bands_dictionary:
        output_agregation_csv_path = os.path.join(output_agregation_folder_path, agregation + ".csv")
        json_to_csv_stdev_or_average_all_metrics(json_summary_path, output_agregation_csv_path, agregation)


def make_one_csv_per_band_from_decompressed_folder_generic_metrics(root_directory: str, dataset_name: str,
                                                                   test_case_number,
                                                                   create_json_summary_if_do_not_exist=False,
                                                                   verbose=True):
    """
    Génère des fichiers CSV à partir des données json de stats calculées sur les data décompressées dans un répertoire spécifique.

    Cette fonction prend un dossier de données décompressées et un résumé JSON associé,
    et convertit les métriques des différentes bandes du satellite en fichiers CSV.

    Args:
        root_directory (str): Le répertoire racine où se trouvent les données décompressées.
        dataset_name (str): Le nom du dataset (lié au type de satellite, par ex. S1, S2, etc.).
        test_case_number (int): Le numéro du cas de test à utiliser.
        create_json_summary_if_do_not_exist (bool, optionnel): Si défini sur True, crée un résumé JSON si aucun n'existe.
                                                               Par défaut, False.
        verbose (bool, optionnel): Si défini sur True, affiche des informations supplémentaires lors de l'exécution.
                                   Par défaut, True.

    Raises:
        ValueError: Si aucun résumé JSON n'est trouvé et que `create_json_summary_if_do_not_exist` est False.
    """
    # Obtient le chemin du dossier décompressé pour le cas de test donné, en utilisant des utilitaires personnalisés
    decompressed_folder_path = utils.get_decompressed_folder_path(root_directory, dataset_name, test_case_number,
                                                                  verbose=verbose)
    # Obtient le chemin du fichier résumé JSON le plus récent
    json_summary_path = utils.get_latest_json_summary_file_path(decompressed_folder_path)
    print(json_summary_path)
    # Si aucun fichier résumé JSON n'est trouvé
    if json_summary_path == None:
        print(
            "no json summary path found, try to make one before using make_csv_from_decompressed_folder or use proper root directory, dataset name and test case number, or put create_json_summary_if_do_not_exist to true")
        if create_json_summary_if_do_not_exist:
            json_builder.create_summary_json_at_use_case_level_from_use_case_path(root_directory, dataset_name, test_case_number)
            json_summary_path = utils.get_latest_json_summary_file_path(decompressed_folder_path)
    # Détermine le chemin du dossier de sortie pour les fichiers CSV
    output_folder_path = os.path.join(decompressed_folder_path, global_variables.summary_output_folder_name,
                                      global_variables.summary_output_csv_folder_name,
                                      global_variables.summary_output_per_band_folder_name)
    # Crée le dossier de sortie s'il n'existe pas déjà
    utils.create_folder_if_do_not_exist(output_folder_path)
    # Parcourt chaque bande (spectrale) définie pour le type de satellite correspondant au dataset
    for band_number, band_name in global_variables.bands_per_satellite_type[dataset_name].items():
        print(band_name)
        output_csv_path = os.path.join(output_folder_path,
                                       get_csv_name_from_wanted_band(band_name))
        json_to_csv_per_band_all_metrics(json_summary_path, output_csv_path, band_name, verbose=True)

    #csv pour le all bands
    output_agregation_folder_path = os.path.join(decompressed_folder_path, global_variables.summary_output_folder_name,
                                                 global_variables.summary_output_csv_folder_name,
                                                 global_variables.summary_output_all_bands_folder_name)

    utils.create_folder_if_do_not_exist(output_agregation_folder_path)
    for agregation in global_variables.metrics_all_bands_dictionary:
        output_agregation_csv_path = os.path.join(output_agregation_folder_path, agregation + ".csv")
        json_to_csv_stdev_or_average_all_metrics(json_summary_path, output_agregation_csv_path, agregation)
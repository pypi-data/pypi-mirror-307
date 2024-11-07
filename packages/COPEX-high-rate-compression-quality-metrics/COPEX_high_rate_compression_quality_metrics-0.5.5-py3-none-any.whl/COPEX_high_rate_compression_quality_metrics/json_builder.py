import json
import math
from collections import defaultdict
from datetime import datetime
import os.path
from typing import List, Any, Optional

import numpy as np
from . import metrics, global_variables, utils
from tqdm import tqdm  # Importez tqdm


def load_json_file(json_file_path: str) -> Any:
    """
    Charge le contenu d'un fichier JSON et le retourne sous forme de dictionnaire ou de liste.

    Args:
        json_file_path (str): Le chemin complet du fichier JSON à charger.

    Returns:
        Any: Le contenu du fichier JSON sous forme de dictionnaire, liste, ou autre
             structure de données Python (selon le contenu du fichier JSON).
    """
    # Vérifier si le fichier spécifié existe
    if not os.path.isfile(json_file_path):
        raise FileNotFoundError(f"Le fichier spécifié n'existe pas : {json_file_path}")

    # Charger le contenu du fichier JSON
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    return data


def calculate_averages_for_specific_string_for_each_metric(data, string_to_average, verbose=False):
    """
    Fonction récursive pour calculer les moyennes des métriques à trois niveaux.
    exemple de json en entrée :
    json_data = {
        "per_use_case": {
            "metric_1": {
                "use_case_1": {
                    "[01-01-003_JJ2000_x150]_[9123996]_[83]_[153]": 0.343,
                    "[01-01-002_JJ2000_x100]_[13655776]_[87]_[170]": 0.272,
                    "[01-01-001_JJ2000_x50]_[26974008]_[102]_[172]": 0.152,
                    "[01-01-004_JJ2000_x200]_[6871782]_[86]_[146]": 0.396,
                    "[01-01-005_JJ2000_x250]_[5534029]_[84]_[136]": 0.433
                },
                "use_case_n": {
                    "[01-01-003_JJ2000_x150]_[9123996]_[83]_[153]": 0.443,
                    "[01-01-002_JJ2000_x100]_[13655776]_[87]_[170]": 0.372,
                    "[01-01-001_JJ2000_x50]_[26974008]_[102]_[172]": 0.052,
                    "[01-01-004_JJ2000_x200]_[6871782]_[86]_[146]": 0.496,
                    "[01-01-005_JJ2000_x250]_[5534029]_[84]_[136]": 0.533
                }
            },
            "metric_n": {
                "use_case_1": {
                    "[01-01-003_JJ2000_x150]_[9123996]_[83]_[153]": 0.129,
                    "[01-01-002_JJ2000_x100]_[13655776]_[87]_[170]": 0.109,
                    "[01-01-001_JJ2000_x50]_[26974008]_[102]_[172]": 0.069,
                    "[01-01-004_JJ2000_x200]_[6871782]_[86]_[146]": 0.143,
                    "[01-01-005_JJ2000_x250]_[5534029]_[84]_[136]": 0.151
                },
                "use_case_n": {
                    "[01-01-003_JJ2000_x150]_[9123996]_[83]_[153]": 0.229,
                    "[01-01-002_JJ2000_x100]_[13655776]_[87]_[170]": 0.209,
                    "[01-01-001_JJ2000_x50]_[26974008]_[102]_[172]": 0.169,
                    "[01-01-004_JJ2000_x200]_[6871782]_[86]_[146]": 0.243,
                    "[01-01-005_JJ2000_x250]_[5534029]_[84]_[136]": 0.351
                }
            }
        }
    }
    """
    # Vérifie si 'per_use_case' est dans la structure actuelle
    if string_to_average in data:
        if verbose: print(f"{string_to_average} is present...")

        # Parcours des métriques et des use cases
        for metric, use_cases in data[string_to_average].items():
            if verbose: print(f"Processing metric: {metric}")

            # Dictionnaire pour regrouper les valeurs par algo
            algo_values = {}

            # Parcours des use cases
            for use_case, values in use_cases.items():
                if verbose: print(f"Processing use case: {use_case}")

                # Pour chaque algo, ajouter ses valeurs dans algo_values
                for algo_key, value in values.items():
                    # On regroupe par algo en fonction de son nom (clé)
                    if algo_key not in algo_values:
                        algo_values[algo_key] = []
                    algo_values[algo_key].append(value)

            # Calcul des moyennes pour chaque algo
            for algo_key, all_values in algo_values.items():
                if all_values:  # Vérifie qu'il y a des valeurs à moyenner
                    valid_values = [value for value in all_values if
                                    isinstance(value, (int, float)) and not math.isinf(value) and value is not None]
                    average_value = sum(valid_values) / len(valid_values) if valid_values else "invalid values"
                    average_key = f'average_{metric}'

                    # Ajout de la moyenne au dictionnaire data
                    if average_key not in data:
                        data[average_key] = {}
                    data[average_key][algo_key] = average_value

                    if verbose:
                        print(f"average_key[{average_key}], algo[{algo_key}], average_value[{average_value}]")

        # Appel récursif pour les sous-niveaux
    for key, value in data.items():
        if isinstance(value, dict):
            calculate_averages_for_specific_string_for_each_metric(value, string_to_average, verbose)

    return data


def get_json_name_by_initialising_new_one_or_getting_already_existing(root_directory, dataset_name, test_case_number,
                                                                      nnvvppp_algoname) -> str:
    """
        Récupère le nom d'un fichier JSON existant avec la date la plus récente, ou crée un nouveau fichier JSON si aucun n'est trouvé.

        Cette fonction cherche un fichier JSON dans un dossier spécifique qui correspond aux paramètres fournis.
        Si des fichiers JSON sont trouvés, elle identifie celui avec la date la plus récente dans son nom.
        Si aucun fichier JSON n'est trouvé, elle initialise un nouveau fichier JSON.
        Si aucune date valide ne peut être extraite, ou si aucun fichier JSON ne peut être trouvé ou créé, une exception est levée.

        Args:
            root_directory (str): Le chemin racine vers le répertoire contenant les résultats.
            dataset_name (str): Le nom du jeu de données.
            test_case_number (str): Le numéro du cas de test associé.
            nnvvppp_algoname (str): Le nom de l'algorithme spécifique.

        Returns:
            str: Le nom du fichier JSON à utiliser, soit un existant avec la date la plus récente, soit un nouveau fichier initialisé.

        Raises:
            ValueError: Si aucun fichier JSON ne peut être récupéré ou créé, une exception est levée pour indiquer une erreur dans les paramètres d'entrée.

        Example:
            Si `root_directory` contient plusieurs fichiers JSON avec des dates dans leur nom, cette fonction retournera
            le fichier avec la date la plus récente. Sinon, elle créera et retournera un nouveau fichier JSON.
        """
    result_folder_path = utils.get_algorithm_results_full_path(root_directory, dataset_name, test_case_number,
                                                               nnvvppp_algoname)
    json_file_list = utils.list_json_files(result_folder_path)
    dates = []

    if json_file_list:
        # Extraire les dates des noms de fichiers JSON
        for json_file_name in json_file_list:
            try:
                dates.append(utils.get_bracket_content(json_file_name, 3))
            except ValueError:
                print(f"Error extracting date from file: {json_file_name}")

        if dates:
            most_recent_index = utils.get_most_recent_date_index(dates)
            final_json_file = json_file_list[most_recent_index]
            # print(f"Dates: {dates}")
            # print(f"Index of most recent date: {most_recent_index}")
            # print(f"Final JSON file to use is {final_json_file}")
            return final_json_file
        else:
            print("No valid dates found in JSON file names.")
    else:
        print(f"No .json found in {result_folder_path}... ")
        final_json_file = initialize_json(root_directory, dataset_name, test_case_number, nnvvppp_algoname)
        print(f"Final JSON file to use is {final_json_file}")
        return final_json_file
    raise ValueError("no json file name could be get or created... verify input parameters.")


# FONCTION PRINCIPALE A UTILISER POUR CALCULER LES
# THEMATIQUES AU NIVEAU D'UN USE CASE
def make_thematic(root_directory, dataset_name, test_case_number, nnvvppp_algoname, thematic_function, verbose=False,
                  *thematic_args,
                  **thematic_kwargs):
    """
    Gère la création ou la mise à jour d'un fichier JSON pour les indicateurs thématiques d'un ensemble de données spécifique.

    Cette fonction vérifie si un fichier JSON existe déjà pour les paramètres donnés. Si tel est le cas, elle modifie le fichier existant ; sinon, elle en crée un nouveau. Elle applique une fonction thématique fournie avec des arguments et des mots-clés supplémentaires pour calculer des indicateurs et ajoute ces informations au fichier JSON.

    Arguments :
    root_directory (str) : Le répertoire racine où se trouvent les données.
    dataset_name (str) : Le nom de l'ensemble de données pour lequel le fichier JSON est généré.
    test_case_number (str) : Le numéro du cas de test associé aux données.
    nnvvppp_algoname (str) : Le nom de l'algorithme avec un format spécifique qui sera utilisé pour identifier le fichier JSON.
    thematic_function (callable) : Une fonction thématique modulaire qui prend des chemins de fichiers comme entrée et retourne un dictionnaire de résultats.
    *thematic_args : Arguments positionnels supplémentaires à passer à la fonction thématique.
    **thematic_kwargs : Arguments nommés supplémentaires à passer à la fonction thématique.

    Retour :
    None
    """
    if verbose: print(f"Arguments positionnels : {thematic_args}")
    if verbose: print(f"Arguments nommés : {thematic_kwargs}")
    # Obtenez le chemin complet du dossier des résultats pour l'algorithme
    result_folder_path = utils.get_algorithm_results_full_path(
        root_directory=root_directory,
        dataset_name=dataset_name,
        test_case_number=test_case_number,
        nnvvppp_algoname=nnvvppp_algoname
    )

    # Obtenez le chemin complet du dossier des données originales
    original_folder_path = utils.get_original_full_path(
        root_directory=root_directory,
        dataset_name=dataset_name,
        test_case_number=test_case_number
    )

    # Trouvez le fichier JSON le plus récent dans le dossier des résultats
    most_recent_json_file = utils.get_last_json_from_use_case_result_folder(
        root_directory,
        dataset_name,
        test_case_number,
        nnvvppp_algoname, verbose=verbose
    )

    if most_recent_json_file:
        # Chargez le contenu du fichier JSON le plus récent
        most_recent_json_file_full_path = os.path.join(result_folder_path, most_recent_json_file)
        json_content = load_json_file(most_recent_json_file_full_path)
    else:
        # Créez un nouveau fichier JSON si aucun fichier existant n'est trouvé
        json_content = get_initialized_json_data(
            root_directory,
            dataset_name,
            test_case_number,
            nnvvppp_algoname
        )

    # Appliquez la fonction thématique fournie à chaque produit avec les arguments supplémentaires
    key = None
    data = {}
    # Utilisez la fonction thématique avec des arguments supplémentaires pour calculer les résultats pour chaque produit
    key, result = thematic_function(*thematic_args, **thematic_kwargs)
    utils.add_data_to_dict(data, result)

    # Ajoutez les statistiques des métriques au contenu JSON
    utils.add_data_to_dict(json_content, {key: metrics.calculate_metrics_statistics(data)})

    final_json_name = algorithm_level_make_json_filename(dataset_name, test_case_number,
                                                         utils.get_nn_vv_ppp_from_full_nnvvppp_algo_name(
                                                             nnvvppp_algoname),
                                                         json_content.get("compression_factor", None))
    final_json_path = os.path.join(result_folder_path, final_json_name)

    # Écrivez le contenu JSON dans le fichier final
    with open(final_json_path, 'w') as json_file:
        json.dump(json_content, json_file, indent=4)

    print(f"Fichier JSON thématique créé : {final_json_name}")


# FONCTION PRINCIPALE A UTILISER POUR CALCULER LES METRIQUES GENERIQUE AU NIVEAU D'UN USE CASE
def make_generic(root_directory, dataset_name, test_case_number, nnvvppp_algoname, verbose=False,
                 computing_block_size=2500) -> int:
    """
    Gère la création ou la mise à jour d'un fichier JSON pour un ensemble de données spécifique.

    Cette fonction vérifie si un fichier JSON existe déjà pour les paramètres donnés. Si tel est le cas, elle modifie le fichier existant ; sinon, elle en crée un nouveau. Le fichier JSON est utilisé pour stocker des informations sur les produits originaux et décompressés, ainsi que sur les métriques calculées.

    Arguments :
    root_directory (str) : Le répertoire racine où se trouvent les données.
    dataset_name (str) : Le nom de l'ensemble de données pour lequel le fichier JSON est généré.
    test_case_number (str) : Le numéro du cas de test associé aux données.
    nnvvppp_algoname (str) : Le nom de l'algorithme avec un format spécifique qui sera utilisé pour identifier le fichier JSON.

    Retour :
    None
    """

    # Obtenez le chemin complet du dossier des résultats pour l'algorithme
    if verbose:
        print("- make_generic - root_directory = ", root_directory)
        print("- make_generic - test_case_number = ", test_case_number)
        print("- make_generic - dataset_name = ", dataset_name)
        print("- make_generic - nnvvppp_algoname = ", nnvvppp_algoname)

    result_folder_path = utils.get_algorithm_results_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                               test_case_number=test_case_number,
                                                               nnvvppp_algoname=nnvvppp_algoname, verbose=verbose)
    # Obtenez le chemin complet du dossier des données originales
    original_folder_path = utils.get_original_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                        test_case_number=test_case_number)

    # Trouvez le fichier JSON le plus récent dans le dossier des résultats
    most_recent_json_file = utils.get_last_json_from_use_case_result_folder(root_directory,
                                                                            dataset_name,
                                                                            test_case_number,
                                                                            nnvvppp_algoname, verbose=verbose)
    if (most_recent_json_file):
        # Chargez le contenu du fichier JSON le plus récent
        most_recent_json_file_full_path = os.path.join(result_folder_path, most_recent_json_file)
        json_content = load_json_file(most_recent_json_file_full_path)
    else:
        # Créez un nouveau fichier JSON si aucun fichier existant n'est trouvé
        json_content = get_initialized_json_data(root_directory,
                                                 dataset_name,
                                                 test_case_number,
                                                 nnvvppp_algoname)

    # Obtenez les chemins des produits originaux et décompressés
    original_product_list = utils.get_product_name_list_from_path(original_folder_path)
    decompressed_product_path_list = []
    original_product_path_list = []
    for product_band_name in original_product_list:
        decompressed_product_path_list.append(utils.find_matching_file(product_band_name, result_folder_path))
        original_product_path_list.append(os.path.join(original_folder_path, product_band_name))

    # print(decompressed_product_path_list)
    # print(original_product_path_list)

    # Calculez les métriques pour chaque paire de produits originaux et décompressés
    for i in tqdm(range(len(original_product_path_list)), desc="Calcul des métriques", unit="produit"):
        data_to_add = metrics.calculate_lrsp(original_product_path_list[i], decompressed_product_path_list[i],
                                             verbose=verbose, computing_block_size=computing_block_size)
        utils.add_data_to_dict(json_content, data_to_add)

    # print("json_content = ", json_content)
    # print("type(json_content) = ", type(json_content))

    # Créez un nom de fichier JSON final basé sur les paramètres fournis
    final_json_name = algorithm_level_make_json_filename(dataset_name, test_case_number,
                                                         utils.get_nn_vv_ppp_from_full_nnvvppp_algo_name(
                                                             nnvvppp_algoname),
                                                         json_content.get("compression_factor", None))
    final_json_path = os.path.join(result_folder_path, final_json_name)

    # Ajoutez les statistiques des métriques au contenu JSON
    utils.add_data_to_dict(json_content, metrics.calculate_metrics_statistics(json_content))

    # Écrivez le contenu JSON dans le fichier final
    with open(final_json_path, 'w') as json_file:
        json.dump(json_content, json_file, indent=4)

    print(f"Fichier JSON créé : {final_json_name}")

    return 1


# ------------------------- USE CASE LEVEL -------------------------
def algorithm_level_make_json_filename(dataset_name, test_case_number, nnvvppp_algoname, compression_factor) -> str:
    """
        Génère un nom de fichier JSON basé sur les paramètres fournis.

        Args:
            dataset_name (str): Le nom du jeu de données.
            test_case_number (int): Le numéro du cas de test.
            nnvvppp_algoname (str): Le nom complet de l'algorithme NN-VV-PPP.
            compression_factor (float): Le facteur de compression.

        Returns:
            str: Le nom de fichier JSON formaté avec les informations fournies et un timestamp.
        """
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"[{dataset_name}]_[{utils.get_test_case_number_str(test_case_number)}]_[{utils.get_nn_vv_ppp_from_full_nnvvppp_algo_name(nnvvppp_algoname)}_x{str(compression_factor)}]_[{now}].json"


def initialize_json(root_directory, dataset_name, test_case_number, nnvvppp_algoname, verbose=False):
    """
    Initialise un fichier JSON pour stocker des informations sur les résultats de compression.

    Args:
        root_directory (str): Le répertoire racine où se trouvent les dossiers de résultats.
        dataset_name (str): Le nom du jeu de données.
        test_case_number (int): Le numéro du cas de test.
        nnvvppp_algoname (str): Le nom complet de l'algorithme NN-VV-PPP utilisé pour la compression.

    Returns:
        str: Le nom du fichier JSON créé.
    """
    # Calculer le facteur de compression xC

    result_folder_path = utils.get_algorithm_results_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                               test_case_number=test_case_number,
                                                               nnvvppp_algoname=nnvvppp_algoname)
    original_folder_path = utils.get_original_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                        test_case_number=test_case_number)
    compression_factor = utils.calculate_compression_factor_between_two_folders(original_folder_path,
                                                                                result_folder_path)
    if verbose: print(f"initializing json file for folder {result_folder_path}...")
    # Générer la date et l'heure actuelle

    # Créer le nom du fichier JSON au format [dataset_name_1]_[TTT]_[NN VV PPP_xC]_[yyyyMMdd_HHmmss].json
    json_filename = algorithm_level_make_json_filename(dataset_name, test_case_number,
                                                       utils.get_nn_vv_ppp_from_full_nnvvppp_algo_name(
                                                           nnvvppp_algoname),
                                                       compression_factor)

    # Initialiser la structure JSON de base
    json_data = get_initialized_json_data(root_directory,dataset_name,test_case_number,nnvvppp_algoname)
    output_path_plus_filename = os.path.join(result_folder_path, json_filename)
    # Sauvegarder le fichier JSON
    with open(output_path_plus_filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    print(f"Fichier JSON créé : {json_filename}")
    return json_filename


def add_bands_size_to_json_file(json_file_path: str, use_case_number,  original_files_folder_path: str):
    """
    Ouvre un fichier JSON existant et ajoute les dimensions (width, height)
    des fichiers TIFF du dossier spécifié.

    Args:
        json_file_path (str): Chemin vers le fichier JSON à modifier.
        use_case_number (str ou int): le numéro de use case.
        original_files_folder_path (str): Chemin vers le dossier contenant les fichiers TIFF.
    """
    # Charger le fichier JSON existant
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
    else:
        raise FileNotFoundError(f"Le fichier JSON spécifié n'existe pas: {json_file_path}")
    
    bands_data = { "bands_size" : {utils.get_test_case_number_str(use_case_number) : metrics.get_tiff_dimensions(original_files_folder_path)} }
    json_data = utils.add_data_to_dict(json_data,bands_data)
    # Sauvegarder les changements dans le fichier JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

def get_initialized_json_data(root_directory, dataset_name, test_case_number, nnvvppp_algoname):
    """
    Initialise les données JSON pour les résultats de compression à partir des chemins spécifiés.

    Args:
        root_directory (str): Le répertoire racine où se trouvent les dossiers de résultats.
        dataset_name (str): Le nom du jeu de données.
        test_case_number (int): Le numéro du cas de test.
        nnvvppp_algoname (str): Le nom complet de l'algorithme NN-VV-PPP utilisé pour la compression.

    Returns:
        dict: Les données JSON contenant les informations sur la compression.
    """
    # Calculer le facteur de compression xC

    result_folder_path = utils.get_algorithm_results_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                               test_case_number=test_case_number,
                                                               nnvvppp_algoname=nnvvppp_algoname)
    original_folder_path = utils.get_original_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                        test_case_number=test_case_number)
    compression_factor = utils.calculate_compression_factor_between_two_folders(original_folder_path,
                                                                                result_folder_path)
    bands_size = metrics.get_tiff_dimensions(original_folder_path)
    print("bands_size = ", bands_size)
    print(f"initializing json file for folder {result_folder_path}...")
    # Générer la date et l'heure actuelle

    # print(nnvvppp_algoname)
    nnvvppp = nnvvppp_algoname.split("_")[0]
    # print(nnvvppp)
    # Initialiser la structure JSON de base
    json_data = {
        "original_size": utils.get_folder_size(original_folder_path),
        "compressed_size": utils.get_compressed_size_from_folder_name(result_folder_path),
        "compression_factor": compression_factor,
        "compression_time": utils.get_bracket_content(result_folder_path, 2),
        "decompression_time": utils.get_bracket_content(result_folder_path, 3),
        "compression_algorithm": nnvvppp_algoname,
        "algorithm_version": nnvvppp.split("-")[1],
        "compression_parameter": nnvvppp.split("-")[2],
        "bands_size": {utils.get_test_case_number_str(test_case_number): bands_size}

        # D'autres sections peuvent être ajoutées ici si nécessaire
    }

    return json_data


# Fonction pour créer un fichier JSON récapitulatif à partir de plusieurs fichiers JSON
def create_summary_json_at_use_case_level(latest_json_files: List[Optional[str]], output_file: str,
                                          verbose=False) -> None:
    """
    Crée un fichier JSON récapitulatif à partir des derniers fichiers JSON trouvés dans différents dossiers.

    :param latest_json_files: Liste des chemins vers les derniers fichiers JSON récupérés.
    :param output_file: Chemin du fichier de sortie pour le fichier récapitulatif.
    """
    # Initialisation du dictionnaire de données récapitulatives
    summary_data = {
        "COPEX high compression library version": "0.2.2",  # Exemple de version
        "date": "2024-09-24 14:47:27",  # Exemple de date
        "original_size": 0,
        "compression_algorithms": {},  # Dictionnaire pour les algorithmes de compression
        "metrics": {},
        "thematics": {}
    }

    # Parcourt les fichiers JSON fournis
    for json_file in latest_json_files:
        if json_file is None:
            continue

        with open(json_file, 'r') as f:
            data = json.load(f)

            # Ajoute la taille originale
            summary_data["original_size"] += data.get("original_size", "not found")

            # Récupère les informations spécifiques à chaque algorithme
            algorithm_key = data.get("compression_algorithm", "unknown")  # clé par défaut
            algorithm_details = {
                "compressed_size": data.get("compressed_size", "not found"),
                "compression_factor": data.get("compression_factor", "not found"),
                "compression_time": data.get("compression_time", "N/A"),
                "decompression_time": data.get("decompression_time", "N/A"),
                "compression_algorithm": algorithm_key,
                "algorithm_version": data.get("algorithm_version", "N/A"),
                "compression_parameter": data.get("compression_parameter", "N/A"),
                "analysis date": utils.reformat_date(json_file.split("[")[-1].replace("].json", ""))
            }

            # Utilise la clé du dossier comme clé dans le dictionnaire des algorithmes
            folder_name = os.path.basename(os.path.dirname(json_file))  # Récupère le nom du dossier
            summary_data["compression_algorithms"][folder_name] = algorithm_details

            # Gestion des métriques
            for metric, details in data.get("metrics", {}).items():
                if verbose:
                    print("metric : ", metric)
                    print("details : ", details)
                if metric not in summary_data["metrics"]:
                    summary_data["metrics"][metric] = {
                        "per_band": {},
                        "average": {},
                        "stdev": {}
                    }

                for band, value in details["results"].items():
                    # Gestion des valeurs non numériques
                    value = value

                    if band not in summary_data["metrics"][metric]["per_band"]:
                        summary_data["metrics"][metric]["per_band"][band] = {}
                    summary_data["metrics"][metric]["per_band"][band][folder_name] = value

                # Ajoute les moyennes et écarts types
                summary_data["metrics"][metric]["average"][folder_name] = details.get("average", 0)
                summary_data["metrics"][metric]["stdev"][folder_name] = details.get("stdev", 0)

            for thematic, thematic_details in data.get("thematics", {}).items():
                if verbose:
                    print("thematic : ", thematic)
                    print("thematic_details : ", thematic_details)
                # Initialisation de la thématique dans le résumé si elle n'existe pas
                if thematic not in summary_data["thematics"]:
                    summary_data["thematics"][thematic] = {
                        "overall_accuracy": {},
                        "kappa_coefficient": {}
                    }

                for algo_key, metrics_values in thematic_details.get("metrics", {}).items():
                    if algo_key == "overall_accuracy":
                        overall_accuracy_result = metrics_values.get("results", {})
                        overall_accuracy = list(overall_accuracy_result.values())[
                            0] if overall_accuracy_result else "not found"
                        # Ajout de l'overall_accuracy au résumé
                        summary_data["thematics"][thematic]["overall_accuracy"][folder_name] = overall_accuracy

                    if algo_key == "kappa_coefficient":
                        kappa_coefficient_result = metrics_values.get("results", {})
                        kappa_coefficient = list(kappa_coefficient_result.values())[
                            0] if kappa_coefficient_result else "not found"

                        # Ajout du kappa_coefficient au résumé
                        summary_data["thematics"][thematic]["kappa_coefficient"][folder_name] = kappa_coefficient

    # Sauvegarde le fichier JSON récapitulatif
    with open(output_file, 'w') as f:
        json.dump(summary_data, f, indent=4)


# FONCTION PRINCIPALE POUR FAIRE UN SUMMARY A UN USE CASE LEVEL
def create_summary_json_from_use_case_path_at_use_case_level(root_directory: str, satellite_type: str,
                                                             test_case_number: any, verbose=False):
    """

    """
    # 1 faire la liste des dossiers
    input_folder_path = utils.get_use_case_full_path(root_directory=root_directory, satellite_type=satellite_type,
                                                     test_case_number=test_case_number,verbose=verbose)
    # print("input_folder_path = ", input_folder_path)
    decompressed_folder_path = os.path.join(input_folder_path, global_variables.decompressed_folder_name)
    folder_name_list = utils.list_directories(decompressed_folder_path)
    json_path_list = []
    for name in folder_name_list:
        folder_path = os.path.join(decompressed_folder_path, name)
        json_path = utils.get_latest_json_file_path_ordering_by_date_in_name(folder_path)
        # print("json_name = ",json_path)
        json_path_list.append(json_path)
    # print(" json list = ", json_path_list)
    output_name = "[" + str(satellite_type) + "]" + "_[" + utils.get_test_case_number_str(
        test_case_number) + "]" + "_[" + str(
        datetime.now().strftime("%Y%m%d_%H%M%S")) + "]_[" + global_variables.use_case_summary_parameter + "].json"
    #print("os.path.join(decompressed_folder_path, output_name) = os.path.join(",decompressed_folder_path,", ",output_name,")")
    create_summary_json_at_use_case_level(json_path_list, os.path.join(decompressed_folder_path, output_name),verbose=verbose)


# ------------------------- DATA/SATELLITE LEVEL -------------------------
def make_json_data_level_name(satellite_type):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "[" + satellite_type + "]_[" + now + "]_["+ global_variables.dataset_summary_parameter+ "].json"


def calculate_averages_for_specific_string_by_key(data, string_to_average, verbose=False):
    """
    Fonction récursive pour calculer les moyennes des métriques à trois niveaux.
    """
    # Vérifie si 'per_use_case' est dans la structure actuelle

    if string_to_average in data:
        if verbose: print(string_to_average, " is present...")
        for metric, use_cases in data[string_to_average].items():
            if verbose: print("metric[", metric, "], use_cases[", use_cases, "]")
            # Initialisation d'une liste pour stocker toutes les valeurs
            all_values = {}

            for use_case, values in use_cases.items():
                if verbose: print("--use_case[", use_case, "], values[", values, "]")
                for key, value in values.items():
                    if verbose: print("----key[", key, "], value[", value, "]")
                    if key not in all_values:
                        all_values[key] = []
                    all_values[key].append(value)

            # Calcule la moyenne des valeurs pour la métrique actuelle
            if all_values:
                if verbose: print("--all_values = ", all_values)
                for keys, value_tab in all_values.items():
                    if verbose: print("------keys[", keys, "], value_tab[", value_tab, "]")
                    average_value = sum(value_tab) / len(value_tab)
                    average_key = f'average_{metric}'
                    if verbose:
                        print("------average_key[", average_key, "], all_values[", average_value, "]")
                        print("------data = ", data)
                    if average_key not in data.keys():
                        data[average_key] = {}
                    data[average_key][keys] = average_value
    print("data = [", data, "]")
    # Appel récursif pour traiter les sous-niveaux
    for key, value in data.items():
        print("key[", key, "],value[", value, "]")
        if isinstance(value, dict):
            calculate_averages_for_specific_string_by_key(value, string_to_average, verbose=verbose)

    return data


def calculate_average_metrics(input_json_path, output_json_path, string_to_average, verbose=False):
    """
    Cette fonction lit les données JSON à trois niveaux depuis un fichier d'entrée,
    calcule la moyenne des valeurs pour chaque métrique,
    et écrit les résultats dans un fichier de sortie.
    """
    # Lecture des données depuis le fichier d'entrée
    with open(input_json_path, 'r') as infile:
        data = json.load(infile)

    # Lancement du traitement pour calculer les moyennes
    calculate_averages_for_specific_string_for_each_metric(data, string_to_average, verbose)

    # Écriture des données modifiées dans le fichier de sortie
    with open(output_json_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def make_data_level_json_summary(filenames: list, output_file: str):
    """
    Génère un résumé des fichiers de summary JSON en fonction des use cases.

    :param filenames: Liste des fichiers JSON à traiter.
    :param output_file: Chemin du fichier de sortie pour le résumé.
    """
    # Initialisation de la structure du fichier résumé
    final_summary = {
        "COPEX high compression library version": None,  # À remplir à partir du premier fichier
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "sum_of_use_cases_original_sizes": 0,  # Somme de tous les original_size
        "use_cases": {},
        "metrics": defaultdict(lambda: {"per_use_case": defaultdict(dict), "average": {}, "stdev": {}}),
        "thematics": defaultdict(
            lambda: {"per_use_case": defaultdict(dict), "overall_accuracy": {}, "kappa_coefficient": {}})
    }

    use_case_counter = 1  # Pour attribuer un numéro unique à chaque use case

    for filename in filenames:
        print("opening ", filename, "...")
        with open(filename, 'r') as f:
            data = json.load(f)

            # Récupération de la version si pas déjà définie
            if final_summary["COPEX high compression library version"] is None:
                final_summary["COPEX high compression library version"] = data["COPEX high compression library version"]

            # Ajout de la taille originale
            final_summary["sum_of_use_cases_original_sizes"] += data["original_size"]

            # Attribution d'un identifiant de use case unique (ex: 001, 002, ...)
            use_case_id = f"{use_case_counter:03}"
            final_summary["use_cases"][use_case_id] = data["compression_algorithms"]
            use_case_counter += 1

            # Agrégation des metrics (LPIPS, RMSE, etc.)
            for metric, metric_data in data["metrics"].items():
                # Vérifie si la métrique existe dans 'final_summary', sinon l'initialise ex "LPIPS":{"per_use_case":{"average":{}...}}
                if metric not in final_summary["metrics"]:
                    final_summary["metrics"][metric] = {"per_use_case": {"average": {}, "stdev": {}}}

                # Vérifie et initialise 'average' et 'stdev' pour le use_case_id
                for stat_type in ["average", "stdev"]:
                    if use_case_id not in final_summary["metrics"][metric]["per_use_case"][stat_type]:
                        final_summary["metrics"][metric]["per_use_case"][stat_type][use_case_id] = {}

                    # Parcourt les algorithmes et les valeurs pour chaque type de statistique
                    if stat_type in metric_data:
                        for algorithm, value in metric_data[stat_type].items():
                            print(f"stat_type = [{stat_type}], algorithm = [{algorithm}], value = [{value}]")

                            # Insère la valeur dans le bon endroit du dictionnaire
                            final_summary["metrics"][metric]["per_use_case"][stat_type][use_case_id][algorithm] = value

            # Agrégation des thematics (kmeans, etc.)
            for thematic, thematic_data in data["thematics"].items():
                # Vérifie si le thematic existe dans 'final_summary', sinon l'initialise avec "per_use_case"
                if thematic not in final_summary["thematics"]:
                    final_summary["thematics"][thematic] = {"per_use_case": {}}

                for stat_type in data["thematics"][thematic]:
                    print("-----------------stat_type = ", stat_type)
                    if stat_type not in final_summary["thematics"][thematic]["per_use_case"]:
                        final_summary["thematics"][thematic]["per_use_case"][stat_type] = {}

                    # Parcourt les algorithmes et les valeurs pour chaque type de statistique
                    if stat_type in thematic_data:
                        for algorithm, value in thematic_data[stat_type].items():
                            print(f"stat_type = [{stat_type}], algorithm = [{algorithm}], value = [{value}]")
                            if use_case_id not in final_summary["thematics"][thematic]["per_use_case"][stat_type]:
                                final_summary["thematics"][thematic]["per_use_case"][stat_type][use_case_id] = {}
                            if use_case_id in final_summary["thematics"][thematic]["per_use_case"][stat_type]:
                                # Insère la valeur dans le bon endroit du dictionnaire
                                final_summary["thematics"][thematic]["per_use_case"][stat_type][use_case_id][
                                    algorithm] = value

    # Sauvegarde du résumé dans un fichier JSON
    with open(output_file, 'w') as outfile:
        json.dump(final_summary, outfile, indent=4)

    print("json was created in ", output_file, " .")


# FONCTION PRINCIPALE A UTILISER POUR FAIRE UN RECAP DE TOUT AU NIVEAU DU DATASET/SATELLITE
def create_summary_json_at_satellite_type_level_from_data_folder(root_directory: str, satellite_type: str,
                                                                 verbose=False):
    """
    Crée un fichier JSON récapitulatif pour un type de satellite donné à partir des données d'un dossier.

    Args:
        root_directory (str): Le chemin du dossier racine contenant les données.
        satellite_type (str): Le type de satellite (ex: 'S1', 'S2') pour lequel le résumé est créé.

    Étapes principales:
    1. Générer la liste des sous-dossiers contenant les données pour le type de satellite.
    2. Filtrer les dossiers pour n'inclure que ceux avec un certain nombre de champs (3 ici).
    3. Récupérer le dernier fichier JSON récapitulatif pour chaque dossier de données.
    4. Créer un nouveau dossier (s'il n'existe pas déjà) pour stocker le fichier JSON final.
    5. Appeler une fonction qui génère un fichier JSON récapitulatif pour le type de satellite.

    Returns:
        None: La fonction crée un fichier JSON dans un dossier de sortie sans retourner de valeur.
    """
    # 1. Générer le chemin du dossier contenant les données du satellite
    data_folder_path = os.path.join(root_directory, satellite_type)

    # Générer le chemin du dossier où sera stocké le résumé final
    data_summary_folder_path = os.path.join(data_folder_path)

    # 2. Lister tous les sous-dossiers dans le dossier de données
    data_folders = utils.list_directories(data_folder_path)

    # Filtrer les dossiers pour n'inclure que ceux avec un nombre de champs égal à 3 (selon ton besoin)
    data_folders = utils.filter_folders_by_field_number(data_folders, field_number=3)
    json_path_list = []  # Initialiser une liste pour stocker les chemins des fichiers JSON

    # 3. Parcourir chaque dossier filtré
    for folder in data_folders:
        # Générer le chemin du dossier contenant les fichiers JSON décompressés
        folder_path = os.path.join(data_folder_path, folder, global_variables.decompressed_folder_name)
        if verbose: print("folder_path = ", folder_path)

        # Récupérer le chemin du dernier fichier JSON récapitulatif dans ce dossier
        json_summary_file_path = utils.get_latest_json_summary_file_path(folder_path)

        # Ajouter ce chemin à la liste
        json_path_list.append(json_summary_file_path)
        if verbose: print("input_folder_path = ", json_summary_file_path)

    # 4. Créer le dossier de sortie si ce dernier n'existe pas déjà
    utils.create_folder_if_do_not_exist(data_summary_folder_path)

    # Générer le chemin de sortie pour le fichier JSON récapitulatif
    print("data_summary_folder_path = ", data_summary_folder_path," , make_json_data_level_name(satellite_type) = ",make_json_data_level_name(satellite_type))
    output_json_path = os.path.join(data_summary_folder_path, make_json_data_level_name(satellite_type))
    print("output json path = ",output_json_path)
    print("input json path list= ", json_path_list)
    # 5. Créer le fichier récapitulatif en combinant les fichiers JSON trouvés
    make_data_level_json_summary(json_path_list, output_json_path)

    # output_average_json_path = os.path.splitext(output_json_path)[0]+"_[average_test].json"
    # 6. faire la moyenne
    string_to_average = "per_use_case"
    calculate_average_metrics(output_json_path, output_json_path, string_to_average, verbose=True)

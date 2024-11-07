import glob
import json
import os
import re
from datetime import datetime
from typing import List, Optional, Dict, Any

import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio import RasterioIOError
from rasterio.enums import Resampling
from . import global_variables


def get_lib_version():
    return global_variables.lib_version


class MultipleBandsError(Exception):
    """Exception levée lorsque le fichier TIFF contient plusieurs bandes."""
    pass


def get_tiff_dimensions(file_path: str, verbose=False) -> tuple:
    """
    Récupère la largeur et la longueur d'un fichier TIFF en utilisant rasterio.
    Lève une exception si le fichier contient plus d'une bande.

    Args:
        file_path (str): Le chemin du fichier TIFF.

    Returns:
        tuple: Un tuple contenant la largeur et la longueur (hauteur) de l'image en pixels.

    Raises:
        MultipleBandsError: Si l'image contient plus d'une bande.
        RasterioIOError: Si le fichier ne peut pas être ouvert ou est corrompu.
    """
    try:
        # Ouvre le fichier TIFF avec rasterio
        with rasterio.open(file_path) as dataset:
            # Vérifie le nombre de bandes (canaux)
            if dataset.count > 1:
                raise MultipleBandsError(f"L'image contient plusieurs bandes : {dataset.count} bandes détectées.")

            # Récupère les dimensions de l'image
            width, height = dataset.width, dataset.height
            if verbose: print("width = [", width, "] , height = [", height, "]")
            return width, height
    except MultipleBandsError as mbe:
        print(f"Erreur : {mbe}")
        raise mbe  # Relève l'erreur pour un traitement ultérieur si besoin
    except RasterioIOError as rioe:
        print(f"Erreur lors de l'ouverture du fichier TIFF : {rioe}")
        return None, None
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
        return None, None


def find_largest_tiff(directory_path: str, verbose=False) -> tuple:
    """
    Parcourt un dossier pour trouver la plus grande image TIFF en termes de surface (largeur * hauteur).
    Utilise la fonction get_tiff_dimensions pour récupérer les dimensions.

    Args:
        directory_path (str): Le chemin du dossier contenant les fichiers TIFF.

    Returns:
        tuple: Un tuple contenant le chemin du plus grand fichier TIFF et ses dimensions (largeur, longueur).
    """
    largest_dimensions = (0, 0)  # Initialisation des dimensions maximales
    largest_file = None  # Initialisation du fichier avec la plus grande dimension
    # Cherche tous les fichiers .tif et .tiff dans le répertoire donné
    print("os cwdir =  [", os.getcwd(), "]")
    tiff_files = list_tiff_files(directory_path)
    if verbose: print("tiff files in [", directory_path, "] = ", tiff_files)
    # Parcourt tous les fichiers trouvés
    for tiff_file in tiff_files:
        try:
            dimensions = get_tiff_dimensions(os.path.join(directory_path, tiff_file), verbose)
            if dimensions:
                width, height = dimensions
                # Calcule la surface de l'image
                surface = width * height
                largest_surface = largest_dimensions[0] * largest_dimensions[1]

                # Si la surface de l'image actuelle est plus grande, on la garde
                if surface > largest_surface:
                    largest_dimensions = dimensions
                    largest_file = tiff_file
        except MultipleBandsError:
            print(f"Le fichier {tiff_file} contient plusieurs bandes et a été ignoré.")
        except RasterioIOError:
            print(f"Impossible d'ouvrir le fichier {tiff_file}.")

    if largest_file:
        return largest_file, largest_dimensions
    else:
        return None, (0, 0)  # Retourne None si aucun fichier valide n'a été trouvé


def list_json_files(target_folder: str, verbose=False) -> List[str]:
    """
    Liste tous les fichiers .json présents dans un dossier cible.

    Args:
        target_folder (str): Le chemin du dossier où chercher les fichiers .json.

    Returns:
        List[str]: Une liste des noms de fichiers .json présents dans le dossier cible.
                   La liste est vide s'il n'y a aucun fichier .json.
    """
    if verbose: print("listing json files from target_folder [", target_folder, "]...")
    # Vérifier si le dossier cible existe
    if not os.path.isdir(target_folder):
        raise ValueError(f"Le dossier spécifié n'existe pas : {target_folder}")

    # Initialiser une liste pour stocker les noms de fichiers .json
    json_files = []

    # Parcourir tous les éléments du dossier cible
    for item in os.listdir(target_folder):
        # Construire le chemin complet de l'élément
        item_path = os.path.join(target_folder, item)

        # Vérifier si l'élément est un fichier et si son extension est .json
        if os.path.isfile(item_path) and item.endswith('.json'):
            # Ajouter le fichier .json à la liste
            json_files.append(item)

    return json_files


def get_folder_size(folderpath) -> int:
    """"
    Calcule et retourne la taille totale d'un dossier en octets.

    Cette fonction parcourt de manière récursive tous les sous-dossiers et fichiers
    présents dans le répertoire spécifié par `folderpath`. Pour chaque fichier, elle
    additionne la taille du fichier au total, permettant ainsi de déterminer le poids
    total de l'ensemble du dossier.

    Args:
        folderpath (str): Le chemin vers le dossier dont on souhaite calculer la taille.

    Returns:
        int: La taille totale du dossier en octets.

    """
    total_size = 0  # Initialisation de la variable pour stocker la taille totale

    # Parcourt récursivement tous les répertoires et fichiers dans folderpath
    for dirpath, dirnames, filenames in os.walk(folderpath):

        # Parcourt chaque fichier dans le dossier courant
        for f in filenames:
            # Construit le chemin complet du fichier
            fp = os.path.join(dirpath, f)
            # Ajoute la taille du fichier à la taille totale
            total_size += os.path.getsize(fp)

    # Retourne la taille totale calculée
    return total_size


def get_compressed_size_from_folder_name(folderpath) -> int:
    """
    Extrait et retourne la taille compressée à partir du nom d'un dossier.

    Cette fonction récupère une valeur numérique spécifique, interprétée comme la taille
    compressée, en extrayant le contenu d'une paire de crochets dans le nom du dossier.
    L'extraction est effectuée en appelant une fonction utilitaire `get_bracket_content`
    qui prend le chemin du dossier et la position de l'élément dans les crochets.

    Args:
        folderpath (str): Le chemin ou le nom du dossier contenant la taille compressée
                          dans une paire de crochets.

    Returns:
        int: La taille compressée extraite du nom du dossier.

    Example:
        Si le nom du dossier est "dataset_[512MB]_compressed", la fonction retournera 512.
    """
    # Appel d'une fonction utilitaire pour extraire et convertir la taille compressée
    return int(get_bracket_content(folderpath, 1))


def calculate_compression_factor_between_two_folders(folderpath_1, folderpath_2, verbose=False) -> int:
    """
        Calcule et retourne le facteur de compression entre deux dossiers.

        Cette fonction compare la taille totale des fichiers dans un premier dossier
        avec une taille compressée spécifiée dans le nom d'un second dossier.
        Elle détermine le facteur de compression en divisant la taille du premier dossier
        par la taille compressée.

        Args:
            folderpath_1 (str): Le chemin vers le premier dossier dont la taille totale des fichiers sera calculée.
            folderpath_2 (str): Le chemin vers le second dossier contenant la taille compressée dans son nom,
                                extraite via `get_bracket_content`.

        Returns:
            int: Le facteur de compression, arrondi à deux décimales.

        Raises:
            ValueError: Si la taille compressée du dossier 2 est égale à 0, une exception est levée car
                        il est impossible de calculer un facteur de compression avec un dénominateur nul.

        Example:
            Si `folderpath_1` désigne un dossier avec 1000 Mo de données et que `folderpath_2` indique
            une taille compressée de 500 Mo dans son nom, la fonction retournera 2.0.
        """
    if verbose: print(f"calculating compression factor between {folderpath_1} and {folderpath_2}")
    size_1 = get_folder_size(folderpath_1)
    size_2 = int(get_bracket_content(folderpath_2, 1))

    # Calcul du facteur de compression
    if size_2 != 0:
        if verbose: print(f"size folder 1 = {size_2} (calculated) and folder 2 (given in folder name) ={size_2}")
        compression_factor = size_1 / size_2
        if verbose: print(f"compression_factor = {compression_factor}")
    else:
        raise ValueError("La taille du dossier 2 est 0, impossible de calculer le facteur de compression.")

    return round(compression_factor, 2)


def get_most_recent_date_index(date_list: List[str]) -> int:
    """
    Retourne l'index de la date la plus récente dans une liste de dates formatées en 'YYYYMMDD_HHMMSS'.

    Args:
        date_list (List[str]): Une liste de dates sous forme de chaînes de caractères au format 'YYYYMMDD_HHMMSS'.

    Returns:
        int: L'index de la date la plus récente dans la liste.
    """
    # Conversion des chaînes de caractères en objets datetime
    date_objects = [datetime.strptime(date_str, '%Y%m%d_%H%M%S') for date_str in date_list]

    # Trouver l'index de la date la plus récente
    most_recent_index = max(range(len(date_objects)), key=lambda i: date_objects[i])

    return most_recent_index


def get_last_json_from_use_case_result_folder(root_directory, dataset_name, test_case_number, nnvvppp_algoname, verbose=False) -> str:
    """
       Récupère le nom du fichier JSON le plus récent dans un dossier de résultats spécifique.

       Cette fonction parcourt un dossier de résultats pour trouver les fichiers JSON correspondants aux paramètres donnés.
       Elle extrait les dates des noms de fichiers JSON et identifie celui qui est le plus récent. Si aucun fichier
       JSON n'est trouvé ou si aucune date valide ne peut être extraite, la fonction retourne `None` ou lève une exception.

       Args:
           root_directory (str): Le chemin racine vers le répertoire contenant les résultats.
           dataset_name (str): Le nom du jeu de données.
           test_case_number (str): Le numéro du cas de test associé.
           nnvvppp_algoname (str): Le nom de l'algorithme spécifique.

       Returns:
           str: Le nom du fichier JSON le plus récent trouvé dans le dossier, ou `None` si aucun fichier n'est trouvé.

       Raises:
           ValueError: Si aucun fichier JSON valide ne peut être récupéré ou créé, une exception est levée pour indiquer une erreur dans les paramètres d'entrée.

       Example:
           Si `root_directory` contient plusieurs fichiers JSON avec des dates dans leurs noms, cette fonction retournera
           le fichier avec la date la plus récente.
       """

    if verbose: print("[      get_last_jsonget_last_json      ]...")
    result_folder_path = get_algorithm_results_full_path(root_directory, dataset_name, test_case_number,
                                                         nnvvppp_algoname)
    if verbose: print("[      get_last_jsonget_last_json      ] utils.get_algorithm_results_full_path = ",
                      result_folder_path, "...")
    json_file_list = list_json_files(result_folder_path, verbose=verbose)
    dates = []

    if json_file_list:
        # Extraire les dates des noms de fichiers JSON
        for json_file_name in json_file_list:
            try:
                dates.append(get_bracket_content(json_file_name, 3))
            except ValueError:
                print(f"Error extracting date from file: {json_file_name}")

        if dates:
            most_recent_index = get_most_recent_date_index(dates)
            final_json_file = json_file_list[most_recent_index]
            # print(f"Dates: {dates}")
            # print(f"Index of most recent date: {most_recent_index}")
            # print(f"Final JSON file to use is {final_json_file}")
            return final_json_file
        else:
            print("No valid dates found in JSON file names.")
    else:
        print(f"No .json found in {result_folder_path}... ")
        return None
    raise ValueError("no json file name could be get or created... verify input parameters.")


def filter_folders_by_field_number(folders: List[str], field_number: int) -> List[str]:
    """
    Filtre une liste de dossiers en fonction du nombre de champs entre crochets [].

    Args:
        folders (List[str]): Liste des noms de dossiers.
        field_number (int): Nombre de champs souhaité.

    Returns:
        List[str]: Liste de dossiers filtrés par nombre de champs.
    """
    filtered_folders = []

    # Expression régulière pour détecter les champs entre crochets
    pattern = re.compile(r'\[([^\[\]]+)\]')

    for folder in folders:
        # Trouver tous les champs entre crochets dans le dossier
        fields = pattern.findall(folder)

        # Si le nombre de champs correspond au nombre requis, on garde le dossier
        if len(fields) == field_number:
            filtered_folders.append(folder)

    return filtered_folders


def get_product_name_from_final_folder_path(original_folder_path, num_de_dossier_en_partant_de_la_fin=-2):
    """
        Extrait l'avant-dernier dossier dans un chemin donné et isole la partie spécifique du nom de dossier.

        Args:
            path (str): Le chemin de fichier complet.
            num_de_dossier_en_partant_de_la_fin(int) : de combien on recule pour prendre le  nom de dossier, -2 = on regule de 1

        Returns:
            tuple: (avant_dernier_dossier, partie_extraite)
        """
    # Récupérer l'avant-dernier dossier du chemin
    # print("getting product name from ",original_folder_path)
    path_parts = original_folder_path.split(os.sep)  # Divise le chemin en parties
    if len(path_parts) < 2:
        raise ValueError("Le chemin n'a pas suffisamment de dossiers.")

    avant_dernier_dossier = path_parts[num_de_dossier_en_partant_de_la_fin]  # Avant-dernier dossier
    # print("avant_dernier_dossier = ",avant_dernier_dossier)
    # Isoler la partie avant ']_' du dossier
    # match = re.search(r'^(\[.*?\])', avant_dernier_dossier)
    if avant_dernier_dossier:
        product_name = avant_dernier_dossier.split(']_')[1][1:]  # Enlever les crochets []
    else:
        product_name = None  # Aucun match trouvé

    return avant_dernier_dossier, product_name


def create_folder_if_do_not_exist(folder_path):
    """
    Crée un dossier s'il n'existe pas déjà.

    :param folder_path: Chemin du dossier à créer.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Dossier créé : {folder_path}")
    else:
        return
        # print(f"Le dossier existe déjà : {folder_path}")


def resample_band(input_path, output_path, scale_factor=2, resampling_method=Resampling.bilinear):
    """
    Fonction pour rééchantillonner une bande d'image raster en utilisant le
    facteur d'échelle spécifié (2 = on multiplie par 2 le nombre de pixels de l'image en x et y).
     Le rééchantillonnage est, par défaut, fait en
    utilisant la méthode du plus proche voisin, mais peut être modifié via le paramètre.

    Args:
        input_path (str): Chemin du fichier raster d'entrée.
        output_path (str): Chemin du fichier raster de sortie.
        scale_factor (float, optional): Facteur par lequel redimensionner l'image.
                                        Par défaut, le facteur est 2.
        resampling_method (rasterio.enums.Resampling, optional): Méthode de rééchantillonnage.
                                        Par défaut, la méthode du plus proche voisin (nearest ou bilinear).

    Returns:
        None. Le fichier rééchantillonné est écrit dans output_path.

    Exemple:
        resample_band("input.tif", "output.tif", scale_factor=3, resampling_method=Resampling.bilinear)
    """
    with rasterio.open(input_path) as src:
        # Récupérer les métadonnées
        profile = src.profile

        # Calculer les nouvelles dimensions
        new_width = int(src.width * scale_factor)
        new_height = int(src.height * scale_factor)

        # Mettre à jour le profil pour le fichier de sortie
        profile.update(
            width=new_width,
            height=new_height,
            transform=src.transform * src.transform.scale(
                (src.width / new_width),
                (src.height / new_height)
            )
        )

        # Rééchantillonner l'image
        data = src.read(
            out_shape=(src.count, new_height, new_width),
            resampling=resampling_method
        )

        # Écrire les données rééchantillonnées
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(data)

    print(f"{input_path} rééchantillonné et sauvegardé sous {output_path}")


def get_nn_vv_ppp_from_full_nnvvppp_algo_name(nnvvppp_algo_name: str) -> str:
    """
    Extrait la partie NN-VV-PPP du nom complet de l'algorithme.

    Args:
        nnvvppp_algo_name (str): Le nom complet de l'algorithme au format 'NN-VV-PPP_suffixedetails'.

    Returns:
        str: La partie NN-VV-PPP extraite du nom complet de l'algorithme.

    Raises:
        ValueError: Si le nom de l'algorithme ne contient pas de séparateur '_' ou si la partie avant le premier '_'
                    est trop courte pour être valide.
    """
    split_list = nnvvppp_algo_name.split("_")[0]
    if len(split_list) < 2:
        raise ValueError(
            f"Le chemin spécifié '{nnvvppp_algo_name}' n'est pas un nom valide, avoir un format nnvvppp_algoname.")
    return nnvvppp_algo_name.split("_")[0]


def get_product_path_list_from_path(path: str) -> List[str]:
    """
    Récupère tous les fichiers TIFF (.tif et .tiff) présents dans le dossier spécifié.

    Args:
        path (str): Le chemin du dossier à explorer.

    Returns:
        List[str]: Une liste des chemins complets des fichiers TIFF trouvés dans le dossier.
    """
    # Liste pour stocker les chemins des fichiers TIFF
    tiff_files = []

    # Vérifier si le chemin spécifié est un dossier
    if not os.path.isdir(path):
        raise ValueError(f"Le chemin spécifié '{path}' n'est pas un dossier valide.")

    # Lister tous les fichiers dans le dossier
    for file_name in os.listdir(path):
        # Construire le chemin complet du fichier
        file_path = os.path.join(path, file_name)

        # Vérifier si c'est un fichier
        if os.path.isfile(file_path):
            # Extraire l'extension du fichier
            _, ext = os.path.splitext(file_name)

            # Vérifier si l'extension est .tif ou .tiff
            if ext.lower() in {'.tif', '.tiff'}:
                tiff_files.append(file_path)

    return tiff_files


def add_data_to_dict(base_dict: Dict[str, Any], data_to_add: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ajoute des données au dictionnaire de base de manière modulaire.

    Args:
        base_dict (Dict[str, Any]): Le dictionnaire de base auquel les données seront ajoutées.
        data_to_add (Dict[str, Any]): Les données à ajouter au dictionnaire de base.

    Returns:
        Dict[str, Any]: Le dictionnaire mis à jour avec les nouvelles données.
    """
    for key, value in data_to_add.items():
        if isinstance(value, dict):
            # Si la valeur est un dictionnaire, on fusionne les dictionnaires récursivement
            base_dict[key] = add_data_to_dict(base_dict.get(key, {}), value)
        else:
            # Sinon, on ajoute ou remplace la valeur dans le dictionnaire de base
            base_dict[key] = value

    return base_dict


def get_product_name_list_from_path(path: str) -> List[str]:
    """
    Récupère tous les fichiers TIFF (.tif et .tiff) présents dans le dossier spécifié.

    Args:
        path (str): Le chemin du dossier à explorer.

    Returns:
        List[str]: Une liste des chemins complets des fichiers TIFF trouvés dans le dossier.
    """
    # Liste pour stocker les chemins des fichiers TIFF
    tiff_files = []

    # Vérifier si le chemin spécifié est un dossier
    if not os.path.isdir(path):
        raise ValueError(f"Le chemin spécifié '{path}' n'est pas un dossier valide.")

    # Lister tous les fichiers dans le dossier
    for file_name in os.listdir(path):
        # Construire le chemin complet du fichier
        file_path = os.path.join(path, file_name)

        # Vérifier si c'est un fichier
        if os.path.isfile(file_path):
            # Extraire l'extension du fichier
            _, ext = os.path.splitext(file_name)

            # Vérifier si l'extension est .tif ou .tiff
            if ext.lower() in {'.tif', '.tiff'}:
                tiff_files.append(os.path.basename(file_path))

    return tiff_files


def get_test_case_number_str(number, verbose=False) -> str:
    """
        Convertit un nombre entier en une chaîne de caractères sur 3 digits.

        Args:
            number: Le nombre à convertir.

        Returns:
            str: Le nombre formaté en chaîne de caractères sur 3 digits (par exemple, 1 -> '001').
        """
    if type(number) == int:
        if verbose : print(number," was an int, stranforming it to 3digit str...")
        return f"{number:03d}"
    else:
        if verbose: print(number, " already an str.")
        return number


def get_compression_factor_from_compressed_folder_name(folder_name):
    bracket_content = get_bracket_content(folder_name, 2)
    return bracket_content.split("x")[-1]


def get_compressed_folder_name() -> str:
    """
    Retourne le nom du dossier contenant les fichiers compressés.

    Returns:
        str: Le nom du dossier compressé.
    """
    return global_variables.compressed_folder_name


def get_decompressed_folder_name() -> str:
    """
    Retourne le nom du dossier contenant les fichiers décompressés.

    Returns:
        str: Le nom du dossier décompressé.
    """
    return global_variables.decompressed_folder_name


def get_original_folder_name() -> str:
    """
    Retourne le nom du dossier contenant les fichiers originaux.

    Returns:
        str: Le nom du dossier original.
    """
    return global_variables.original_folder_name


def find_matching_file(image_full_name, folder_path):
    """
    Trouve le fichier correspondant dans le répertoire donné qui commence par le nom de base spécifié.

    Args:
        image_full_name (str): Nom de base du fichier (sans extension).
        folder_path (str): Le chemin vers le répertoire où chercher les fichiers.

    Returns:
        str: Le chemin complet du fichier trouvé ou None si aucun fichier correspondant n'est trouvé.
    """
    # Construire le motif de recherche pour les fichiers qui commencent par image_full_name

    base_name = os.path.splitext(image_full_name)[0]
    # Lister tous les fichiers dans le dossier
    all_files = os.listdir(folder_path)

    # Chercher un fichier qui contient le base_name dans son nom
    for file_name in all_files:
        if base_name in file_name and file_name.endswith(('.tif', '.tiff')):
            return os.path.join(folder_path, file_name)
    return None


def get_algorithm_results_full_path(root_directory: str, dataset_name: str, test_case_number,
                                    nnvvppp_algoname: str, verbose=False) -> str:
    """
    Construit le chemin complet vers les résultats d'un algorithme spécifique pour un test donné.

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.
        nnvvppp_algoname (str): Le nom de l'algorithme dans le format NN VV PPP_algo.

    Returns:
        str: Le chemin complet vers les résultats de l'algorithme.
    """
    if verbose: print("-- get_algorithm_results_full_path -- getting algo result folder full path 1...")
    test_case_folder = get_use_case_folder(root_directory, dataset_name, get_test_case_number_str(test_case_number),
                                           verbose=verbose)
    if verbose: print("-- get_algorithm_results_full_path -- test_case_folder = ", test_case_folder)

    decompressed_folder_name = get_decompressed_folder_name()
    if verbose: print("-- get_algorithm_results_full_path -- decompressed_folder_name = ", decompressed_folder_name)

    algorithm_results_folders = get_algorithm_results_folder(root_directory, dataset_name,
                                                             get_test_case_number_str(test_case_number),
                                                             nnvvppp_algoname, verbose=verbose)
    if verbose: print("-- get_algorithm_results_full_path -- algorithm_results_folders = ", algorithm_results_folders)
    if algorithm_results_folders:

        final_path = os.path.join(root_directory,
                                  dataset_name,
                                  test_case_folder,
                                  decompressed_folder_name,
                                  algorithm_results_folders
                                  )
        if verbose: print("final path = ", final_path)
        return final_path
    else:
        return None


def get_original_full_path(root_directory: str, dataset_name: str, test_case_number: int, verbose=False) -> str:
    """
    Construit le chemin complet vers les fichiers originaux pour un test donné.

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.

    Returns:
        str: Le chemin complet vers les fichiers originaux.
    """
    return os.path.join(
        root_directory,
        dataset_name,
        get_use_case_folder(root_directory, dataset_name, get_test_case_number_str(test_case_number), verbose=verbose),
        get_original_folder_name()
    )


def get_use_case_full_path(root_directory: str, satellite_type: str, test_case_number: int, verbose=False) -> str:
    """
    Construit le chemin complet vers le dossier use case pour un test donné.

    Args:
        satellite_type (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.

    Returns:
        str: Le chemin complet vers les fichiers originaux.
    """
    return os.path.join(
        root_directory,
        satellite_type,
        get_use_case_folder(root_directory, satellite_type, get_test_case_number_str(test_case_number,verbose),verbose))


def get_satellite_full_path(root_directory: str, satellite_type: str) -> str:
    """
    Construit le chemin complet vers le dossier d'un certain satellite.

    Args:
        satellite_type (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.

    Returns:
        str: Le chemin complet vers les fichiers originaux.
    """
    return os.path.join(root_directory, satellite_type)


# Fonction pour récupérer le dernier fichier JSON dans un dossier donné
def get_latest_json_file_path_ordering_by_date_in_name(folder_path: str) -> Optional[str]:
    """
    Récupère le dernier fichier JSON dans un dossier donné, en se basant sur la date dans le nom du fichier.
    La date est supposée être dans le format 'YYYYMMDD_HHMMSS'.

    :param folder_path: Chemin du dossier où rechercher les fichiers JSON.
    :return: Chemin complet du dernier fichier JSON basé sur la date, ou None si aucun fichier n'est trouvé.
    """
    # Liste tous les fichiers dans le dossier qui ont une extension ".json"
    json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

    # Si aucun fichier JSON n'est trouvé, renvoie None
    if not json_files:
        return None

    # Regex pour extraire la date au format 'YYYYMMDD_HHMMSS'
    date_pattern = re.compile(r"(\d{8}_\d{6})")

    def extract_date_from_filename(filename: str) -> Optional[datetime]:
        match = date_pattern.search(filename)
        if match:
            # Si une date est trouvée, la convertir en objet datetime
            return datetime.strptime(match.group(1), "%Y%m%d_%H%M%S")
        return None

    # Filtre les fichiers JSON qui ont une date valide dans le nom
    json_files_with_dates = [
        (f, extract_date_from_filename(f)) for f in json_files
    ]

    # Retire les fichiers qui n'ont pas pu extraire une date valide
    json_files_with_dates = [f for f in json_files_with_dates if f[1] is not None]

    # Si aucun fichier avec une date valide n'est trouvé, renvoie None
    if not json_files_with_dates:
        return None

    # Trie les fichiers JSON par date en ordre décroissant
    json_files_with_dates.sort(key=lambda x: x[1], reverse=True)

    # Retourne le chemin complet du fichier JSON le plus récent
    return os.path.join(folder_path, json_files_with_dates[0][0])


def get_latest_json_summary_file_path(folder_path: str) -> Optional[str]:
    """
    Récupère le dernier fichier JSON summary dans un dossier donné, en se basant sur la date dans le nom du fichier.

    :param folder_path: Chemin du dossier où rechercher les fichiers JSON.
    :return: Chemin complet du dernier fichier JSON basé sur la date, ou None si aucun fichier n'est trouvé.
    """
    # Liste tous les fichiers dans le dossier qui ont une extension ".json"
    json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

    # Si aucun fichier JSON n'est trouvé, renvoie None
    if not json_files:
        return None
    # Trie les fichiers JSON par date d'analyse (extraite du nom de fichier) en ordre décroissant
    json_files.sort(
        key=lambda f: datetime.strptime(f.split('[')[-2].replace(']_', ''), "%Y%m%d_%H%M%S"),
        reverse=True
    )

    # Retourne le chemin complet du dernier fichier JSON
    return os.path.join(folder_path, json_files[0])


def get_decompressed_folder_path(root_directory: str, dataset_name: str, test_case_number, verbose=False) -> \
        Optional[str]:
    """
    Retourne le chemin du dossier decompressed ou peut se trouver le json summary

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.

    Returns:
        Optional[str]: Le chemin du decompressed folder,
        ou None si aucun dossier ne correspond.
    """
    if verbose: print("--- get_algorithm_results_folders --- starting ...")
    test_case_folder_name = get_use_case_folder(root_directory, dataset_name,
                                                get_test_case_number_str(test_case_number), verbose=verbose)
    if verbose: print("---- test case folder name = ", test_case_folder_name)
    # print("test_case_folder_name = ",test_case_folder_name)
    root_dir = os.path.join(root_directory, dataset_name, test_case_folder_name,
                            global_variables.decompressed_folder_name)
    return root_dir


def get_algorithm_results_folder(root_directory: str, dataset_name: str, test_case_number, nnvvpp_algoname: str,
                                 verbose=False) -> \
        Optional[str]:
    """
    Retourne le nom du dossier contenant les résultats d'un algorithme spécifique.

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.
        nnvvpp_algoname (str): Le nom de l'algorithme dans le format NN VV PPP_algo.

    Returns:
        Optional[str]: Le nom du dossier contenant les résultats de l'algorithme,
        ou None si aucun dossier ne correspond.
    """
    if verbose: print("--- get_algorithm_results_folders --- starting ...")
    test_case_folder_name = get_use_case_folder(root_directory, dataset_name,
                                                get_test_case_number_str(test_case_number), verbose=verbose)
    if verbose: print("---- test case folder name = ", test_case_folder_name)
    # print("test_case_folder_name = ",test_case_folder_name)
    root_dir = os.path.join(root_directory, dataset_name, test_case_folder_name,
                            global_variables.decompressed_folder_name)
    if verbose: print("--- get_algorithm_results_folders --- root dir = ", root_dir)

    result = list_matching_folders(root_dir=root_dir, search_str=nnvvpp_algoname, bracket_num=0, verbose=verbose).pop(0)
    if verbose: print("--- get_algorithm_results_folders --- list of matching folders = ",
                      list_matching_folders(root_dir=root_dir, search_str=nnvvpp_algoname, bracket_num=0,
                                            verbose=verbose))

    return result


def get_use_case_folder(root_directory: str, dataset_name: str, test_case_number, verbose=False) -> Optional[str]:
    """
    Retourne le nom du dossier contenant les données pour un test donné.

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.

    Returns:
        Optional[str]: Le nom du dossier de test case, ou None si aucun dossier ne correspond.
    """
    test_case_root_folder = os.path.join(root_directory, dataset_name)
    if verbose: print("get_use_case_folder ----> test_case_root_folder = ", test_case_root_folder)
    result = list_matching_folders(test_case_root_folder, get_test_case_number_str(test_case_number), 0,
                                   verbose=verbose).pop(0)
    if verbose: print("get_use_case_folder ----> result = ", result)
    return result


def get_bracket_content(folder_name: str, bracket_num: int) -> str:
    """
    Extrait le Nième champ entre crochets dans une chaîne de caractères et vérifie s'il contient une sous-chaîne spécifique.

    Args:
        folder_name (str): Le nom du dossier au format [001]_[1c_256_256]_[1]..[] ou chempin du dossier
        (si c est un chemin de dossier, alors on le découpera et regardera uniquement le dernier dossier.
        search_str (str): La sous-chaîne à rechercher dans le champ extrait.
        bracket_num (int): Le numéro du champ entre crochets à extraire (commençant à 0).

    Returns:
        bool: True si le Nième champ contient la sous-chaîne, False sinon.
    """
    # Extraire tous les champs entre crochets
    # print("checking bracket contents for ",search_str,"...")
    # Vérifier si folder_name est un chemin complet et extraire le nom du dernier dossier
    if os.path.sep in folder_name:
        folder_name = os.path.basename(folder_name)

    fields = folder_name.split('[')[1:]  # Diviser la chaîne et ignorer tout avant le premier crochet ouvrant
    # print("fields = ",fields)
    fields = [field.split(']')[0] for field in fields]  # Extraire les contenus des crochets
    # print("fields = ",fields)

    # Vérifier que le numéro de champ demandé est valide
    if 0 <= bracket_num <= len(fields):
        # Extraire le Nième champ
        selected_field = fields[bracket_num]

        return selected_field
    else:
        # Si le numéro de champ est invalide, retourner False
        raise ValueError("Si le numéro de champ est invalide ou le champs n'existe pas")


def check_bracket_content(folder_name: str, search_str: str, bracket_num: int, verbose=False) -> bool:
    """
    Extrait le Nième champ entre crochets dans une chaîne de caractères et vérifie s'il contient une sous-chaîne spécifique.

    Args:
        folder_name (str): Le nom du dossier au format [001]_[1c_256_256]_[1]..[].
        search_str (str): La sous-chaîne à rechercher dans le champ extrait.
        bracket_num (int): Le numéro du champ entre crochets à extraire (commençant à 0).

    Returns:
        bool: True si le Nième champ contient la sous-chaîne, False sinon.
    """
    # Extraire tous les champs entre crochets
    # print("checking bracket contents for ",search_str,"...")
    # Vérifier si folder_name est un chemin complet et extraire le nom du dernier dossier
    if verbose: print("---- check_bracket_content ---- trying to find ", folder_name, " in ", folder_name,
                      " at bracket number ", bracket_num, " ...")
    if os.path.sep in folder_name:
        folder_name = os.path.basename(folder_name)

    fields = folder_name.split('[')[1:]  # Diviser la chaîne et ignorer tout avant le premier crochet ouvrant
    if verbose: print(
        "---- check_bracket_content ---- Diviser la chaîne et ignorer tout avant le premier crochet ouvrant = ", fields)

    fields = [field.split(']')[0] for field in fields]  # Extraire les contenus des crochets
    if verbose: print("---- check_bracket_content ---- Extraire les contenus des crochets = ", fields)

    # print("fields = ",fields)

    # Vérifier que le numéro de champ demandé est valide

    if 0 <= bracket_num <= len(fields) and len(fields) != 0:
        # Extraire le Nième champ
        selected_field = fields[bracket_num]
        # Vérifier si la sous-chaîne est présente
        # print(search_str in selected_field)
        if verbose:
            print("---- check_bracket_content ---- selected_field = ", selected_field)
            print("---- check_bracket_content ---- search_str in selected_field = ", search_str in selected_field)
        return search_str in selected_field
    else:
        # Si le numéro de champ est invalide, retourner False
        if verbose: print("---- check_bracket_content ---- Si le numéro de champ est invalide, retourner False ")

        return False


def list_matching_folders(root_dir: str, search_str: str, bracket_num: int, verbose=False) -> List[str]:
    """
    Liste les sous-dossiers d'un répertoire racine et vérifie si le Nième champ
    entre crochets dans leur nom contient une sous-chaîne spécifique.

    Args:
        root_dir (str): Le chemin du répertoire racine.
        search_str (str): La sous-chaîne à rechercher dans le Nième champ.
        bracket_num (int): Le numéro du champ entre crochets à vérifier (commençant à 1).

    Returns:
        List[str]: Une liste de chemins complets des sous-dossiers correspondants.
    """
    if verbose: print("list_matching_folders --> matching folders from ", root_dir, ", trying to find ", search_str,
                      " in bracket number ", bracket_num, "...")
    matching_folders = []
    list_of_dirs = os.listdir(root_dir)
    # Lister tous les sous-dossiers dans le répertoire racine
    if verbose:
        print("list_matching_folders --> LIST OF DIRS : ", list_of_dirs)

    for folder_name in list_of_dirs:
        if verbose:
            print("list_matching_folders --> folder name [", folder_name, "]...")
        folder_path = os.path.join(root_dir, folder_name)

        # Vérifier si l'élément est bien un dossier
        if os.path.isdir(folder_path):
            # Utiliser check_bracket_content pour vérifier le contenu du Nième champ
            is_content_found = check_bracket_content(folder_name, search_str, bracket_num, verbose=verbose)
            if verbose:
                print("list_matching_folders --> is_content_found = ", is_content_found, "")

            if is_content_found:
                if verbose:
                    print("list_matching_folders --> folder FOUND [", folder_name, "].")

                # Si trouvé, ajouter le chemin complet du dossier à la liste
                matching_folders.append(folder_name)

    if verbose: print("list_matching_folders --> returns : ", matching_folders, ".")
    return matching_folders


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize the image for display, regardless of the value range.

    This function adjusts the image data to a standard range for display purposes.
    It handles different data types and scales the image values accordingly.

    Args:
        image (np.ndarray): The input image as a NumPy array.

    Returns:
        np.ndarray: The normalized image.
    """
    # Check the data type and normalize accordingly
    if image.dtype == np.uint16:
        # For 16-bit unsigned integer images, scale to the range [0, 1]
        image = image.astype(np.float32) / 65535.0
    elif image.dtype == np.float32:
        # For floating-point images, clip values to the range [0, 1]
        image = np.clip(image, 0, 1)
    else:
        # For other data types, normalize to the range [0, 1]
        image = image.astype(np.float32)
        image_min = np.min(image)
        image_max = np.max(image)
        # Avoid division by zero if the image has a uniform value
        if image_max > image_min:
            image = (image - image_min) / (image_max - image_min)
        else:
            image = np.zeros_like(image)

    return image


def display_multiband_tiffs(image1: np.ndarray, image2: np.ndarray) -> None:
    """
    Display two TIFF images with appropriate normalization and visualization.

    This function displays two images side by side. It handles different numbers of channels and normalizes
    the images for better visualization. It supports single-channel, multi-channel (e.g., RGB), and images
    with more than three channels.

    Args:
        image1 (np.ndarray): The first image as a NumPy array (HxWxC or HxW).
        image2 (np.ndarray): The second image as a NumPy array (HxWxC or HxW).

    Returns:
        None
    """
    plt.figure(figsize=(10, 5))

    # Normalize images for display
    image1 = normalize_image(image1)
    image2 = normalize_image(image2)

    plt.subplot(1, 2, 1)
    plt.title('Image 1')
    if image1.ndim == 3:
        if image1.shape[2] == 1:
            # Display single-channel image as grayscale
            plt.imshow(image1[:, :, 0], cmap='gray')
        if image1.shape[2] == 2:
            # Display  a two-channel image
            plt.imshow(image1[:, :, :1])
        elif image1.shape[2] == 3:
            # Display RGB image
            plt.imshow(image1)
        else:
            # Display the first three channels of an image with more than 3 channels
            img_to_show = image1[:, :, :3]
            # Normalize data for better visualization
            img_to_show = (img_to_show - np.min(img_to_show)) / (np.max(img_to_show) - np.min(img_to_show))
            plt.imshow(img_to_show)
    elif image1.ndim == 2:
        # Display grayscale image
        plt.imshow(image1, cmap='gray')
    plt.axis('off')

    # Display Image 2
    plt.subplot(1, 2, 2)
    plt.title('Image 2')
    if image2.ndim == 3:
        if image2.shape[2] == 1:
            # Display single-channel image as grayscale
            plt.imshow(image2[:, :, 0], cmap='gray')
        if image2.shape[2] == 2:
            # Display a two-channel image
            plt.imshow(image2[:, :, :1])
        elif image2.shape[2] == 3:
            # Display RGB image
            plt.imshow(image2)
        else:
            # Display the first three channels of an image with more than 3 channels
            img_to_show = image2[:, :, :3]
            # Normalize data for better visualization
            img_to_show = (img_to_show - np.min(img_to_show)) / (np.max(img_to_show) - np.min(img_to_show))
            plt.imshow(img_to_show)
    elif image2.ndim == 2:
        # Display grayscale image
        plt.imshow(image2, cmap='gray')
    plt.axis('off')

    plt.show()


def reformat_date(input_date: str) -> str:
    """
    Reformate une chaîne de date au format 'YYYYMMDD_HHMMSS' en 'YYYY-MM-DD HH:MM:SS'.

    :param input_date: La chaîne de date à reformater.
    :return: La chaîne de date reformée.
    """
    # Vérifie que la chaîne a la longueur attendue
    if len(input_date) != 15 or input_date[8] != '_':
        raise ValueError("La date doit être au format 'YYYYMMDD_HHMMSS'")

    # Sépare la date et l'heure
    date_part = input_date[:8]  # 'YYYYMMDD'
    time_part = input_date[9:]  # 'HHMMSS'

    # Reformate la date
    reformatted_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]} {time_part[:2]}:{time_part[2:4]}:{time_part[4:]}"

    return reformatted_date


def list_directories(base_path="decompressed"):
    """
    Liste tous les dossiers dans un répertoire donné.

    Args:
        base_path (str): Le chemin du dossier à inspecter (par défaut "decompressed").

    Returns:
        list: Une liste des noms de dossiers trouvés dans le répertoire spécifié.
    """
    try:
        # Vérifie si le chemin spécifié existe
        if not os.path.exists(base_path):
            print(f"Le dossier '{base_path}' n'existe pas.")
            return []

        # Liste des dossiers
        directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

        return directories

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return []


def list_csv_files(directory_path: str):
    """
    Liste tous les fichiers CSV dans un dossier donné.

    Parameters:
    directory_path (str): Le chemin vers le dossier où chercher les fichiers CSV.

    Returns:
    list: Une liste contenant les noms de fichiers CSV.
    """
    # Vérifie que le dossier existe
    if not os.path.exists(directory_path):
        print(f"Le dossier {directory_path} n'existe pas.")
        return []

    # Liste tous les fichiers dans le dossier et filtre uniquement ceux avec l'extension .csv
    csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

    return csv_files


def list_tiff_files(directory_path: str):
    """
    Liste tous les fichiers tiff et tif dans un dossier donné.

    Parameters:
    directory_path (str): Le chemin vers le dossier où chercher les fichiers CSV.

    Returns:
    list: Une liste contenant les noms de fichiers CSV.
    """
    # Vérifie que le dossier existe
    if not os.path.exists(directory_path):
        print(f"Le dossier {directory_path} n'existe pas.")
        return []

    # Liste tous les fichiers dans le dossier et filtre uniquement ceux avec l'extension .csv
    csv_files = [file for file in os.listdir(directory_path) if file.endswith(('.tif', '.tiff'))]

    return csv_files


def save_json_data_into_file(data: Dict, file_path: str) -> None:
    """
    Sauvegarde un dictionnaire Python dans un fichier JSON.

    :param data: Le dictionnaire à sauvegarder.
    :param file_path: Le chemin complet vers le fichier où sauvegarder le JSON.
    """
    try:
        # Ouverture du fichier en mode écriture
        with open(file_path, 'w', encoding='utf-8') as file:
            # Sauvegarde du dictionnaire sous forme de JSON avec indentation pour la lisibilité
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Le fichier JSON a été sauvegardé avec succès à : {file_path}")
    except Exception as e:
        # Gestion des erreurs
        print(f"Une erreur est survenue lors de la sauvegarde du fichier : {e}")

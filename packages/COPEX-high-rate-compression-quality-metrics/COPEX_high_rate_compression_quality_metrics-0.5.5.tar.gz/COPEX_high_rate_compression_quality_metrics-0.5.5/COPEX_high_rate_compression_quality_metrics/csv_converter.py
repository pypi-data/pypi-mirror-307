# convertisseur qui permet de formatter des données sour forme de plot standardisé
import csv
import os.path

import matplotlib.pyplot as plt

from . import utils, global_variables


def csv_to_png_plot_metric_vs_compression_factor(csv_input_path: str, png_output_path: str, metric: str, verbose=False,
                                                 show_output=False, auto_scale=False):
    """
    Génère un graphique montrant l'évolution de LPIPS en fonction du facteur de compression
    pour plusieurs algorithmes à partir des données d'un fichier CSV, puis enregistre le graphique sous forme de fichier PNG.

    :param csv_input_path: Chemin vers le fichier CSV contenant les données (Algorithm, LPIPS, Compression Factor).
    :param png_output_path: Chemin vers l'image PNG à générer et sauvegarder.
    :param metric: The metric you want to print
    :param verbose: Booléen pour activer les messages d'information supplémentaires.
    :param show_output: plot the output if true
    :param auto_scale: if auto_scale is True, scale is made given no specific rule (based on data used),
    but if its false, it is based on global variable dictionnary

    """

    # Dictionnaire pour stocker les données de chaque algorithme
    algorithm_data = {}

    # Lire le fichier CSV
    with open(csv_input_path, 'r') as csv_file:
        reader = csv.reader(csv_file)

        # Sauter l'en-tête
        next(reader)

        # Récupérer les informations du fichier CSV
        for row in reader:
            algorithm_full_name = row[0]  # Nom complet de l'algorithme
            lpips_value = float(row[1])  # Valeur de LPIPS
            compression_factor = float(row[2])  # Facteur de compression

            # Extraire le nom de l'algorithme
            algorithm_name = algorithm_full_name.split('_')[1]  # On prend la deuxième partie

            # Si l'algorithme n'est pas encore dans le dictionnaire, l'initialiser
            if algorithm_name not in algorithm_data:
                algorithm_data[algorithm_name] = {
                    metric: [],
                    'compression': []
                }

            # Ajouter les valeurs dans les listes correspondantes
            algorithm_data[algorithm_name][metric].append(lpips_value)
            algorithm_data[algorithm_name]['compression'].append(compression_factor)

    # Affichage des données si verbose est activé
    if verbose:
        print("Données par algorithme :")
        for algo, data in algorithm_data.items():
            print(f"{algo} : {metric} - {data[metric]}, Compression - {data['compression']}")

    # Vérifier si la métrique est valide
    if metric not in global_variables.metrics_dictionary:
        raise ValueError(
            f"Métrique '{metric}' non reconnue. Choisissez parmi {list(global_variables.metrics_dictionary.keys())}.")

    # Générer le graphique
    plt.figure(figsize=(10, 6))

    # Tracer les données pour chaque algorithme
    for algorithm_name, data in algorithm_data.items():
        color = global_variables.algorithm_colors.get(algorithm_name,
                                                      'blue')  # Utiliser la couleur définie ou bleu par défaut
        plt.plot(data['compression'], data[metric], marker='o', linestyle='-', label=algorithm_name, color=color)

    # Ajouter des étiquettes et un titre
    plt.xlabel('Compression Factor')
    plt.ylabel(f'{metric} Value')
    plt.title(f'{metric} vs Compression Factor for Various Algorithms')

    # Définir les limites des axes
    if not auto_scale:
        plt.xlim(global_variables.data_range_for_compression["min"], global_variables.data_range_for_compression["max"])
        plt.ylim(global_variables.metrics_dictionary[metric]["min"], global_variables.metrics_dictionary[metric]["max"])

    # Ajouter la légende
    plt.legend()

    # Ajouter une grille
    plt.grid(True)

    # Sauvegarder le graphique sous forme de fichier PNG
    plt.savefig(png_output_path)

    # Afficher le graphique dans la console si nécessaire
    if show_output:
        plt.show()

    print(f"Le graphique a été sauvegardé sous '{png_output_path}'.")


# TODO csv_to_png_plot_thematic_vs_compression_factor est juste une copie de csv_to_png_plot_metric_vs_compression_factor
def csv_to_png_plot_thematic_vs_compression_factor(csv_input_path: str, png_output_path: str, metric: str,
                                                   verbose=False, show_output=False):
    """
    Génère un graphique montrant l'évolution de LPIPS en fonction du facteur de compression
    pour plusieurs algorithmes à partir des données d'un fichier CSV, puis enregistre le graphique sous forme de fichier PNG.

    :param csv_input_path: Chemin vers le fichier CSV contenant les données (Algorithm, LPIPS, Compression Factor).
    :param png_output_path: Chemin vers l'image PNG à générer et sauvegarder.
    :param verbose: Booléen pour activer les messages d'information supplémentaires.
    """

    # Dictionnaire pour stocker les données de chaque algorithme
    algorithm_data = {}

    # Lire le fichier CSV
    with open(csv_input_path, 'r') as csv_file:
        reader = csv.reader(csv_file)

        # Sauter l'en-tête
        next(reader)

        # Récupérer les informations du fichier CSV
        for row in reader:
            algorithm_full_name = row[0]  # Nom complet de l'algorithme
            lpips_value = float(row[1])  # Valeur de LPIPS
            compression_factor = float(row[2])  # Facteur de compression

            # Extraire le nom de l'algorithme
            algorithm_name = algorithm_full_name.split('_')[1]  # On prend la deuxième partie

            # Si l'algorithme n'est pas encore dans le dictionnaire, l'initialiser
            if algorithm_name not in algorithm_data:
                algorithm_data[algorithm_name] = {
                    metric: [],
                    'compression': []
                }

            # Ajouter les valeurs dans les listes correspondantes
            algorithm_data[algorithm_name][metric].append(lpips_value)
            algorithm_data[algorithm_name]['compression'].append(compression_factor)

    # Affichage des données si verbose est activé
    if verbose:
        print("Données par algorithme :")
        for algo, data in algorithm_data.items():
            print(f"{algo} : {metric} - {data[metric]}, Compression - {data['compression']}")

    # Vérifier si la métrique est valide
    if metric not in global_variables.metrics_dictionary:
        raise ValueError(
            f"Métrique '{metric}' non reconnue. Choisissez parmi {list(global_variables.metrics_dictionary.keys())}.")

    # Générer le graphique
    plt.figure(figsize=(10, 6))

    # Tracer les données pour chaque algorithme
    for algorithm_name, data in algorithm_data.items():
        color = global_variables.algorithm_colors.get(algorithm_name,
                                                      'blue')  # Utiliser la couleur définie ou bleu par défaut
        plt.plot(data['compression'], data[metric], marker='o', linestyle='-', label=algorithm_name, color=color)

    # Ajouter des étiquettes et un titre
    plt.xlabel('Compression Factor')
    plt.ylabel(f'{metric} Value')
    plt.title(f'{metric} vs Compression Factor for Various Algorithms')

    # Définir les limites des axes
    plt.xlim(global_variables.data_range_for_compression["min"], global_variables.data_range_for_compression["max"])
    plt.ylim(global_variables.metrics_dictionary[metric]["min"], global_variables.metrics_dictionary[metric]["max"])

    # Ajouter la légende
    plt.legend()

    # Ajouter une grille
    plt.grid(True)

    # Sauvegarder le graphique sous forme de fichier PNG
    plt.savefig(png_output_path)

    # Afficher le graphique dans la console si nécessaire
    if show_output:
        plt.show()

    print(f"Le graphique a été sauvegardé sous '{png_output_path}'.")


def csv_to_png_plot_rowA_on_y_axis_vs_rowB_on_x_axis(csv_input_path: str, png_output_path: str, rowA: str, rowB: str,
                                                     verbose=False, show_output=False):
    """
    Génère un graphique montrant l'évolution de LPIPS en fonction du facteur de compression
    pour plusieurs algorithmes à partir des données d'un fichier CSV, puis enregistre le graphique sous forme de fichier PNG.

    :param csv_input_path: Chemin vers le fichier CSV contenant les données (Algorithm, LPIPS, Compression Factor).
    :param png_output_path: Chemin vers l'image PNG à générer et sauvegarder.
    :param verbose: Booléen pour activer les messages d'information supplémentaires.
    """

    # Dictionnaire pour stocker les données de chaque algorithme
    algorithm_data = {}

    # Lire le fichier CSV
    with open(csv_input_path, 'r') as csv_file:
        reader = csv.reader(csv_file)

        # Sauter l'en-tête
        next(reader)

        # Récupérer les informations du fichier CSV
        for row in reader:
            algorithm_full_name = row[0]  # Nom complet de l'algorithme
            lpips_value = float(row[1])  # Valeur de LPIPS
            compression_factor = float(row[2])  # Facteur de compression

            # Extraire le nom de l'algorithme
            algorithm_name = algorithm_full_name.split('_')[1]  # On prend la deuxième partie

            # Si l'algorithme n'est pas encore dans le dictionnaire, l'initialiser
            if algorithm_name not in algorithm_data:
                algorithm_data[algorithm_name] = {
                    rowA: [],
                    rowB: []
                }

            # Ajouter les valeurs dans les listes correspondantes
            algorithm_data[algorithm_name][rowA].append(lpips_value)
            algorithm_data[algorithm_name][rowB].append(compression_factor)

    # Affichage des données si verbose est activé
    if verbose:
        print("Données par algorithme :")
        for algo, data in algorithm_data.items():
            print(f"{algo} : {rowA} - {data[rowA]}, Compression - {data[rowB]}")

    # Générer le graphique
    plt.figure(figsize=(10, 6))

    # Tracer les données pour chaque algorithme
    for algorithm_name, data in algorithm_data.items():
        color = global_variables.algorithm_colors.get(algorithm_name,
                                                      'blue')  # Utiliser la couleur définie ou bleu par défaut
        plt.plot(data[rowB], data[rowA], marker='o', linestyle='-', label=algorithm_name, color=color)

    # Ajouter des étiquettes et un titre
    plt.xlabel('Compression Factor')
    plt.ylabel(f'{rowA} Value')
    plt.title(f'{rowA} vs Compression Factor for Various Algorithms')

    # Ajouter la légende
    plt.legend()

    # Ajouter une grille
    plt.grid(True)

    # Sauvegarder le graphique sous forme de fichier PNG
    plt.savefig(png_output_path)

    # Afficher le graphique dans la console si nécessaire
    if show_output:
        plt.show()

    print(f"Le graphique a été sauvegardé sous '{png_output_path}'.")


def csv_to_png_plot_for_all_metrics(csv_input_path: str, output_folder: str, verbose=False, show_output=False,
                                    auto_scale=False):
    """
    Génère un graphique pour chaque métrique (LPIPS, SSIM, PSNR, RMSE) montrant l'évolution en fonction du facteur de compression
    pour plusieurs algorithmes à partir des données d'un fichier CSV, puis enregistre chaque graphique sous forme de fichier PNG.

    :param csv_input_path: Chemin vers le fichier CSV contenant les données (Algorithm, Compression Factor, LPIPS, SSIM, PSNR, RMSE).
    :param output_folder: Chemin vers le dossier où les images PNG seront sauvegardées.
    :param verbose: Booléen pour activer les messages d'information supplémentaires.
    :param show_output: plot the output if true
    :param auto_scale: if auto_scale is True, scale is made given no specific rule (based on data used),
    but if its false, it is based on global variable dictionnary
    """

    # Vérifier si le dossier de sortie existe, sinon le créer
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Dictionnaire pour stocker les données de chaque algorithme pour chaque métrique
    algorithm_data = {}

    # Liste des métriques à traiter (colonne 2 à 5 du CSV)
    metrics = global_variables.metrics_dictionary.keys()

    # Lire le fichier CSV
    with open(csv_input_path, 'r') as csv_file:
        reader = csv.reader(csv_file)

        # Sauter l'en-tête
        next(reader)

        # Récupérer les informations du fichier CSV
        for row in reader:
            algorithm_full_name = row[0]  # Nom complet de l'algorithme
            compression_factor = float(row[1])  # Facteur de compression

            # Extraire le nom de l'algorithme
            algorithm_name = algorithm_full_name.split('_')[1]  # On prend la deuxième partie

            # Si l'algorithme n'est pas encore dans le dictionnaire, l'initialiser
            if algorithm_name not in algorithm_data:
                algorithm_data[algorithm_name] = {metric: [] for metric in metrics}
                algorithm_data[algorithm_name]['compression'] = []

            # Ajouter les valeurs dans les listes correspondantes pour chaque métrique
            algorithm_data[algorithm_name]['compression'].append(compression_factor)
            for i, metric in enumerate(metrics):
                algorithm_data[algorithm_name][metric].append(
                    float(row[i + 2]))  # Les valeurs des métriques sont dans les colonnes 3 à 6

    # Générer un graphique pour chaque métrique
    for metric in metrics:
        if verbose:
            print(f"Génération du graphique pour la métrique : {metric}")

        # Créer le graphique
        plt.figure(figsize=(10, 6))

        # Tracer les données pour chaque algorithme
        for algorithm_name, data in algorithm_data.items():
            color = global_variables.algorithm_colors.get(algorithm_name,
                                                          'blue')  # Utiliser la couleur définie ou bleu par défaut
            plt.plot(data['compression'], data[metric], marker='o', linestyle='-', label=algorithm_name, color=color)

        # Ajouter des étiquettes et un titre
        plt.xlabel('Compression Factor')
        plt.ylabel(f'{metric} Value')
        plt.title(f'{metric} vs Compression Factor for Various Algorithms')

        # Définir les limites des axes
        if auto_scale is False:
            plt.xlim(global_variables.data_range_for_compression["min"],
                     global_variables.data_range_for_compression["max"])
            plt.ylim(global_variables.metrics_dictionary[metric]["min"],
                     global_variables.metrics_dictionary[metric]["max"])

        # Ajouter la légende
        plt.legend()

        # Ajouter une grille
        plt.grid(True)

        # Sauvegarder le graphique sous forme de fichier PNG
        png_output_path = os.path.join(output_folder, f"{metric}_vs_Compression.png")
        plt.savefig(png_output_path)

        # Afficher le graphique dans la console si nécessaire
        if show_output:
            plt.show()

        # Indiquer que le graphique a été sauvegardé
        if verbose:
            print(f"Le graphique '{metric}' a été sauvegardé sous '{png_output_path}'.")

    print("Tous les graphiques ont été générés et sauvegardés.")


def csv_mono_metric_to_png_plot_from_decompressed_folder_name_per_band(root_directory: str, dataset_name: str,
                                                                       test_case_number,
                                                                       verbose=True):
    decompressed_folder_path = utils.get_decompressed_folder_path(root_directory, dataset_name, test_case_number,
                                                                  verbose=verbose)
    summary_csv_folder_path = os.path.join(decompressed_folder_path, global_variables.summary_output_folder_name,
                                           global_variables.summary_output_csv_folder_name,
                                           global_variables.summary_output_per_band_folder_name)
    summary_png_folder_path = os.path.join(decompressed_folder_path, global_variables.summary_output_folder_name,
                                           global_variables.summary_output_png_folder_name,
                                           global_variables.summary_output_per_band_folder_name)
    utils.create_folder_if_do_not_exist(summary_png_folder_path)
    csv_files = utils.list_csv_files(summary_csv_folder_path)
    print(csv_files)
    for csv_file_name in csv_files:
        input_csv_path = os.path.join(summary_csv_folder_path, csv_file_name)
        png_file_name = csv_file_name.split(".")[0] + ".png"
        wanted_metric = png_file_name.split(".")[0].split("_")[-1]
        output_png_path = os.path.join(summary_png_folder_path, png_file_name)
        csv_to_png_plot_metric_vs_compression_factor(input_csv_path, output_png_path, wanted_metric, verbose=True)


def csv_multi_metric_to_png_plot_from_decompressed_folder_name_per_band(root_directory: str, dataset_name: str,
                                                                        test_case_number,
                                                                        verbose=True):
    decompressed_folder_path = utils.get_decompressed_folder_path(root_directory, dataset_name, test_case_number,
                                                                  verbose=verbose)
    summary_csv_folder_path = os.path.join(decompressed_folder_path, global_variables.summary_output_folder_name,
                                           global_variables.summary_output_csv_folder_name,
                                           global_variables.summary_output_per_band_folder_name)
    summary_png_folder_path = os.path.join(decompressed_folder_path, global_variables.summary_output_folder_name,
                                           global_variables.summary_output_png_folder_name,
                                           global_variables.summary_output_per_band_folder_name)
    utils.create_folder_if_do_not_exist(summary_png_folder_path)
    csv_files = utils.list_csv_files(summary_csv_folder_path)
    print(csv_files)
    for csv_file_name in csv_files:
        input_csv_path = os.path.join(summary_csv_folder_path, csv_file_name)
        png_file_name = csv_file_name.split(".")[0] + ".png"
        output_png_folder_path = os.path.join(summary_png_folder_path, png_file_name.split(".")[0])
        csv_to_png_plot_for_all_metrics(input_csv_path, output_png_folder_path, verbose=True)


def csv_multi_metric_to_png_plot_from_decompressed_folder_name_all_bands(root_directory: str, dataset_name: str,
                                                                         test_case_number,
                                                                         verbose=True):
    decompressed_folder_path = utils.get_decompressed_folder_path(root_directory, dataset_name, test_case_number,
                                                                  verbose=verbose)
    summary_csv_folder_path = os.path.join(decompressed_folder_path, global_variables.summary_output_folder_name,
                                           global_variables.summary_output_csv_folder_name,
                                           global_variables.summary_output_all_bands_folder_name)
    summary_png_folder_path = os.path.join(decompressed_folder_path, global_variables.summary_output_folder_name,
                                           global_variables.summary_output_png_folder_name,
                                           global_variables.summary_output_all_bands_folder_name)
    utils.create_folder_if_do_not_exist(summary_png_folder_path)
    csv_files = utils.list_csv_files(summary_csv_folder_path)
    print(csv_files)
    for csv_file_name in csv_files:
        input_csv_path = os.path.join(summary_csv_folder_path, csv_file_name)
        png_file_name = csv_file_name.split(".")[0] + ".png"
        output_png_folder_path = os.path.join(summary_png_folder_path, png_file_name.split(".")[0])
        if csv_file_name.__contains__("stdev"):
            csv_to_png_plot_for_all_metrics(input_csv_path, output_png_folder_path, verbose=True, auto_scale=True)
        else:
            csv_to_png_plot_for_all_metrics(input_csv_path, output_png_folder_path, verbose=True, auto_scale=False)

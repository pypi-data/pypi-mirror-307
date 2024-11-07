import argparse
import os

from COPEX_high_rate_compression_quality_metrics import json_builder
# Partie du code permettant l'utilisation de COPEX_high_rate_compression_quality_metrics en ligne de commande

# Remplacez ce chemin par le chemin obtenu précédemment
os.environ['GDAL_DATA'] = r'D:\VisioTerra\technique\P382_ESRIN_COPEX-DCC\engineering\COPEX_high_rate_compression_quality_metrics\python_interpreter_test\Lib\site-packages\rasterio\gdal-data'

# Vérifiez que GDAL_DATA est correctement défini
print("GDAL_DATA est défini sur :", os.environ['GDAL_DATA'])

def main():
    # Initialiser l'analyseur d'arguments
    parser = argparse.ArgumentParser(
        description="Outil pour créer des métriques et résumés JSON à partir des données satellitaires.")

    # Sous-commandes pour chaque fonction disponible
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # Commande pour `make_generic`
    parser_generic = subparsers.add_parser('make_generic', help="Exécuter la fonction make_generic.")
    parser_generic.add_argument('root_directory', type=str, help="Le répertoire racine contenant les données.")
    parser_generic.add_argument('dataset_name', type=str, help="Le nom du dataset.")
    parser_generic.add_argument('test_case_number', type=str, help="Le numéro du test case.")
    parser_generic.add_argument('nnvvppp_algoname', type=str, help="Le nom de l'algorithme.")
    parser_generic.add_argument('--verbose', action='store_true', help="Afficher des informations supplémentaires.")
    parser_generic.add_argument('--computing_block_size', type=int, default=2500, help="La taille du block de calcul pour les metriques gourmandes.")

    # Commande pour `make_thematic`
    parser_thematic = subparsers.add_parser('make_thematic', help="Exécuter la fonction make_thematic.")
    parser_thematic.add_argument('root_directory', type=str, help="Le répertoire racine.")
    parser_thematic.add_argument('dataset_name', type=str, help="Le nom du dataset.")
    parser_thematic.add_argument('test_case_number', type=str, help="Le numéro du test case.")
    parser_thematic.add_argument('nnvvppp_algoname', type=str, help="Le nom de l'algorithme.")
    parser_thematic.add_argument('thematic_function', type=str, help="La fonction thématique à utiliser.")
    parser_thematic.add_argument('--verbose', action='store_true', help="Afficher des informations supplémentaires.")
    parser_thematic.add_argument('thematic_args', nargs='*', help="Arguments pour la fonction thématique.")

    # Commande pour `create_summary_json_from_use_case_path_at_use_case_level`
    parser_summary_use_case = subparsers.add_parser('create_summary_json_use_case',
                                                    help="Créer un résumé JSON au niveau du cas d'utilisation.")
    parser_summary_use_case.add_argument('root_directory', type=str, help="Le répertoire racine.")
    parser_summary_use_case.add_argument('satellite_type', type=str, help="Le type de satellite.")
    parser_summary_use_case.add_argument('test_case_number', help="Le numéro du test case.")

    # Commande pour `create_summary_json_at_satellite_type_level_from_data_folder`
    parser_summary_satellite_type = subparsers.add_parser('create_summary_json_satellite_type',
                                                          help="Créer un résumé JSON au niveau du type de satellite.")
    parser_summary_satellite_type.add_argument('root_directory', type=str, help="Le répertoire racine.")
    parser_summary_satellite_type.add_argument('satellite_type', type=str, help="Le type de satellite.")
    parser_summary_satellite_type.add_argument('--verbose', action='store_true',
                                               help="Afficher des informations supplémentaires.")

    # Analyse des arguments
    args = parser.parse_args()

    # Exécution de la fonction correspondante
    if args.command == 'make_generic':
        json_builder.make_generic(args.root_directory, args.dataset_name, args.test_case_number, args.nnvvppp_algoname, args.verbose,
                     args.computing_block_size)

    elif args.command == 'make_thematic':
        json_builder.make_thematic(args.root_directory, args.dataset_name, args.test_case_number, args.nnvvppp_algoname,
                      args.thematic_function, args.verbose, *args.thematic_args)

    elif args.command == 'create_summary_json_use_case':
        json_builder.create_summary_json_from_use_case_path_at_use_case_level(args.root_directory, args.satellite_type,
                                                                 args.test_case_number)

    elif args.command == 'create_summary_json_satellite_type':
        json_builder.create_summary_json_at_satellite_type_level_from_data_folder(args.root_directory, args.satellite_type,
                                                                     args.verbose)


if __name__ == "__main__":
    main()
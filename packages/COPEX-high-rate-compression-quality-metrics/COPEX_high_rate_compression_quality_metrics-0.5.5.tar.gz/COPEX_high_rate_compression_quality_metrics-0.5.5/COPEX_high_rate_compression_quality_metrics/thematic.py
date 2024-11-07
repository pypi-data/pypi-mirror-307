import importlib.metadata as lib_meta
import os.path
import re

from lpips.pretrained_networks import resnet
from numpy.core.defchararray import decode
from rasterio.enums import Resampling
from skimage import io
from pathlib import Path
# from osgeo import gdal
from sklearn.cluster import KMeans
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import accuracy_score
import numpy as np
import rasterio
from torch._VF import saddmm
from datetime import datetime
from . import utils

# Ensemble des bandes utilisés et pour quelles thematiques
# les programme doivent rechercher le numéro de bande dans le nom et donc chaque bande est en string
# bands needing resampling est un tableau de tuples, ou chaque tuple contiens un tableau de bandes a reechantilloner, et le facteur a utiliser
thematic_usecase_bands = {
    'S1_GRD': {  # Type de donnée S
        'Kmeans++': {  # Thématique Kmeans++
            'valid_band': ['vv', 'vh'],  # Bandes valides pour S et Kmeans++
            'band_prefix': "grd-",
            'bands_needing_resampling': {
                "bands": [],
                "factor": 2
            },
        }
    },
    'S2_L1C': {  # Type de donnée S2
        'Kmeans++': {  # Thématique Kmeans++ pour S2
            'valid_band': ['02', '03', '04', '05', '06', '07', '08', '11', '12'],  # Bandes valides pour S2 et Kmeans++
            'band_prefix': "_B",
            'bands_needing_resampling': {
                "bands": ['05', '06', '07', '11', '12'],
                "factor": 2
            }  # Bandes à rééchantillonner pour S2 et flooding et le facteur a appliquer
        }
    },
    'S2_L2A': {  # Type de donnée S2
        'Kmeans++': {  # Thématique Kmeans++ pour S2
            'valid_band': ['02', '03', '04', '05', '06', '07', '08', '11', '12'],  # Bandes valides pour S2 et Kmeans++
            'band_prefix': "_B",
            'bands_needing_resampling': {
                "bands": ['05', '06', '07', '11', '12'],
                "factor": 2
            }  # Bandes à rééchantillonner pour S2 et flooding et le facteur a appliquer
        }
    }
}


def periodic_sample(image, interval):
    """
       Réalise un échantillonnage périodique sur l'image, prenant un pixel tous les 'interval' pixels.

       Parameters:
           image (numpy array): L'image à échantillonner.
           interval (int): L'intervalle de sélection des pixels.

       Returns:
           numpy array: Une matrice contenant les pixels échantillonnés, aplatie pour K-means.
       """
    # print("Échantillonnage périodique des pixels...")
    # Échantillonnage des pixels à intervalles réguliers.
    sampled_pixels = image[::interval, ::interval, :]
    # print("Échantillonnage terminé.")
    # Reshape pour créer un tableau 2D adapté à K-means.
    return sampled_pixels.reshape(-1, image.shape[2])


def classify_block(block, kmeans):
    """
    Applique le modèle K-means à un bloc d'image pour le classifier.

    Parameters:
        block (numpy array): Le bloc d'image à classifier.
        kmeans (KMeans): Modèle K-means déjà entraîné.

    Returns:
        numpy array: Les labels K-means appliqués au bloc d'image.
    """
    # Reshape du bloc pour correspondre aux dimensions attendues par K-means.
    block_reshaped = block.reshape(-1, block.shape[-1])
    # Prédiction des clusters sur chaque pixel du bloc.
    labels = kmeans.predict(block_reshaped)
    # Reshape les labels pour correspondre à la forme du bloc d'image original.
    return labels.reshape(block.shape[:-1])


def compute_kmeans(image_path, classif_path, centroid_path, sample_interval=10, n_clusters=10, random_state=42):
    """
    Applique l'algorithme K-means à une image pour générer une classification des pixels.

    Parameters:
        image_path (str or Path): Le chemin de l'image à classifier.
        classif_path (str or Path): Le chemin où enregistrer l'image classifiée.
        centroid_path (str or Path): Le chemin du fichier de centroides pour K-means.
        sample_interval (int): L'intervalle d'échantillonnage des pixels pour l'entraînement K-means.
        n_clusters (int): Le nombre de clusters pour K-means.
        random_state (int): La graine aléatoire pour K-means.

    Returns:
        numpy array: L'image classifiée par K-means.
    """

    try:
        # Lecture de l'image avec rasterio (format raster)
        with rasterio.open(image_path) as src:
            image = src.read()
            profile = src.profile.copy()  # Copie des métadonnées associées à l'image.

        # Réorganisation des bandes d'image (canaux) sur le dernier axe.
        image = np.stack(image, axis=-1)
    except:
        # Lecture de l'image en format non-raster avec skimage en cas d'échec de rasterio.
        image = io.imread(image_path)
        image = np.stack([image], axis=-1)

        profile = None  # Aucun profil disponible si skimage est utilisé.

    print(image.shape)  # Affiche la taille de l'image pour vérification.

    # Échantillonnage périodique des pixels pour réduire le nombre de données pour K-means.
    sampled_pixels = periodic_sample(image, sample_interval)

    # Vérification de l'existence d'un fichier de centroides. Si inexistant, il sera créé.
    init_centroid = centroid_path.exists() is False
    centroid = None

    if init_centroid:
        # Initialisation des centroides avec K-means++
        kmeans_init = KMeans(n_clusters=n_clusters, init='k-means++', random_state=random_state)
        kmeans_init.fit(sampled_pixels)  # Entraînement sur les pixels échantillonnés
        centroid = kmeans_init.cluster_centers_  # Récupération des centroides
        # Sauvegarde des centroides pour future réutilisation
        np.savetxt(centroid_path, centroid, delimiter=',')
    else:
        # Chargement des centroides depuis un fichier CSV existant.
        centroid = np.loadtxt(centroid_path, delimiter=',')
        centroid = centroid.reshape(-1, 1)

    # compute kmeans on image
    # Initialisation du K-means avec les centroides
    kmeans = KMeans(n_clusters=n_clusters, init=centroid, random_state=random_state)
    kmeans.fit(sampled_pixels)  # Entraînement du modèle sur les pixels échantillonnés

    # Préparation d'une image vide pour recevoir les labels de classification.
    height, width, _ = image.shape
    classified_image = np.zeros((height, width), dtype=np.uint8)

    # Définir la taille des blocs
    block_size = 512
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            # Définition des limites du bloc
            i_end = min(i + block_size, height)
            j_end = min(j + block_size, width)
            block = image[i:i_end, j:j_end, :]
            # Classification du bloc avec K-means
            block_labels = classify_block(block, kmeans)
            classified_image[i:i_end, j:j_end] = block_labels

    # Sauvegarde de l'image classifiée, avec ou sans profil raster.
    if profile is None:
        io.imsave(classif_path, classified_image)  # Sauvegarde avec skimage

    else:
        profile.update(dtype=rasterio.uint8, compress='lzw')  # Mise à jour du profil raster

        with rasterio.open(classif_path, 'w', **profile) as dst:
            dst.write(classified_image.astype(rasterio.uint8), 1)

    return classified_image


def compute_kmeans_multiband(image, image_ref_path, classif_path, centroid_path, sample_interval=10, n_clusters=10,
                             random_state=42):
    """
    Applique l'algorithme K-means à une image pour générer une classification des pixels.

    Parameters:
        image_path (str or Path): Le chemin de l'image à classifier.
        classif_path (str or Path): Le chemin où enregistrer l'image classifiée.
        centroid_path (str or Path): Le chemin du fichier de centroides pour K-means.
        sample_interval (int): L'intervalle d'échantillonnage des pixels pour l'entraînement K-means.
        n_clusters (int): Le nombre de clusters pour K-means.
        random_state (int): La graine aléatoire pour K-means.

    Returns:
        numpy array: L'image classifiée par K-means.
    """
    print("compute_kmeans_multiband...")
    try:
        # Lecture de l'image avec rasterio (format raster)
        with rasterio.open(image_ref_path) as src:
            profile = src.profile.copy()  # Copie des métadonnées associées à l'image.

        # Réorganisation des bandes d'image (canaux) sur le dernier axe.
    except:
        # Lecture de l'image en format non-raster avec skimage en cas d'échec de rasterio.
        profile = None  # Aucun profil disponible si skimage est utilisé.

    print(image.shape)  # Affiche la taille de l'image pour vérification.

    # Échantillonnage périodique des pixels pour réduire le nombre de données pour K-means.
    sampled_pixels = periodic_sample(image, sample_interval)

    # Vérification de l'existence d'un fichier de centroides. Si inexistant, il sera créé.
    init_centroid = centroid_path.exists() is False
    centroid = None

    if init_centroid:
        # Initialisation des centroides avec K-means++
        print("initialisation des centroid...")
        kmeans_init = KMeans(n_clusters=n_clusters, init='k-means++', random_state=random_state)
        kmeans_init.fit(sampled_pixels)  # Entraînement sur les pixels échantillonnés
        centroid = kmeans_init.cluster_centers_  # Récupération des centroides
        # Sauvegarde des centroides pour future réutilisation
        np.savetxt(centroid_path, centroid, delimiter=',')
    else:
        print("chargement des centroid...")
        # Chargement des centroides depuis un fichier CSV existant.
        centroid = np.loadtxt(centroid_path, delimiter=',')
        # print("reshaping centroids = ",centroid)
        # centroid = centroid.reshape(-1, 1)
        # print("centroids reshaped = ",centroid)

    # compute kmeans on image
    # Initialisation du K-means avec les centroides
    kmeans = KMeans(n_clusters=n_clusters, init=centroid, random_state=random_state)
    kmeans.fit(sampled_pixels)  # Entraînement du modèle sur les pixels échantillonnés

    # Préparation d'une image vide pour recevoir les labels de classification.
    height, width, _ = image.shape
    classified_image = np.zeros((height, width), dtype=np.uint8)

    # Définir la taille des blocs
    block_size = 512
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            # Définition des limites du bloc
            i_end = min(i + block_size, height)
            j_end = min(j + block_size, width)
            block = image[i:i_end, j:j_end, :]
            # Classification du bloc avec K-means
            block_labels = classify_block(block, kmeans)
            classified_image[i:i_end, j:j_end] = block_labels

    # Sauvegarde de l'image classifiée, avec ou sans profil raster.
    if profile is None:
        io.imsave(classif_path, classified_image)  # Sauvegarde avec skimage

    else:
        profile.update(dtype=rasterio.uint8, compress='lzw')  # Mise à jour du profil raster

        with rasterio.open(classif_path, 'w', **profile) as dst:
            dst.write(classified_image.astype(rasterio.uint8), 1)

    return classified_image


def get_classification_path(image_path, sample_interval, n_clusters, random_state):
    """
    Génère le chemin d'accès pour l'image classifiée.

    Parameters:
        image_path (Path): Le chemin de l'image d'entrée.
        sample_interval (int): L'intervalle d'échantillonnage des pixels.
        n_clusters (int): Le nombre de clusters pour K-means.
        random_state (int): La graine aléatoire.

    Returns:
        Path: Le chemin d'accès de l'image classifiée.
    """
    return Path(os.path.join(image_path.parent, "thematic",
                             image_path.stem + ".kmeans++-" + str(sample_interval) + "-" + str(n_clusters) + "-" + str(
                                 random_state) + ".tif"))


def get_classification_path_multiband(folder_path, sample_interval, n_clusters, random_state, return_number=-2):
    """
    Génère le chemin d'accès pour l'image classifiée.

    Parameters:
        folder_path (Path): Le chemin du dossier d'entrée.
        sample_interval (int): L'intervalle d'échantillonnage des pixels.
        n_clusters (int): Le nombre de clusters pour K-means.
        random_state (int): La graine aléatoire.

    Returns:
        Path: Le chemin d'accès de l'image classifiée.
    """
    classif_output_name = (
            str(utils.get_product_name_from_final_folder_path(folder_path, return_number)[1]) + ".kmeans++-" +
            str(sample_interval) + "-" + str(n_clusters) + "-" + str(random_state) + ".tif")

    return Path(os.path.join(folder_path, "thematic", classif_output_name))


def get_centroid_path(image_path, sample_interval, n_clusters, random_state):
    """
       Génère le chemin d'accès pour le fichier de centroides.

       Parameters:
           image_path (Path): Le chemin de l'image d'entrée.
           sample_interval (int): L'intervalle d'échantillonnage des pixels.
           n_clusters (int): Le nombre de clusters pour K-means.
           random_state (int): La graine aléatoire.

       Returns:
           Path: Le chemin d'accès du fichier de centroides.
       """
    return Path(os.path.join(image_path.parent, "thematic",
                             image_path.stem + ".kmeans++-" + str(sample_interval) + "-" + str(
                                 n_clusters) + "-" + str(random_state) + "-centroid.csv"))


def get_centroid_path_multiband(folder_path, product_name, sample_interval, n_clusters, random_state, valid_bands=None,
                                resampled_bands=None, compression_factor=None):
    """
       Génère le chemin d'accès pour le fichier de centroides.

       Parameters:
           folder_path (Path): Le chemin du dossier original.
           product_name(str):nom du produit sur lequel on travail
           sample_interval (int): L'intervalle d'échantillonnage des pixels.
           n_clusters (int): Le nombre de clusters pour K-means.
           random_state (int): La graine aléatoire.

       Returns:
           Path: Le chemin d'accès du fichier de centroides.
    """

    """str_bands = "B_"
    for band in valid_bands:
        str_bands= str_bands+str(band)+"_"
        
    if resampled_bands is not None:
        str_bands = str_bands+"_resampled_f"+str(compression_factor)+"_B_"
        for elem in resampled_bands:
            str_bands = str_bands + str(elem) + "_"""

    final_csv_name = str(product_name) + ".kmeans++-" + str(sample_interval) + "-" + str(
        n_clusters) + "-" + str(random_state) + "-centroid.csv"

    return Path(os.path.join(folder_path, "thematic", final_csv_name))


def compute_kmeans_score(image1_path, image2_path, sample_interval=10, n_clusters=30, random_state=42):
    """
        Calcule la similarité entre deux images classifiées avec K-means via l'accuracy et le coefficient de kappa.

        Parameters:
            image1_path (str or Path): Chemin de la première image.
            image2_path (str or Path): Chemin de la deuxième image (décompressée).
            sample_interval (int): L'intervalle d'échantillonnage des pixels.
            n_clusters (int): Le nombre de clusters pour K-means.
            random_state (int): La graine aléatoire.

        Returns:
            str: Nom du modèle K-means avec les paramètres utilisés.
            dict: Résultats des métriques (accuracy et kappa).
    """
    image_path = Path(image1_path)
    decompressed_path = Path(image2_path)

    # Obtention des chemins pour les centroides et les classifications
    centroid_path = get_centroid_path(image_path, sample_interval, n_clusters, random_state)

    # Crée le répertoire pour les fichiers de centroides si inexistant.
    if centroid_path.parent.exists() is False:
        centroid_path.parent.mkdir()

    # Génère le chemin pour sauvegarder ou lire l'image classifiée.
    image_classif_path = get_classification_path(image_path, sample_interval, n_clusters, random_state)

    # Crée le répertoire pour les images classifiées si inexistant.
    if image_classif_path.parent.exists() is False:
        image_classif_path.parent.mkdir()

    # Si le fichier classifié n'existe pas, génère l'image classifiée avec K-means.
    if image_classif_path.exists() is False:
        image_classif = compute_kmeans(image_path, image_classif_path, centroid_path, n_clusters=n_clusters,
                                       sample_interval=sample_interval, random_state=random_state)
    else:
        # Charge l'image déjà classifiée.
        image_classif = io.imread(image_classif_path)

    # Même processus pour la deuxième image.
    decompressed_classif_path = get_classification_path(decompressed_path, sample_interval, n_clusters, random_state)

    if decompressed_classif_path.parent.exists() is False:
        decompressed_classif_path.parent.mkdir()

    if decompressed_classif_path.exists() is False:
        decompressed_classif = compute_kmeans(decompressed_path, decompressed_classif_path, centroid_path,
                                              n_clusters=n_clusters, sample_interval=sample_interval,
                                              random_state=random_state)
    else:
        decompressed_classif = io.imread(decompressed_classif_path)

    # print(image_classif, decompressed_classif)

    # Calcule les métriques de similarité entre les deux images classifiées (accuracy et kappa).
    accuracy = accuracy_score(image_classif.flatten(), decompressed_classif.flatten())
    kappa = cohen_kappa_score(image_classif.flatten(), decompressed_classif.flatten())

    # Récupère le nom du fichier d'entrée pour affichage.
    image_1_name = os.path.basename(image1_path)

    # Organise les résultats dans un dictionnaire pour reporting.
    data = {
        "library": "scikit-learn",
        "version": lib_meta.version("scikit-learn"),
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "metrics": {
            "overall_accuracy": {
                "results": {
                    image_1_name: accuracy
                }
            },
            "kappa_coefficient": {
                "results": {
                    image_1_name: kappa
                }
            }
        }
    }

    # Retourne le nom du modèle K-means et les métriques de similarité.
    return "kmeans++-" + str(sample_interval) + "-" + str(n_clusters) + "-" + str(random_state), data


def get_first_valid_band_path(directory, valid_bands):
    band_regex = re.compile(r'_B(\d{2}).*\.tif$', re.IGNORECASE)
    for filename in os.listdir(directory):
        match = band_regex.search(filename)
        if match:
            band_num = match.group(1)
            if band_num in valid_bands:
                return os.path.join(directory, filename)
    return None


def load_multispectral_images(directory, valid_bands, resample_bands, resample_factor, band_prefix,
                              resampling_method=Resampling.bilinear, verbose = False):
    """
    Fonction pour charger des images multispectrales avec rééchantillonnage des bandes à 20 mètres.

    Args:
        directory (str): Le chemin du dossier contenant les images TIF.

    Returns:
        image (np.ndarray): Tableau numpy avec les bandes empilées.
        geo_transform (affine.Affine): Transformation géospatiale des images.
        projection (str): Projection des images.
        base_filename (str): Nom de base des fichiers d'image.
    """

    # print("Chargement des images multispectrales avec rééchantillonnage...")

    # Regex pour extraire le numéro de bande
    band_regex = re.compile(band_prefix + r'(\w{2}).*\.tiff?$', re.IGNORECASE)
    if verbose : print("band_regex = ", band_regex)
    # Définir les bandes valides et celles à rééchantillonner

    # Dossier pour stocker les images rééchantillonnées
    resampled_dir = os.path.join(directory, 'resampled')
    if not os.path.exists(resampled_dir):
        os.makedirs(resampled_dir)

    bands = {}
    base_filename = None
    geo_transform = None
    projection = None
    i = 0
    # Parcourir tous les fichiers du dossier
    for filename in os.listdir(directory):
        match = band_regex.search(filename)
        #print("match = ", match)
        if match:
            i += 1
            band_num = match.group(1)
            if band_num in valid_bands:
                file_path = os.path.join(directory, filename)

                # Rééchantillonner les bandes à 20 mètres
                if band_num in resample_bands:
                    resampled_path = os.path.join(resampled_dir, filename)
                    if not os.path.exists(resampled_path):
                        utils.resample_band(file_path, resampled_path, resample_factor, resampling_method)
                    file_path = resampled_path

                # print(f"Lecture de {filename}...")

                # Utiliser Rasterio pour ouvrir le fichier
                with rasterio.open(file_path) as dataset:
                    band_data = dataset.read(1)  # Lire la première bande
                    if geo_transform is None:
                        geo_transform = dataset.transform
                        projection = dataset.crs

                # Stocker la bande
                bands[i] = band_data

                # Définir le base_filename si ce n'est pas encore fait
                if base_filename is None:
                    base_filename = filename.replace(match.group(0), '')

    # Vérifier que toutes les bandes sont présentes et trier par numéro de bande
    if not bands:
        raise ValueError("Aucune bande valide trouvée dans le dossier.")

    # Trier les bandes et empiler dans un tableau numpy
    sorted_bands = [bands[key] for key in sorted(bands.keys())]
    image = np.stack(sorted_bands, axis=-1)

    # print("Images multispectrales chargées.")
    return image, geo_transform, projection, base_filename


def compute_kmeans_score_for_multiband(original_folder_path, decompressed_folder_path, satellite_type: str,
                                       sample_interval=10, n_clusters=10, random_state=42,
                                       resampling_method=Resampling.bilinear):
    """
        Calcule la similarité entre deux images classifiées avec K-means via l'accuracy et le coefficient de kappa.

        Parameters:
            original_folder_path (str or Path): Chemin du premier dossier.
            decompressed_folder_path (str or Path): Chemin du deuxieme dossier.
            sample_interval (int): L'intervalle d'échantillonnage des pixels.
            n_clusters (int): Le nombre de clusters pour K-means.
            random_state (int): La graine aléatoire.

        Returns:
            str: Nom du modèle K-means avec les paramètres utilisés.
            dict: Résultats des métriques (accuracy et kappa).
    """
    # récupération des bandes valides
    valid_bands = thematic_usecase_bands[satellite_type]['Kmeans++']['valid_band']
    resample_bands = thematic_usecase_bands[satellite_type]['Kmeans++']['bands_needing_resampling']["bands"]
    resample_factor = thematic_usecase_bands[satellite_type]['Kmeans++']['bands_needing_resampling']["factor"]
    band_prefix = thematic_usecase_bands[satellite_type]['Kmeans++']["band_prefix"]

    ref_band_path = get_first_valid_band_path(original_folder_path, valid_bands)

    # print("ref band = ", ref_band_path)
    # print("computing kmeans++ for ", satellite_type, " in folder ", original_folder_path)
    # print("valid_bands : ", valid_bands)
    # print("resample_bands : ", resample_bands)
    # print("resample_factor : ", resample_factor)

    image_original, geo_transform, projection, base_filename = load_multispectral_images(directory=original_folder_path,
                                                                                         valid_bands=valid_bands,
                                                                                         resample_bands=resample_bands,
                                                                                         resample_factor=resample_factor,
                                                                                         band_prefix=band_prefix,
                                                                                         resampling_method=resampling_method)

    # Obtention des chemins pour les centroides et les classifications
    centroid_path = get_centroid_path_multiband(original_folder_path,
                                                utils.get_product_name_from_final_folder_path(original_folder_path)[1],
                                                sample_interval, n_clusters, random_state)
    # print("centroid path = ", centroid_path)

    # Crée le répertoire pour les fichiers de centroides si inexistant.
    if centroid_path.parent.exists() is False:
        centroid_path.parent.mkdir()

    # Génère le chemin pour sauvegarder ou lire l'image classifiée.
    image_classif_path = get_classification_path_multiband(original_folder_path, sample_interval, n_clusters,
                                                           random_state)

    # Crée le répertoire pour les images classifiées si inexistant.
    if image_classif_path.parent.exists() is False:
        image_classif_path.parent.mkdir()

    # Si le fichier classifié n'existe pas, génère l'image classifiée avec K-means.
    if image_classif_path.exists() is False:
        image_classif = compute_kmeans_multiband(image=image_original, image_ref_path=ref_band_path,
                                                 classif_path=image_classif_path,
                                                 centroid_path=centroid_path, n_clusters=n_clusters,
                                                 sample_interval=sample_interval, random_state=random_state)
    else:
        # Charge l'image déjà classifiée.
        print("image deja classifiée dans ", image_classif_path, "..., lecture directe")
        image_classif = io.imread(image_classif_path)

    # Même processus pour la deuxième image.

    image_decompressed, _, _, _ = load_multispectral_images(directory=decompressed_folder_path,
                                                            valid_bands=valid_bands,
                                                            resample_bands=resample_bands,
                                                            band_prefix=band_prefix,
                                                            resample_factor=resample_factor)

    # print("decompressed_folder_path", decompressed_folder_path)
    decompressed_classif_path = get_classification_path_multiband(decompressed_folder_path, sample_interval, n_clusters,
                                                                  random_state, return_number=-3)
    # print("decompressed_classif_path = ", decompressed_classif_path)

    if decompressed_classif_path.parent.exists() is False:
        decompressed_classif_path.parent.mkdir()

    if decompressed_classif_path.exists() is False:
        decompressed_classif = compute_kmeans_multiband(image=image_decompressed, image_ref_path=ref_band_path,
                                                        classif_path=decompressed_classif_path,
                                                        centroid_path=centroid_path, n_clusters=n_clusters,
                                                        sample_interval=sample_interval, random_state=random_state)
    else:
        decompressed_classif = io.imread(decompressed_classif_path)

    # print(image_classif, decompressed_classif)

    # Calcule les métriques de similarité entre les deux images classifiées (accuracy et kappa).
    accuracy = accuracy_score(image_classif.flatten(), decompressed_classif.flatten())
    kappa = cohen_kappa_score(image_classif.flatten(), decompressed_classif.flatten())

    # Récupère le nom du fichier d'entrée pour affichage.
    image_name = os.path.basename(decompressed_classif_path)

    # Organise les résultats dans un dictionnaire pour reporting.
    data = {
        "kmeans++" + "-" + str(sample_interval) + "-" + str(n_clusters) + "-" + str(
            random_state): {
            "library": "scikit-learn",
            "version": lib_meta.version("scikit-learn"),
            "COPEX high compression library version": utils.get_lib_version(),
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "original bands": valid_bands,
            "resampled bands": resample_bands,
            "resampled bands factor": resample_factor,
            "resampling method": resampling_method.name,
            "centroids": str(np.loadtxt(centroid_path, delimiter=',')),
            "metrics": {
                "overall_accuracy": {
                    "results": {
                        str(image_name): accuracy
                    }
                },
                "kappa_coefficient": {
                    "results": {
                        str(image_name): kappa
                    }
                }
            }
        }
    }

    # Retourne le nom du modèle K-means et les métriques de similarité.
    return "thematics", data

import os
import numpy as np
import matplotlib.pyplot as plt
from osgeo import gdal
from sklearn.cluster import KMeans
import re


def resample_band(input_path, output_path, scale_factor=2, resample_alg=gdal.GRA_Bilinear):
    """
    Rechantillonne une bande d'image à une résolution plus fine.

    :param input_path: Chemin du fichier TIFF d'entrée.
    :param output_path: Chemin du fichier TIFF de sortie.
    :param scale_factor: Facteur de rééchantillonnage (0.5 pour réduire de moitié la taille des pixels).
    :param resample_alg: Algorithme de rééchantillonnage (gdal.GRA_Bilinear pour bilinéaire).
    """
    dataset = gdal.Open(input_path)
    if not dataset:
        raise FileNotFoundError(f"Le fichier {input_path} est introuvable ou ne peut être ouvert.")

    width = int(dataset.RasterXSize * scale_factor)
    height = int(dataset.RasterYSize * scale_factor)
    driver = gdal.GetDriverByName('GTiff')

    output_dataset = driver.Create(output_path, width, height, 1, dataset.GetRasterBand(1).DataType)
    output_dataset.SetGeoTransform([
        dataset.GetGeoTransform()[0],
        dataset.GetGeoTransform()[1] * (1 / scale_factor),
        dataset.GetGeoTransform()[2],
        dataset.GetGeoTransform()[3],
        dataset.GetGeoTransform()[4],
        dataset.GetGeoTransform()[5] * (1 / scale_factor)
    ])
    output_dataset.SetProjection(dataset.GetProjection())

    gdal.ReprojectImage(dataset, output_dataset, None, None, resample_alg)
    output_dataset.FlushCache()
    output_dataset = None
    dataset = None
    print(f"{input_path} rechantillonné et sauvegardé sous {output_path}")


def load_multispectral_images(directory, verbose = False):
    print("Chargement des images multispectrales avec rechantillonnage...")
    # Regex pour extraire le numéro de bande et le type de bande à utiliser
    band_regex = re.compile(r'_B(\d{2}).*\.tif$', re.IGNORECASE)
    valid_bands = {'02', '03', '04', '05', '06', '07', '08', '11', '12'} # bandes a 10 metres
    resample_bands = {'05', '06', '07', '11', '12'} # bandes a 20 metres qu'on resample avec un facteur 2
    resampled_dir = os.path.join(directory, 'resampled')

    if not os.path.exists(resampled_dir):
        os.makedirs(resampled_dir)

    bands = {}
    base_filename = None

    # Parcourir tous les fichiers du dossier
    for filename in os.listdir(directory):
        match = band_regex.search(filename)
        if match:
            band_num = match.group(1)
            if band_num in valid_bands:
                file_path = os.path.join(directory, filename)

                if band_num in resample_bands:
                    resampled_path = os.path.join(resampled_dir, filename)
                    resample_band(file_path, resampled_path)
                    file_path = resampled_path

                print(f"Lecture de {filename}...")
                dataset = gdal.Open(file_path)
                if dataset is None:
                    if verbose : print(f"Warning: Failed to open {file_path}")
                    continue

                band_data = dataset.ReadAsArray()

                bands[int(band_num)] = band_data
                if 'geo_transform' not in locals():
                    geo_transform = dataset.GetGeoTransform()
                    projection = dataset.GetProjection()
                dataset = None  # Fermer le fichier

                # Définir le base_filename si ce n'est pas encore fait
                if base_filename is None:
                    base_filename = filename.replace(match.group(0), '')

    # Vérifier que toutes les bandes sont présentes et trier par numéro de bande
    if not bands:
        raise ValueError("No valid bands found in the directory")

    sorted_bands = [bands[key] for key in sorted(bands.keys())]

    # Convertir la liste de bandes en un tableau numpy
    image = np.stack(sorted_bands, axis=-1)

    print("Images multispectrales chargées.")
    return image, geo_transform, projection, base_filename


def periodic_sample(image, interval):
    print("Échantillonnage périodique des pixels...")
    sampled_pixels = image[::interval, ::interval, :]
    print("Échantillonnage terminé.")
    return sampled_pixels.reshape(-1, image.shape[2])


def classify_block(block, kmeans):
    block_reshaped = block.reshape(-1, block.shape[-1])
    labels = kmeans.predict(block_reshaped)
    return labels.reshape(block.shape[:-1])


def kmeans(directory_path, n_clusters=5, random_state=42, sample_interval=10, n_jobs=-1):
    # Charger les images multispectrales à partir du dossier avec rechantillonnage
    image, geo_transform, projection, base_filename = load_multispectral_images(directory_path)

    # Appliquer l'échantillonnage périodique pour réduire la taille des données
    sampled_pixels = periodic_sample(image, sample_interval)

    # Initialisation des centroides avec K-means++
    kmeans_init = KMeans(n_clusters=n_clusters, init='k-means++', random_state=random_state, n_init=1)
    kmeans_init.fit(sampled_pixels)

    # Export des centroides initiaux
    initial_centroids = kmeans_init.cluster_centers_
    initial_centroids_filename = os.path.join(directory_path, f"initial_centroids_nc{n_clusters}.csv")
    np.savetxt(initial_centroids_filename, initial_centroids, delimiter=',')
    print(f"Centroides initiaux sauvegardés dans {initial_centroids_filename}")

    # Entraînement du modèle K-means avec les centroides initiaux
    print("Entraînement du modèle K-means avec les centroides initiaux...")
    kmeans = KMeans(n_clusters=n_clusters, init=initial_centroids, n_init=1, random_state=random_state, n_jobs=n_jobs)
    kmeans.fit(sampled_pixels)
    print("Modèle K-means entraîné.")

    # Export des centroides finaux
    final_centroids = kmeans.cluster_centers_
    final_centroids_filename = os.path.join(directory_path, f"final_centroids_nc{n_clusters}.csv")
    np.savetxt(final_centroids_filename, final_centroids, delimiter=',')
    print(f"Centroides finaux sauvegardés dans {final_centroids_filename}")

    # Assigner les labels aux pixels d'origine
    height, width, _ = image.shape
    classified_image = np.zeros((height, width), dtype=np.uint8)
    print("Classification des pixels d'origine...")

    # Définir la taille des blocs
    block_size = 512
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            i_end = min(i + block_size, height)
            j_end = min(j + block_size, width)
            block = image[i:i_end, j:j_end, :]
            block_labels = classify_block(block, kmeans)
            classified_image[i:i_end, j:j_end] = block_labels

    print("Classification terminée.")

    # Afficher les résultats
    print("Affichage des résultats...")
    plt.imshow(classified_image, cmap='viridis')
    plt.colorbar()
    plt.title('Classification K-means++')
    # plt.show()

    # Définir le nom du fichier de sortie avec les paramètres
    output_filename = f"{base_filename}_kmeans_nc{n_clusters}_si{sample_interval}_rs{random_state}.tif"
    output_path = os.path.join(directory_path, output_filename)

    # Sauvegarder l'image classifiée en GeoTIFF
    print("Sauvegarde de l'image classifiée...")
    driver = gdal.GetDriverByName('GTiff')
    out_dataset = driver.Create(output_path, width, height, 1, gdal.GDT_Byte)
    out_dataset.SetGeoTransform(geo_transform)
    out_dataset.SetProjection(projection)
    out_band = out_dataset.GetRasterBand(1)
    out_band.WriteArray(classified_image)
    out_band.FlushCache()
    out_dataset = None  # Sauvegarder et fermer le fichier
    print("Image classifiée sauvegardée.")

    return output_path, initial_centroids_filename, final_centroids_filename


def kmeans_compressed(directory_path, initial_centroids_file, n_clusters=5, random_state=42, sample_interval=10,
                      n_jobs=-1):
    # Charger les images multispectrales compressées-décompressées
    image, geo_transform, projection, base_filename = load_multispectral_images(directory_path)

    # Appliquer l'échantillonnage périodique pour réduire la taille des données
    sampled_pixels = periodic_sample(image, sample_interval)

    # Charger les centroides initiaux depuis le fichier CSV
    initial_centroids = np.loadtxt(initial_centroids_file, delimiter=',')
    print(f"Centroides initiaux chargés depuis {initial_centroids_file}")

    # Appliquer K-means++ avec les centroides initiaux
    print("Classification avec K-means en utilisant les centroides initiaux...")
    kmeans = KMeans(n_clusters=n_clusters, init=initial_centroids, n_init=1, random_state=random_state, n_jobs=n_jobs)
    kmeans.fit(sampled_pixels)
    print("Classification K-means terminée.")

    # Assigner les labels aux pixels d'origine
    height, width, _ = image.shape
    classified_image = np.zeros((height, width), dtype=np.uint8)
    print("Attribution des labels aux pixels...")

    # Définir la taille des blocs
    block_size = 512
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            i_end = min(i + block_size, height)
            j_end = min(j + block_size, width)
            block = image[i:i_end, j:j_end, :]
            block_labels = classify_block(block, kmeans)
            classified_image[i:i_end, j:j_end] = block_labels

    print("Attribution des labels terminée.")

    # Afficher les résultats
    print("Affichage des résultats...")
    plt.imshow(classified_image, cmap='viridis')
    plt.colorbar()
    plt.title('Classification K-means++ sur image compressée-décompressée')
    # plt.show()

    # Définir le nom du fichier de sortie avec les paramètres
    output_filename = f"{base_filename}_kmeans_compressed_nc{n_clusters}_si{sample_interval}_rs{random_state}.tif"
    output_path = os.path.join(directory_path, output_filename)

    # Sauvegarder l'image classifiée en GeoTIFF
    print("Sauvegarde de l'image classifiée...")
    driver = gdal.GetDriverByName('GTiff')
    out_dataset = driver.Create(output_path, width, height, 1, gdal.GDT_Byte)
    out_dataset.SetGeoTransform(geo_transform)
    out_dataset.SetProjection(projection)
    out_band = out_dataset.GetRasterBand(1)
    out_band.WriteArray(classified_image)
    out_band.FlushCache()
    out_dataset = None  # Sauvegarder et fermer le fichier
    print(f"Image classifiée sauvegardée sous {output_path}")

    return output_path


origin_directory_path       = 'E:/BACKUP_VT/VisioTerra/technique/P355_AGRECO_UE_CARTOGRAPHIE_ENVIRONNEMENTALE/data/Martial_wologizi_Mt-Nimba_stage/Mont_Nimba/data/__COPEX_Zhour_2024/original/'

compressed_directory_path   = 'E:/BACKUP_VT/VisioTerra/technique/P355_AGRECO_UE_CARTOGRAPHIE_ENVIRONNEMENTALE/data/Martial_wologizi_Mt-Nimba_stage/Mont_Nimba/data/__COPEX_Zhour_2024/decompressed/[01-01-001_JJ2000_x50]_[23696692]_[102]_[172]/'

n_clusters = 40        # Le nombre de clusters pour K-means.
                       # Cela représente le nombre de groupes ou "classes" que l'on souhaite créer à partir des données.
                       # Chaque pixel de l'image sera attribué à l'un de ces clusters en fonction de sa similarité avec les autres.
                       # Un nombre plus élevé de clusters peut capturer plus de détails dans l'image, mais peut aussi entraîner
                       # une sur-segmentation, tandis qu'un nombre trop faible peut ne pas capturer toute la variabilité de l'image.

random_state = 42      # Le paramètre permettant de garantir la reproductibilité des résultats.
                       # Ce paramètre fixe la graine du générateur aléatoire utilisé pour l'initialisation des centroides.
                       # En spécifiant un 'random_state', on s'assure que le même ensemble de centroides initiaux
                       # est utilisé chaque fois que l'on exécute l'algorithme, ce qui permet d'obtenir les mêmes
                       # résultats à chaque exécution, facilitant ainsi la comparaison entre différentes exécutions.

sample_interval = 100   # Intervalle d'échantillonnage pour réduire le nombre de pixels à traiter.
                       # Ce paramètre contrôle la fréquence à laquelle les pixels sont échantillonnés dans l'image.
                       # Un intervalle de 10 signifie que seulement un pixel sur 10 sera utilisé pour l'entraînement
                       # du modèle K-means. Cela réduit considérablement la quantité de données à traiter,
                       # ce qui accélère l'exécution de l'algorithme tout en maintenant une représentation suffisante
                       # des données. Cela est particulièrement utile pour les images de grande taille.

n_jobs = -1            # Nombre de cœurs CPU à utiliser pour l'exécution parallèle.
                       # Ce paramètre détermine combien de processeurs seront utilisés pour exécuter le K-means en parallèle.
                       # -1 signifie que tous les cœurs disponibles sur la machine seront utilisés, maximisant ainsi
                       # la vitesse de traitement. Si on souhaite limiter l'utilisation des ressources ou si on travaille
                       # dans un environnement partagé, on peut définir ce paramètre à un nombre spécifique
                       # pour utiliser un nombre réduit de cœurs.


# Classification de l'image d'origine
output_file, initial_centroids_filename, final_centroids_filename = kmeans(origin_directory_path, n_clusters=n_clusters, random_state=random_state, sample_interval=sample_interval, n_jobs=n_jobs)
print(f"Classified image saved to {output_file}")

#initial_centroids_filename= 'E:/BACKUP_VT/VisioTerra/technique/P355_AGRECO_UE_CARTOGRAPHIE_ENVIRONNEMENTALE/data/Martial_wologizi_Mt-Nimba_stage/Mont_Nimba/data/__COPEX_Zhour_2024/original/initial_centroids_nc20.csv'
# classification de l'image compressée décompressée avec initiatilisation des centroides
#initial_centroids_filename = 'D:/L1C_T29NNJ_A023786_20200111T110827/IMG_DATA/initial_centroids_nc13.csv'
output_file_compressed = kmeans_compressed(compressed_directory_path,
                                           initial_centroids_filename , n_clusters=n_clusters, random_state=random_state, sample_interval=sample_interval, n_jobs=n_jobs)
print(f"Classified compressed image saved to {output_file_compressed}")


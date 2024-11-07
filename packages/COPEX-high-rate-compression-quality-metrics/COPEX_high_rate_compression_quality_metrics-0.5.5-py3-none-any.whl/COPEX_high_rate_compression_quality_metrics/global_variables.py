import os.path

lib_version = "0.5.5"

compressed_folder_name = "compressed"
decompressed_folder_name = "decompressed"
original_folder_name = "original"
algorithm_colors = {
    "JJ2000": "green",
    "HiFiC": "green",
    # Ajoute d'autres algorithmes et leurs couleurs ici
}
thematics_dictionary = {

}
metrics_dictionary = {
    "LPIPS": {
        "min": 0,
        "max": 1
    },
    "SSIM": {
        "min": 0.995,
        "max": 1
    },
    "RMSE": {
        "min": 0,
        "max": 650
        # Pourquoi 650 ? , avec 40db comme valeure d'appuis on a :
        # PSNR = 20.log10(MAX) - 10.log10(MSE)
        # 5,6329598612473982468396446311838 = log10(MSE)
        # MSE = 429519
        # RMSE = 655,3769
    },
    "PSNR": {
        "min": 40,
        "max": 100
    }
}
metrics_all_bands_dictionary = {
    "average",
    "stdev"
}
data_range_for_compression = {
    "min": 0,
    "max": 1000
}
bands_per_satellite_type = {
    "S2_L1C": {
        1: "B01",
        2: "B02",
        3: "B03",
        4: "B04",
        5: "B05",
        6: "B06",
        7: "B07",
        8: "B08",
        9: "B09",
        10: "B10",
        11: "B11",
        12: "B12",
        13: "B8A"
    },
    "S1_GRD": {
        1: "VV",
        2: "VH",
    }

}
summary_output_folder_name = "summary"
summary_output_csv_folder_name = "csv"
summary_output_per_band_folder_name = "per_band"
summary_output_all_bands_folder_name = "all_bands"
summary_output_group_of_bands_folder_name = "group_of_bands"
summary_output_png_folder_name = "png"
dataset_summary_parameter = "dataset_summary"
use_case_summary_parameter = "use_case_summary"
script_directory = os.path.dirname(
    os.path.abspath(__file__))  # le model se trouvera toujours dans un dossier sous lpips_model
lpips_model_path = os.path.join(script_directory, "lpips_model", "alex.pth")

# Vérifiez si le fichier existe à ce chemin
if not os.path.exists(lpips_model_path):
    print(f"Le modèle LPIPS n'a pas été trouvé à l'emplacement suivant : {lpips_model_path}")


import importlib.metadata as lib_meta
import math
import os.path
from typing import Dict, Any
import importlib_metadata  # Pour obtenir des informations sur les packages installés
import numpy as np
import rasterio
from skimage import io
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import mean_squared_error
import lpips
import torch
import random
from datetime import datetime

from . import utils, global_variables


def initialize_LPIPS() -> lpips.LPIPS:
    """
    Initializes and returns an LPIPS model using the AlexNet architecture.

    LPIPS (Learned Perceptual Image Patch Similarity) is a perceptual metric
    used to evaluate the similarity between two images. The 'net' parameter
    specifies the neural network architecture to use, in this case, 'alex'
    refers to AlexNet.

    Returns:
        lpips.LPIPS: An instance of the LPIPS model initialized with AlexNet.
    """

    # Initialize the LPIPS model with the 'alex' network (AlexNet).
    lpips_model = lpips.LPIPS(net='alex', verbose=False,
                              model_path=os.path.join(global_variables.lpips_model_path))

    # Return the initialized LPIPS model.
    return lpips_model


def get_tiff_dimensions(folder_path: str) -> dict:
    """
    Parcourt un dossier pour trouver tous les fichiers .tif/.tiff,
    récupère la largeur et la hauteur de chaque fichier, et construit un dictionnaire.

    Args:
        folder_path (str): Chemin vers le dossier contenant les fichiers TIFF.

    Returns:
        dict: Dictionnaire contenant les dimensions de chaque fichier TIFF sous la forme
        {"bande_name": {"width": width, "height": height}}.
    """
    tiff_dimensions = {}

    # Liste tous les fichiers du dossier et filtre ceux qui se terminent par .tif ou .tiff
    for file_name in utils.list_tiff_files(folder_path):
        print("file_name = ", file_name)
        file_path = os.path.join(folder_path, file_name)

        # Ouvre le fichier TIFF avec rasterio
        with rasterio.open(file_path) as src:
            width = src.width
            height = src.height

            # Ajoute les dimensions au dictionnaire avec le nom du fichier sans extension
            band_name = os.path.splitext(file_name)[0]
            tiff_dimensions[band_name] = {"width": width, "height": height}

    return tiff_dimensions


def preprocess_image(image: np.ndarray, verbose=False) -> np.ndarray:
    """
    Preprocess an image for use with the LPIPS model.

    This function normalizes the pixel values of the input image to the range
    [-1, 1], which is required for the LPIPS model.

    Args:
        image (np.ndarray): The input image as a NumPy array.

    Returns:
        np.ndarray: The preprocessed image with pixel values normalized
                    to the range [-1, 1].
    """
    # Convert the image to float32 for precision in further calculations
    image = image.astype(np.float32)
    if verbose:
        print("min = ", image.min())
        print("max = ", image.max())

    # Normalize the image to the range [0, 1], but if min and max = 0, then the image is full of background
    if (np.max(image) - np.min(image)) == 0:
        return image * 2 - 1
    image = (image - np.min(image)) / (np.max(image) - np.min(image))

    # Scale the image to the range [-1, 1], as required by the LPIPS model
    image = image * 2 - 1

    return image


def convert_to_rgb(image: np.ndarray, verbose=False) -> np.ndarray:
    """
    Convert an image to a 3-channel RGB format if necessary.

    This function ensures that the input image has three channels (RGB). If the image
    is grayscale (2D), it is repeated across three channels. If the image has more
    than three channels, only the first three are retained.

    Args:
        image (np.ndarray): The input image as a NumPy array. It can be grayscale
                            (2D) or have multiple channels (3D).

    Returns:
        np.ndarray: The converted RGB image with three channels.

    Raises:
        ValueError: If the input image does not have 2 or 3 dimensions.
    """
    if verbose: print("convert_to_rgb...")

    if image.ndim == 2:
        # print("Grayscale image detected, converting to 3 channels (RGB)...")
        # Image is grayscale (2D), so we repeat the single channel three times to create an RGB image
        image_rgb = np.repeat(image[:, :, np.newaxis], 3, axis=2)

    elif image.ndim == 3:
        n_bands = image.shape[2]
        if n_bands == 3:
            # If the image already has 3 channels, no conversion is needed
            image_rgb = image
        elif n_bands == 1:
            # If the image has a single channel, repeat it across three channels to create an RGB image
            image_rgb = np.repeat(image, 3, axis=2)
        else:
            # If the image has more than 3 channels, take only the first three
            if n_bands < 3:
                # Special case where there are fewer than 3 channels, repeat them to create 3 channels
                image_rgb = np.repeat(image, 3, axis=2)
            else:
                # Use only the first three channels to create an RGB image
                image_rgb = image[:, :, :3]

    else:
        raise ValueError("The input image must have ndim = 2 or 3 .")

    return image_rgb


def calculate_rmse(image1: np.ndarray, image2: np.ndarray) -> float:
    """
    Calculate the Root Mean Square Error (RMSE) between two multi-band images.

    RMSE is a standard metric used to measure the difference between two images.
    It is particularly useful for comparing image quality, where lower values indicate
    greater similarity.

    Args:
        image1 (np.ndarray): The first image as a NumPy array.
        image2 (np.ndarray): The second image as a NumPy array.

    Returns:
        float: The RMSE value between the two images.

    Raises:
        ValueError: If the input images do not have the same shape.
    """
    # Ensure both images have the same shape
    if image1.shape != image2.shape:
        raise ValueError("Both images must have the same dimensions.")

    # Calculate the Mean Squared Error (MSE) between the two images
    mse_value = mean_squared_error(image1, image2)

    # Calculate the Root Mean Square Error (RMSE) from the MSE
    rmse_value = np.sqrt(mse_value)

    return rmse_value


def calculate_psnr(image1: np.ndarray, image2: np.ndarray, data_range_mode="data_type") -> float:
    """
    Calculate the Peak Signal-to-Noise Ratio (PSNR) between two multi-band images.

    PSNR is a common metric used to measure the quality of reconstruction of images.
    Higher PSNR values generally indicate better image quality, where the two images
    are more similar.

    Args:
        image1 (np.ndarray): The first image as a NumPy array.
        image2 (np.ndarray): The second image as a NumPy array.
        data_range_mode : data_range setting, either data_type based or data_min_max calculated [data_type : take the value of the datatype OR data_min_max : take the max-min of the image1]

    Returns:
        float: The PSNR value between the two images in decibels (dB).

    Raises:
        ValueError: If the input images do not have the same shape.
    """
    # Ensure both images have the same shape
    if image1.shape != image2.shape:
        raise ValueError("Both images must have the same dimensions.")
    if data_range_mode == "data_type":
        data_range = get_data_type_range(image1.dtype)
    elif data_range_mode == "data_min_max":
        data_range = image1.max() - image1.min()
    else:
        raise ValueError("Invalid data range mode \"" + str(data_range_mode) + "\"")

    # Calculate the PSNR value considering the data range of the images
    psnr_value = psnr(image1, image2, data_range=data_range)

    return psnr_value


def get_data_type_range(dtype: np.dtype, verbose=False):
    """
        Cette fonction renvoie l'intervalle de valeurs possibles pour un type de donnée donné (entier ou flottant).
        - Pour les types entiers, elle utilise np.iinfo.
        - Pour les types flottants, elle utilise np.finfo.
        verbose est a false par defaut, mettre a true pour avoir les info de min et max
        """
    """min_value = np.float128
    max_value = np.float128"""

    if np.issubdtype(dtype, np.integer):
        # Pour les types entiers
        min_value = np.iinfo(dtype).min
        max_value = np.iinfo(dtype).max
    elif np.issubdtype(dtype, np.floating):
        # Pour les types flottants
        min_value = np.float64(np.finfo(dtype).min)
        max_value = np.float64(np.finfo(dtype).max)
    else:
        raise ValueError(f"Type de donnée non supporté : {dtype}")
    """if verbose:
        print("datatype min = ", min_value, " & datatype max = ", max_value)"""
    if verbose: print("get_data_type_range for dtype[", dtype, "]--- min = [", min_value, "] max = [", max_value, "]")
    if np.isinf(max_value - min_value):
        raise ValueError(
            f"Type de donnée non supporté car valeures trop grandes pour le type {dtype} min_value = {min_value}, max_value = {max_value}")
    return max_value - min_value


# TODO ssim badest score for 2 images that are not the same is not so low, is that important ?
def calculate_ssim_multiband(image1: np.ndarray, image2: np.ndarray, data_range_mode="data_type",
                             verbose=False) -> float:
    """
    Calculate the average Structural Similarity Index (SSIM) between two images,
    processing each band separately for multi-band images.

    The SSIM metric is used to measure the similarity between two images. It is
    particularly useful for assessing image quality where higher values indicate
    better similarity. For multi-band images, SSIM is computed for each band separately
    and then averaged.

    Args:
        image1 (np.ndarray): The first image as a NumPy array (HxWxC or HxW).
        image2 (np.ndarray): The second image as a NumPy array (HxWxC or HxW).
        data_range_mode : data_range setting, either data_type based or data_min_max calculated [data_type : take the value of the datatype OR data_min_max : take the max-min of the image1]

    Returns:
        float: The average SSIM value between the two images.

    Raises:
        ValueError: If the input images do not have the same shape or have more than 3 dimensions.
    """
    # Ensure both images have the same shape
    if image1.shape != image2.shape:
        raise ValueError("Both images must have the same dimensions.")

    # Determine if the image is multi-band (3D) or single-band (2D)
    if image1.ndim == 3:
        # Multi-band image
        ssim_values = []
        for band in range(image1.shape[2]):
            # Calculate data range for each band
            if data_range_mode == "data_type":
                data_range = get_data_type_range(image1.dtype, verbose=verbose)
            else:
                data_range = max(image1[:, :, band].max() - image1[:, :, band].min(),
                                 image2[:, :, band].max() - image2[:, :, band].min())
            # Calculate SSIM for each band
            ssim_value = ssim(image1, image2, data_range=data_range, win_size=11, K1=0.01, K2=0.03,
                              use_sample_covariance=False, full=False)
            ssim_values.append(ssim_value)

        # Compute the average SSIM value across all bands
        return np.mean(ssim_values)

    elif image1.ndim == 2:
        # Single-band image
        if data_range_mode == "data_type":
            data_range = get_data_type_range(image1.dtype, verbose=verbose)
        elif data_range_mode == "data_min_max":
            data_range = image1.max() - image1.min()
        else:
            raise ValueError("Invalid data range mode \"" + str(data_range_mode) + "\"")
        # print('data_range = ',data_range)

        return ssim(image1, image2, data_range=data_range, win_size=11, K1=0.01, K2=0.03, use_sample_covariance=False,
                    full=False)

    else:
        raise ValueError("Images must be either 2D or 3D.")


def calculate_ssim_multiband_with_blocks_of_even_size(image1: np.ndarray, image2: np.ndarray, tile_size: int = 5000,
                                                      data_range_mode="data_type",
                                                      verbose=False) -> float:
    # Ensure both images have the same shape
    if image1.shape != image2.shape:
        raise ValueError("Both images must have the same dimensions.")

    # Determine image dimensions
    height, width = image1.shape[:2]

    # Initialize SSIM list
    ssim_values = []

    # Loop over the image in tiles
    for i in range(0, height, tile_size):
        for j in range(0, width, tile_size):
            # Define the tile boundaries
            tile1 = image1[i:min(i + tile_size, height), j:min(j + tile_size, width)]
            tile2 = image2[i:min(i + tile_size, height), j:min(j + tile_size, width)]
            # tile1 = image1[i:i + tile_size, j:j + tile_size]
            # tile2 = image2[i:i + tile_size, j:j + tile_size]

            # Ensure both tiles have the same size
            if tile1.shape != tile2.shape:
                continue  # Skip this tile if shapes don't match (this could happen at the edges)

            # Determine if multi-band (3D) or single-band (2D)
            if tile1.ndim == 3:
                # Multi-band image
                for band in range(tile1.shape[2]):
                    # Calculate data range for each band
                    if data_range_mode == "data_type":
                        data_range = get_data_type_range(tile1.dtype, verbose=verbose)
                    else:
                        data_range = max(tile1[:, :, band].max() - tile1[:, :, band].min(),
                                         tile2[:, :, band].max() - tile2[:, :, band].min())

                    # Calculate SSIM for each band and append to list
                    if verbose: print("data range = [", data_range, "]")
                    ssim_value = ssim(tile1[:, :, band], tile2[:, :, band], data_range=data_range, win_size=11, K1=0.01,
                                      K2=0.03, use_sample_covariance=False)
                    ssim_values.append(ssim_value)

            elif tile1.ndim == 2:
                # Single-band image
                if data_range_mode == "data_type":
                    data_range = get_data_type_range(tile1.dtype, verbose=verbose)
                elif data_range_mode == "data_min_max":
                    data_range = tile1.max() - tile1.min()
                else:
                    raise ValueError("Invalid data range mode \"" + str(data_range_mode) + "\"")

                if verbose: print("data range = [", data_range, "]")
                # Calculate SSIM for the tile and append to list
                ssim_value = ssim(tile1, tile2, data_range=data_range, win_size=11, K1=0.01, K2=0.03,
                                  use_sample_covariance=False)
                ssim_values.append(ssim_value)

    # Return the average SSIM value across all tiles
    return np.mean(ssim_values)


def calculate_lpips_multiband_multiblock_of_even_size(image1: np.ndarray, image2: np.ndarray, loss_fn,
                                                      max_block_size: int = 2000, min_block_size=1000,
                                                      verbose=False) -> (
        list, float):
    """
    Calculate the LPIPS between two images, handling images with different dimensions and channels.
    The images are split into homogeneous tiles of the same size for processing.

    Args:
        image1 (np.ndarray): The first image as a NumPy array (HxWxC or HxW).
        image2 (np.ndarray): The second image as a NumPy array (HxWxC or HxW).
        loss_fn: A function that computes the LPIPS score given two image tensors.
        max_block_size (int): The maximum size of the tiles to split the image into for processing.

    Returns:
        tuple: A tuple containing:
            - A list of LPIPS values for each tile (or a single value if the image has 3 channels).
            - The average LPIPS value across tiles (or the LPIPS value itself if the image has 3 channels).
    """
    if verbose: print("calculate_lpips_multiband_multiblock_of_even_size...")

    def process_block(image1_block, image2_block):
        # Preprocess the images
        image1_block = preprocess_image(image1_block)
        image2_block = preprocess_image(image2_block)

        # Convert images to RGB if necessary
        if image1_block.ndim == 2:
            image1_block = convert_to_rgb(image1_block, verbose=verbose)
        if image2_block.ndim == 2:
            image2_block = convert_to_rgb(image2_block, verbose=verbose)

        # Convert images to torch tensors and permute dimensions for LPIPS calculation
        image1_tensor = torch.tensor(image1_block).permute(2, 0, 1).unsqueeze(0).float()
        image2_tensor = torch.tensor(image2_block).permute(2, 0, 1).unsqueeze(0).float()

        if image1_tensor.shape[1] == 3:
            return loss_fn(image1_tensor, image2_tensor).item()
        else:
            n_bands = image1_block.shape[2]
            lpips_values = []

            for i in range(n_bands):
                # Convert each band to RGB format
                image1_band = np.repeat(image1_block[:, :, i:i + 1], 3, axis=2)
                image2_band = np.repeat(image2_block[:, :, i:i + 1], 3, axis=2)

                # Convert the bands to torch tensors
                image1_band_tensor = torch.tensor(image1_band).permute(2, 0, 1).unsqueeze(0).float()
                image2_band_tensor = torch.tensor(image2_band).permute(2, 0, 1).unsqueeze(0).float()

                lpips_value = loss_fn(image1_band_tensor, image2_band_tensor).item()
                lpips_values.append(lpips_value)

            return np.mean(lpips_values)

    height, width = image1.shape[:2]

    """# Calculate the number of tiles needed
    num_tiles_y = int(np.ceil(height / max_block_size))
    num_tiles_x = int(np.ceil(width / max_block_size))

    # Calculate the adjusted tile size to ensure homogeneous tiles
    tile_height = max(min_block_size, height // num_tiles_y)
    tile_width = max(min_block_size, width // num_tiles_x)

    lpips_scores = []

    for y in range(0, height, tile_height):
        for x in range(0, width, tile_width):
            # Adjust tile dimensions at the borders
            end_y = min(y + tile_height, height)
            end_x = min(x + tile_width, width)
            # print(f"Image block y[{y}:{end_y}]x[{x},{end_x}]")
            # Extract blocks from each image
            print(" block_image1 = image1[",y,":",end_y,",",x,":",end_x,")")
            block_image1 = image1[y:end_y, x:end_x]
            block_image2 = image2[y:end_y, x:end_x]

            # Calculate LPIPS for this block
            block_lpips = process_block(block_image1, block_image2)
            lpips_scores.append(block_lpips)"""
    lpips_scores = []
    y = 0

    # Process rows
    while y < height:
        # Determine block height
        remaining_height = height - y
        block_height = min(max_block_size, remaining_height)
        if block_height < min_block_size:
            block_height = remaining_height  # Take the remaining part if it's smaller than the minimum block size

        x = 0

        # Process columns
        while x < width:
            # Determine block width
            remaining_width = width - x
            block_width = min(max_block_size, remaining_width)
            if block_width < min_block_size:
                block_width = remaining_width  # Take the remaining part if it's smaller than the minimum block size

            # Extract blocks from the images
            end_y = min(y + block_height, height)
            end_x = min(x + block_width, width)
            block_image1 = image1[y:end_y, x:end_x]
            block_image2 = image2[y:end_y, x:end_x]

            # Debug printing
            if verbose:
                print(f"Processing block: y[{y}:{end_y}], x[{x}:{end_x}]")

            # Calculate LPIPS for this block
            block_lpips = process_block(block_image1, block_image2)
            lpips_scores.append(block_lpips)

            # Move to the next column
            x += block_width

        # Move to the next row
        y += block_height

    mean_lpips = np.mean(lpips_scores)
    return lpips_scores, mean_lpips


def calculate_lpips_multiband__multiblock_of_fixed_size(image1: np.ndarray, image2: np.ndarray, loss_fn,
                                                        max_block_size: int = 5000, verbose=False) -> (
        list, float):
    """
    Calculate the Learned Perceptual Image Patch Similarity (LPIPS) between two images,
    handling images with different dimensions and channels.

    LPIPS is a metric used to evaluate the perceptual similarity between images. It
    considers the learned features from a deep network and provides a similarity score.
    work on blocks of max 5000x5000 (border of images can be uneven
    Args:
        image1 (np.ndarray): The first image as a NumPy array (HxWxC or HxW).
        image2 (np.ndarray): The second image as a NumPy array (HxWxC or HxW).
        loss_fn: A function that computes the LPIPS score given two image tensors.
        max_block_size (int): The maximum size of the blocks to split the image into for processing.

    Returns:
        tuple: A tuple containing:
            - A list of LPIPS values for each band (or a single value if the image has 3 channels).
            - The average LPIPS value across bands (or the LPIPS value itself if the image has 3 channels).

    Raises:
        ValueError: If the input images do not have the same shape.
    """

    def process_block(image1_block, image2_block):
        # Preprocess the images
        image1_block = preprocess_image(image1_block)
        image2_block = preprocess_image(image2_block)

        # Convert images to RGB if necessary
        if image1_block.ndim == 2:
            image1_block = convert_to_rgb(image1_block, verbose=verbose)
        if image2_block.ndim == 2:
            image2_block = convert_to_rgb(image2_block, verbose=verbose)

        # Convert images to torch tensors and permute dimensions for LPIPS calculation
        image1_tensor = torch.tensor(image1_block).permute(2, 0, 1).unsqueeze(0).float()
        image2_tensor = torch.tensor(image2_block).permute(2, 0, 1).unsqueeze(0).float()

        if image1_tensor.shape[1] == 3:
            # Case where the image already has three channels (RGB)
            return loss_fn(image1_tensor, image2_tensor).item()

        else:
            # Case where the image has more than three channels (multi-band)
            n_bands = image1_block.shape[2]
            lpips_values = []

            for i in range(n_bands):
                # Convert each band to RGB format
                image1_band = np.repeat(image1_block[:, :, i:i + 1], 3, axis=2)
                image2_band = np.repeat(image2_block[:, :, i:i + 1], 3, axis=2)

                # Convert the bands to torch tensors
                image1_band_tensor = torch.tensor(image1_band).permute(2, 0, 1).unsqueeze(0).float()
                image2_band_tensor = torch.tensor(image2_band).permute(2, 0, 1).unsqueeze(0).float()

                # Calculate LPIPS for this band
                lpips_value = loss_fn(image1_band_tensor, image2_band_tensor).item()
                lpips_values.append(lpips_value)

            # Compute the average LPIPS value across bands for this block
            return np.mean(lpips_values)

    # Determine the number of blocks needed based on the max block size
    height, width = image1.shape[:2]
    lpips_scores = []

    for y in range(0, height, max_block_size):
        for x in range(0, width, max_block_size):
            # Extract blocks from each image
            # print(f"block [{y}:{y + max_block_size},{x}:{x + max_block_size}]")
            block_image1 = image1[y:y + max_block_size, x:x + max_block_size]
            block_image2 = image2[y:y + max_block_size, x:x + max_block_size]

            # Calculate LPIPS for this block
            block_lpips = process_block(block_image1, block_image2)
            lpips_scores.append(block_lpips)

    # Calculate the overall mean LPIPS score
    mean_lpips = np.mean(lpips_scores)
    return lpips_scores, mean_lpips


def calculate_lpips_multiband(image1: np.ndarray, image2: np.ndarray, loss_fn) -> (list, float):
    """
    Calculate the Learned Perceptual Image Patch Similarity (LPIPS) between two images,
    handling images with different dimensions and channels.

    LPIPS is a metric used to evaluate the perceptual similarity between images. It
    considers the learned features from a deep network and provides a similarity score.

    Args:
        image1 (np.ndarray): The first image as a NumPy array (HxWxC or HxW).
        image2 (np.ndarray): The second image as a NumPy array (HxWxC or HxW).
        loss_fn: A function that computes the LPIPS score given two image tensors.

    Returns:
        tuple: A tuple containing:
            - A list of LPIPS values for each band (or a single value if the image has 3 channels).
            - The average LPIPS value across bands (or the LPIPS value itself if the image has 3 channels).

    Raises:
        ValueError: If the input images do not have the same shape.
    """
    # Preprocess the images
    image1 = preprocess_image(image1)
    image2 = preprocess_image(image2)

    # Convert images to RGB if necessary (particularly if they are grayscale)
    if image1.ndim == 2:
        image1 = convert_to_rgb(image1)
    if image2.ndim == 2:
        image2 = convert_to_rgb(image2)

    # Convert images to torch tensors and permute dimensions for LPIPS calculation
    image1_tensor = torch.tensor(image1).permute(2, 0, 1).unsqueeze(0).float()
    image2_tensor = torch.tensor(image2).permute(2, 0, 1).unsqueeze(0).float()

    if image1_tensor.shape[1] == 3:
        # Case where the image already has three channels (RGB)
        lpips_value = loss_fn(image1_tensor, image2_tensor).item()
        return [lpips_value], lpips_value

    else:
        # Case where the image has more than three channels (multi-band)
        n_bands = image1.shape[2]
        lpips_values = []

        for i in range(n_bands):
            # Convert each band to RGB format
            image1_band = np.repeat(image1[:, :, i:i + 1], 3, axis=2)
            image2_band = np.repeat(image2[:, :, i:i + 1], 3, axis=2)

            # Convert the bands to torch tensors
            image1_band_tensor = torch.tensor(image1_band).permute(2, 0, 1).unsqueeze(0).float()
            image2_band_tensor = torch.tensor(image2_band).permute(2, 0, 1).unsqueeze(0).float()

            # Calculate LPIPS for this band
            lpips_value = loss_fn(image1_band_tensor, image2_band_tensor).item()
            lpips_values.append(lpips_value)

        # Compute the average LPIPS value across bands
        mean_lpips = np.mean(lpips_values)
        return lpips_values, mean_lpips


def calculate_metrics_statistics(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcule la moyenne et l'écart type des valeurs dans les métriques et ajoute ces informations au dictionnaire.

    Args:
        data (Dict[str, Any]): Dictionnaire contenant les métriques avec les valeurs associées aux fichiers TIFF sous la clé 'results'.

    Returns:
        Dict[str, Any]: Dictionnaire mis à jour avec les statistiques de la métrique.
    """
    metrics = data.get("metrics", {})

    # Parcours des métriques dans le dictionnaire
    for metric_name, metric_data in metrics.items():
        # Vérifie si la clé est un dictionnaire de métriques
        if isinstance(metric_data, dict) and 'results' in metric_data:
            results = metric_data['results']

            # Filtrer uniquement les valeurs numériques des fichiers TIFF
            values = list(results.values())

            if values:
                # Calculer la moyenne et l'écart type
                try:
                    average = np.mean(values)
                    # Ajouter les statistiques au dictionnaire des métriques
                    metrics[metric_name]['average'] = round(average, 3)  # Arrondir pour la lisibilité
                except:
                    average = None
                    metrics[metric_name]['average'] = "None"  # Arrondir pour la lisibilité
                try:
                    stdev = np.std(values)
                    metrics[metric_name]['stdev'] = round(stdev, 3)  # Arrondir pour la lisibilité
                except:
                    average = None
                    metrics[metric_name]['stdev'] = "None"  # Arrondir pour la lisibilité

    return data


def calculate_lrsp(image1_path, image2_path, data_range_mode="data_type", verbose=False,
                   computing_block_size=2500) -> dict:
    """
        Calcule les métriques de comparaison entre deux images : LPIPS, SSIM, PSNR et RMSE.

        Args:
            image1_path (str): Chemin vers la première image.
            image2_path (str): Chemin vers la seconde image.
            data_range_mode : data_range setting for SSIM or PSNR, either data_type based or data_min_max calculated [data_type : take the value of the datatype OR data_min_max : take the max-min of the image1]

        Returns:
            dict: Un dictionnaire contenant les résultats des métriques de comparaison avec des informations sur la bibliothèque utilisée et la version.

        Raises:
            ValueError: Si les deux images n'ont pas les mêmes dimensions.
        """
    loss_fn = initialize_LPIPS()
    # load images and show shapes
    image1 = io.imread(image1_path)
    # print(image1, " [shape =", image1.shape, ", min =", np.min(image1), ", max =", np.max(image1), ", dtype = ",
    # image1.dtype, "]")
    image2 = io.imread(image2_path)
    # print(image2, " [shape =", image2.shape, ", min =", np.min(image2), ", max =", np.max(image2), ", dtype = ",
    # image2.dtype, "]")

    # checking if images have the same shape
    if verbose: print("image1.shape = [", image1.shape, "]")
    if image1.shape != image2.shape:
        raise ValueError("Les deux images ( ", image1_path, " & ", image2_path,
                         " ) doivent avoir les mêmes dimensions. image1.shape[", image1.shape, "] != [", image2.shape,
                         "]image2.shape")

    # Calculate all metrics
    lpips_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lpips_func = calculate_lpips_multiband_multiblock_of_even_size
    lpips_values, lpips_value = lpips_func(image1, image2, loss_fn, computing_block_size, verbose=verbose)

    mean_ssim_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ssim_func = calculate_ssim_multiband_with_blocks_of_even_size
    mean_ssim = ssim_func(image1, image2, tile_size=computing_block_size, data_range_mode=data_range_mode,
                          verbose=verbose)

    psnr_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    psnr_value = calculate_psnr(image1, image2, data_range_mode=data_range_mode)

    rmse_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rmse_value = calculate_rmse(image1, image2)

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    image_1_name = os.path.basename(image1_path)
    data = {
        "metrics": {
            "LPIPS": {
                "library": "lpips",
                "version": lib_meta.version("lpips"),
                "COPEX high compression library version": utils.get_lib_version(),
                "block handling": lpips_func.__name__,
                "block size": computing_block_size,
                "date": lpips_date,
                "results": {
                    image_1_name: lpips_value
                }
            },
            "SSIM": {
                "library": "scikit-image",
                "version": lib_meta.version("scikit-image"),
                "COPEX high compression library version": utils.get_lib_version(),
                "block handling": ssim_func.__name__,
                "block size": computing_block_size,
                "date": mean_ssim_date,
                "data range mode": data_range_mode,
                "results": {
                    image_1_name: mean_ssim
                }
            },
            "PSNR": {
                "library": "scikit-image",
                "version": lib_meta.version("scikit-image"),
                "COPEX high compression library version": utils.get_lib_version(),
                "date": psnr_date,
                "data range mode": data_range_mode,
                "results": {
                    image_1_name: str(psnr_value) if math.isinf(psnr_value) else psnr_value
                }
            },
            "RMSE": {
                "library": "scikit-image",
                "version": lib_meta.version("scikit-image"),
                "COPEX high compression library version": utils.get_lib_version(),
                "date": rmse_date,
                "results": {
                    image_1_name: rmse_value
                }
            }
        }
    }
    return data


def calculate_lrsp_for_uneven_tiles(image1_path, image2_path, data_range_mode="data_type", verbose=False,
                                    computing_block_size=2500, do_calculate_lpips=True, do_calculate_rmse=True,
                                    do_calculate_ssim=True, do_calculate_psnr=True) -> dict:
    """
        Calcule les métriques de comparaison entre deux images : LPIPS, SSIM, PSNR et RMSE.

        Args:
            image1_path (str): Chemin vers la première image.
            image2_path (str): Chemin vers la seconde image.
            data_range_mode : data_range setting for SSIM or PSNR, either data_type based or data_min_max calculated [data_type : take the value of the datatype OR data_min_max : take the max-min of the image1]

        Returns:
            dict: Un dictionnaire contenant les résultats des métriques de comparaison avec des informations sur la bibliothèque utilisée et la version.

        Raises:
            ValueError: Si les deux images n'ont pas les mêmes dimensions.
        """
    loss_fn = initialize_LPIPS()
    # load images and show shapes
    image1 = io.imread(image1_path)
    image1 = image1.astype(np.float16)
    # print(image1, " [shape =", image1.shape, ", min =", np.min(image1), ", max =", np.max(image1), ", dtype = ",
    # image1.dtype, "]")
    image2 = io.imread(image2_path)
    # print(image2, " [shape =", image2.shape, ", min =", np.min(image2), ", max =", np.max(image2), ", dtype = ",
    # image2.dtype, "]")

    # checking if images have the same shape
    if verbose: print("image1.shape = [", image1.shape, "]")
    if image1.shape != image2.shape:
        # Récupérer les dimensions des deux images
        rows1, cols1 = image1.shape[:2]
        rows2, cols2 = image2.shape[:2]

        # Déterminer le nombre maximum de lignes et colonnes communes
        max_rows = min(rows1, rows2)
        max_cols = min(cols1, cols2)
        print("Les deux images ( ", image1_path, " & ", image2_path,
              " ) doivent avoir les mêmes dimensions. image1.shape[", image1.shape, "] != [", image2.shape,
              "]image2.shape, ici on coupe pour avoir au final ....")
        if len(image1.shape) == 3:  # Si les images sont en couleur (3 canaux), on garde les canaux
            image1 = image1[:max_rows, :max_cols, :]
        else:  # Si les images sont en niveau de gris (2 dimensions)
            image1 = image1[:max_rows, :max_cols]

        if len(image2.shape) == 3:
            image2 = image2[:max_rows, :max_cols, :]
        else:
            image2 = image2[:max_rows, :max_cols]
        print("image1.shape[", image1.shape, "] != [", image2.shape, "]")

    # Calculate all metrics
    if do_calculate_lpips:
        lpips_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        lpips_func = calculate_lpips_multiband_multiblock_of_even_size
        lpips_values, lpips_value = lpips_func(image1, image2, loss_fn, computing_block_size, verbose=verbose)

    if do_calculate_ssim:
        mean_ssim_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ssim_func = calculate_ssim_multiband_with_blocks_of_even_size
        mean_ssim = ssim_func(image1, image2, tile_size=computing_block_size, data_range_mode=data_range_mode,
                              verbose=verbose)

    if do_calculate_psnr:
        psnr_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        psnr_value = calculate_psnr(image1, image2, data_range_mode=data_range_mode)

    if do_calculate_rmse:
        rmse_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rmse_value = calculate_rmse(image1, image2)

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    image_1_name = os.path.basename(image1_path)
    final_data = {}
    if do_calculate_lpips:
        tmp_data = {
            "metrics": {
                "LPIPS": {
                    "library": "lpips",
                    "version": lib_meta.version("lpips"),
                    "COPEX high compression library version": utils.get_lib_version(),
                    "block handling": lpips_func.__name__,
                    "block size": computing_block_size,
                    "date": lpips_date,
                    "results": {
                        image_1_name: lpips_value
                    }
                }
            }
        }
        utils.add_data_to_dict(final_data, tmp_data)
    if do_calculate_rmse:
        tmp_data = {
            "metrics": {
                "RMSE": {
                    "library": "scikit-image",
                    "version": lib_meta.version("scikit-image"),
                    "COPEX high compression library version": utils.get_lib_version(),
                    "date": rmse_date,
                    "results": {
                        image_1_name: rmse_value
                    }
                }
            }
        }
        utils.add_data_to_dict(final_data, tmp_data)
    if do_calculate_ssim:
        tmp_data = {
            "metrics": {
                "SSIM": {
                    "library": "scikit-image",
                    "version": lib_meta.version("scikit-image"),
                    "COPEX high compression library version": utils.get_lib_version(),
                    "block handling": ssim_func.__name__,
                    "block size": computing_block_size,
                    "date": mean_ssim_date,
                    "data range mode": data_range_mode,
                    "results": {
                        image_1_name: mean_ssim
                    }
                }
            }
        }
        utils.add_data_to_dict(final_data, tmp_data)
    if do_calculate_psnr:
        tmp_data = {
            "metrics": {
                "PSNR": {
                    "library": "scikit-image",
                    "version": lib_meta.version("scikit-image"),
                    "COPEX high compression library version": utils.get_lib_version(),
                    "date": psnr_date,
                    "data range mode": data_range_mode,
                    "results": {
                        image_1_name: str(psnr_value) if math.isinf(psnr_value) else psnr_value
                    }
                }
            }
        }
        utils.add_data_to_dict(final_data, tmp_data)
    return final_data


def calculate_min(image1_path, suffixe="", verbose=False, computing_block_size=2500, calculate_min=True) -> dict:
    """
        Calcule les métriques de comparaison entre deux images : LPIPS, SSIM, PSNR et RMSE.

        Args:
            image1_path (str): Chemin vers la première image.
            image2_path (str): Chemin vers la seconde image.
            data_range_mode : data_range setting for SSIM or PSNR, either data_type based or data_min_max calculated [data_type : take the value of the datatype OR data_min_max : take the max-min of the image1]

        Returns:
            dict: Un dictionnaire contenant les résultats des métriques de comparaison avec des informations sur la bibliothèque utilisée et la version.

        Raises:
            ValueError: Si les deux images n'ont pas les mêmes dimensions.
        """
    # load images and show shapes
    image1 = io.imread(image1_path)
    image1 = image1.astype(np.float16)

    if verbose: print("image1.shape = [", image1.shape, "]")
    # Récupérer les dimensions des deux images
    # Calculate all metrics
    min_value = image1.min()

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    image_1_name = os.path.basename(image1_path)
    final_data = {}

    data = {
        "metrics": {
            "min" + suffixe: {
                "library": "scikit-image",
                "version": lib_meta.version("scikit-image"),
                "COPEX high compression library version": utils.get_lib_version(),
                "date": current_date,
                "results": {
                    image_1_name: str(min_value)
                }
            }
        }
    }
    utils.add_data_to_dict(final_data, data)
    return data


def calculate_max(image1_path, suffixe="", verbose=False, computing_block_size=2500, calculate_min=True) -> dict:
    """
        Calcule les métriques de comparaison entre deux images : LPIPS, SSIM, PSNR et RMSE.

        Args:
            image1_path (str): Chemin vers la première image.
            image2_path (str): Chemin vers la seconde image.
            data_range_mode : data_range setting for SSIM or PSNR, either data_type based or data_min_max calculated [data_type : take the value of the datatype OR data_min_max : take the max-min of the image1]

        Returns:
            dict: Un dictionnaire contenant les résultats des métriques de comparaison avec des informations sur la bibliothèque utilisée et la version.

        Raises:
            ValueError: Si les deux images n'ont pas les mêmes dimensions.
        """
    # load images and show shapes
    image1 = io.imread(image1_path)
    image1 = image1.astype(np.float16)

    if verbose: print("image1.shape = [", image1.shape, "]")
    # Récupérer les dimensions des deux images
    # Calculate all metrics
    max_value = image1.max()

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    image_1_name = os.path.basename(image1_path)
    final_data = {}

    data = {
        "metrics": {
            "max" + suffixe: {
                "library": "scikit-image",
                "version": lib_meta.version("scikit-image"),
                "COPEX high compression library version": utils.get_lib_version(),
                "date": current_date,
                "results": {
                    image_1_name: str(max_value)
                }
            }
        }
    }
    utils.add_data_to_dict(final_data, data)
    return data


def calculate_mean(image1_path, suffixe="", verbose=False, computing_block_size=2500, calculate_min=True) -> dict:
    """
        Calcule les métriques de comparaison entre deux images : LPIPS, SSIM, PSNR et RMSE.

        Args:
            image1_path (str): Chemin vers la première image.
            image2_path (str): Chemin vers la seconde image.
            data_range_mode : data_range setting for SSIM or PSNR, either data_type based or data_min_max calculated [data_type : take the value of the datatype OR data_min_max : take the max-min of the image1]

        Returns:
            dict: Un dictionnaire contenant les résultats des métriques de comparaison avec des informations sur la bibliothèque utilisée et la version.

        Raises:
            ValueError: Si les deux images n'ont pas les mêmes dimensions.
        """
    # load images and show shapes
    image1 = io.imread(image1_path)
    image1 = image1.astype(np.float16)

    if verbose: print("image1.shape = [", image1.shape, "]")
    # Récupérer les dimensions des deux images
    # Calculate all metrics
    mean_value = np.mean(image1)

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    image_1_name = os.path.basename(image1_path)
    final_data = {}

    data = {
        "metrics": {
            "mean" + suffixe: {
                "library": "numpy",
                "version": lib_meta.version("numpy"),
                "COPEX high compression library version": utils.get_lib_version(),
                "date": current_date,
                "results": {
                    image_1_name: str(mean_value)
                }
            }
        }
    }
    utils.add_data_to_dict(final_data, data)
    return data


def calculate_stdev(image1_path, suffixe="", verbose=False, computing_block_size=2500, calculate_min=True) -> dict:
    """
        Calcule les métriques de comparaison entre deux images : LPIPS, SSIM, PSNR et RMSE.

        Args:
            image1_path (str): Chemin vers la première image.
            image2_path (str): Chemin vers la seconde image.
            data_range_mode : data_range setting for SSIM or PSNR, either data_type based or data_min_max calculated [data_type : take the value of the datatype OR data_min_max : take the max-min of the image1]

        Returns:
            dict: Un dictionnaire contenant les résultats des métriques de comparaison avec des informations sur la bibliothèque utilisée et la version.

        Raises:
            ValueError: Si les deux images n'ont pas les mêmes dimensions.
        """
    # load images and show shapes
    image1 = io.imread(image1_path)
    image1 = image1.astype(np.float16)

    if verbose: print("image1.shape = [", image1.shape, "]")
    # Récupérer les dimensions des deux images
    # Calculate all metrics
    std_value = np.std(image1)

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    image_1_name = os.path.basename(image1_path)
    final_data = {}

    data = {
        "metrics": {
            "std" + suffixe: {
                "library": "numpy",
                "version": lib_meta.version("numpy"),
                "COPEX high compression library version": utils.get_lib_version(),
                "date": current_date,
                "results": {
                    image_1_name: str(std_value)
                }
            }
        }
    }
    utils.add_data_to_dict(final_data, data)
    return data


def calculate_clamped_max(image1_path, suffixe="", clamp_percentage=0.002, verbose=False, computing_block_size=2500,
                          calculate_min=True) -> dict:
    """
        Calcule les métriques de comparaison entre deux images : LPIPS, SSIM, PSNR et RMSE.

        Args:
            image1_path (str): Chemin vers la première image.
            image2_path (str): Chemin vers la seconde image.
            data_range_mode : data_range setting for SSIM or PSNR, either data_type based or data_min_max calculated [data_type : take the value of the datatype OR data_min_max : take the max-min of the image1]

        Returns:
            dict: Un dictionnaire contenant les résultats des métriques de comparaison avec des informations sur la bibliothèque utilisée et la version.

        Raises:
            ValueError: Si les deux images n'ont pas les mêmes dimensions.
        """
    # load images and show shapes
    image1 = io.imread(image1_path)
    image1 = image1.astype(np.float16)

    if verbose: print("image1.shape = [", image1.shape, "]")
    # Récupérer les dimensions des deux images
    # Calculate all metrics
    # Aplatir l'image en une seule dimension (pour faciliter le tri)
    flattened_image = image1.flatten()

    # Trier les valeurs des pixels
    sorted_values = np.sort(flattened_image)

    # Calculer le nombre de valeurs à exclure (0.2% des plus grandes valeurs)
    clamp_index = int((1 - clamp_percentage) * len(sorted_values))

    # Trouver le nouveau max après avoir exclu les 0.2% des plus grandes valeurs
    clamped_max = sorted_values[clamp_index - 1]

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    image_1_name = os.path.basename(image1_path)
    final_data = {}

    data = {
        "metrics": {
            "clamped_max" + suffixe + "_" + str(clamp_percentage): {
                "library": "numpy",
                "version": lib_meta.version("numpy"),
                "COPEX high compression library version": utils.get_lib_version(),
                "date": current_date,
                "results": {
                    image_1_name: str(clamped_max)
                }
            }
        }
    }
    utils.add_data_to_dict(final_data, data)
    return data


def calculate_excluded_value_number_if_clamp_right(image1_path, suffixe="", clamp_value=1000, verbose=False,
                                                   computing_block_size=2500, calculate_min=True) -> dict:
    """
        Calcule les métriques de comparaison entre deux images : LPIPS, SSIM, PSNR et RMSE.

        Args:
            image1_path (str): Chemin vers la première image.
            image2_path (str): Chemin vers la seconde image.
            data_range_mode : data_range setting for SSIM or PSNR, either data_type based or data_min_max calculated [data_type : take the value of the datatype OR data_min_max : take the max-min of the image1]

        Returns:
            dict: Un dictionnaire contenant les résultats des métriques de comparaison avec des informations sur la bibliothèque utilisée et la version.

        Raises:
            ValueError: Si les deux images n'ont pas les mêmes dimensions.
    """
    # load images and show shapes
    image1 = io.imread(image1_path)
    image1 = image1.astype(np.float16)

    if verbose: print("image1.shape = [", image1.shape, "]")
    # Récupérer les dimensions des deux images
    # Calculate all metrics
    # Aplatir l'image en une seule dimension (pour faciliter le tri)
    flattened_image = image1.flatten()

    exluded_values_count = np.sum(flattened_image > clamp_value)

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    image_1_name = os.path.basename(image1_path)
    final_data = {}

    data = {
        "metrics": {
            "clamped_value_number" + suffixe + "_" + str(clamp_value): {
                "library": "numpy",
                "version": lib_meta.version("numpy"),
                "COPEX high compression library version": utils.get_lib_version(),
                "date": current_date,
                "results": {
                    image_1_name: str(exluded_values_count)
                }
            }
        }
    }
    utils.add_data_to_dict(final_data, data)
    return data


def calculate_compression_factor(image1_path: str, image2_path: str, verbose=False) -> dict:
    """
    Calcule le facteur de compression entre deux images et retourne un dictionnaire avec les résultats.

    Args:
        image1_path (str): Chemin vers la première image (image non compressée).
        image2_path (str): Chemin vers la seconde image (image compressée).
        verbose (bool): Si vrai, imprime des informations supplémentaires pour le débogage.

    Returns:
        dict: Un dictionnaire contenant le facteur de compression et des informations sur la version de la bibliothèque.
    """

    # Récupérer les noms des images
    image_1_name = os.path.basename(image1_path)
    image_2_name = os.path.basename(image2_path)

    # Obtenir la taille des fichiers en octets
    size_image1 = os.path.getsize(image1_path)
    size_image2 = os.path.getsize(image2_path)

    if verbose:
        print(f"Taille de {image_1_name}: {size_image1} octets")
        print(f"Taille de {image_2_name}: {size_image2} octets")

    # Calculer le facteur de compression
    if size_image2 > 0:
        compression_factor = size_image1 / size_image2
    else:
        raise ValueError("La taille de la seconde image est nulle, impossible de calculer le facteur de compression.")

    # Création du dictionnaire de résultat
    data = {
        "metrics": {
            "Compression factor": {
                "COPEX high compression library version": utils.get_lib_version(),
                "results": {
                    image_1_name: compression_factor
                }
            }
        }
    }

    if verbose:
        print(f"Facteur de compression calculé : {compression_factor}")

    return data

# COPEX High Rate Compression Quality Metrics

This package provides quality metrics for high rate compression.

## Installation

```console
pip install COPEX_high_rate_compression_quality_metrics
```

## Library usage
### Comparison of Two Multiband TIFF Images via LRSP (L:LPIPS, R:RMSE, S:SSIM, P:PSNR)

the following shows concrete example of use of the library

### Steps:
1. Import necessary libraries
2. Initialize the model and specify the file paths
3. Define preprocessing functions
4. Load the TIFF files
5. Calculate the metrics individually
6. Json Builder


### 1 Library install / import
use "pip install COPEX-high-rate-compression-quality-metrics" to install the library


```python
# Array handler
import numpy as np
# to have a json formated output
import json
import math
# File handler
from skimage import io

# File path handler
import os

# Metrics and utils
import COPEX_high_rate_compression_quality_metrics.metrics as COPEX_metrics
import COPEX_high_rate_compression_quality_metrics.utils as COPEX_utils
```

### 2 LPIPS initialization


```python
# LPIPS initialization
loss_fn = COPEX_metrics.initialize_LPIPS()
```


### 3 File path definition


```python
# Specify file paths here
file_path1 = os.path.join('T28PGV_20160318T111102_B04_20m.tif')
file_path2 = os.path.join('T28PGV_20160318T111102_B04_20m_ter.tif')
```

### 4 File loading


```python
#load images and show shapes
image1 = io.imread(file_path1)
print(file_path1," [shape =",image1.shape,", min =",np.min(image1), ", max =",np.max(image1), ", dtype = ",image1.dtype,"]")
image2 = io.imread(file_path2)
print(file_path2," [shape =",image2.shape,", min =",np.min(image2), ", max =",np.max(image2), ", dtype = ",image2.dtype,"]")


# checking if images have the same shape
if image1.shape != image2.shape:
    raise ValueError("Les deux images doivent avoir les mêmes dimensions.")
print("images loaded with success.")
```


### File visualization (optional)


```python
COPEX_utils.display_multiband_tiffs(image1, image2)
```


    
![png](output_10_0.png)
    


### 5 metrics calculation


```python
# Calculate all metrics
lpips_values,lpips_value = COPEX_metrics.calculate_lpips_multiband(image1, image2,loss_fn)
mean_ssim = COPEX_metrics.calculate_ssim_multiband(image1, image2)
psnr_value = COPEX_metrics.calculate_psnr(image1, image2)
rmse_value = COPEX_metrics.calculate_rmse(image1, image2)
```

## Results interpretation
### see <span style="color:#68E8D7">VT-P382-SLD-003-E-01-00_COPEX_DCC_PM3_20230630.pdf</span> for more informations about metrics weeknesses

<span style="color:#407CBF">LPIPS</span> : (<span style="color:#19E629">identical images</span>) <b>0 <==========> 1</b> (<span style="color:#F55353">completely different images</span>) <b>lower is better</b> [very good LPIPS do not mean that images are not totaly different pixel wise]

<span style="color:#BF40BB">RMSE</span> : (<span style="color:#19E629">identical images</span>) <b>0 <==========> +inf</b> (<span style="color:#F55353">completely different images</span>) <b>lower is better</b> [different kind of degradations can give the same score, do not capture blurring]

<span style="color:#BF8340">SSIM</span> : (<span style="color:#F55353">completely different images</span>) <b>-1 <==========> 1</b> (<span style="color:#19E629">identical images</span>) <b>higher is better</b> [sensible to little local distorions, sensible to noise differences]

<span style="color:#40BF44">PSNR</span> : (<span style="color:#F55353">completely different images</span>) <b>0 <==========> +inf</b> (<span style="color:#19E629">identical images</span>) <b>higher is better</b> [sensible to Big local differences]


```python
data = {
    "files paths":{
        "file1":file_path1,
        "file2":file_path2
        },
    "metrics":{
        "LPIPS":lpips_value,
        "RMSE":rmse_value,
        "SSIM":mean_ssim,
        "PSNR":str(psnr_value) if math.isinf(psnr_value) else psnr_value     
    }
}
json_data = json.dumps(data, indent=4)

print(json_data)
```
```console

    {
        "files paths": {
            "file1": "T28PGV_20160318T111102_B04_20m.tif",
            "file2": "T28PGV_20160318T111102_B04_20m_ter.tif"
        },
        "metrics": {
            "LPIPS": 0.038381848484277725,
            "RMSE": 192.01308995822703,
            "SSIM": 0.9817911582274915,
            "PSNR": 26.491058156522357
        }
    }
```

## Json builder
### auto_update the bensh algo json file automaticly
#### 1 import library

```python 

import COPEX_high_rate_compression_quality_metrics.json_builder as json_builder
import COPEX_high_rate_compression_quality_metrics.metrics as metrics
```
#### 2 define pathparameters
```python

root_directory = "data"
dataset_name = "RANDOM"
test_case_number = 4
nnvvppp_algoname = "01-01-002_JPEG2000"
```
#### 3 calculate generics/thematics in any order you want

```python
#json_builder.initialize_json(root_directory=root_directory, dataset_name=dataset_name,test_case_number=test_case_number,nnvvppp_algoname=nnvvppp_algoname)
json_builder.make_generic(root_directory = root_directory,
                          dataset_name = dataset_name,
                          test_case_number = test_case_number,
                          nnvvppp_algoname = nnvvppp_algoname)

json_builder.make_thematic(root_directory,
                           dataset_name,
                           test_case_number,
                           nnvvppp_algoname,
                           thematic.compute_kmeans_score_for_multiband,
                           original_folder_path,
                           decompressed_folder_path,
                           satellite_type)
```
#### 4 look at results

```json
{
    "original_size": 525312,
    "compressed_size": 48637,
    "compression_factor": 10.8,
    "compression_time": 253,
    "decompression_time": 432,
    "compression_algorithm": "01-01-002_JPEG2000",
    "algorithm_version": "01",
    "compression_parameter": "002",
    "metrics": {
        "LPIPS": {
            "library": "scikit-image",
            "version": "0.24.0",
            "date": "2024-08-19 16:53:07",
            "results": {
                "4c_256_256_random_band_1.tif": 0.15013514459133148,
                "4c_256_256_random_band_2.tif": 0.1589806228876114,
                "4c_256_256_random_band_3.tif": 0.1509121209383011,
                "4c_256_256_random_band_4.tif": 0.1467234492301941
            },
            "average": 0.152,
            "stdev": 0.004
        },
        "SSIM": {
            "library": "scikit-image",
            "version": "0.24.0",
            "date": "2024-08-19 16:53:07",
            "results": {
                "4c_256_256_random_band_1.tif": 0.01048029893613139,
                "4c_256_256_random_band_2.tif": -0.0020971790915714186,
                "4c_256_256_random_band_3.tif": 0.007405245569149331,
                "4c_256_256_random_band_4.tif": 0.005087706587301147
            },
            "average": 0.005,
            "stdev": 0.005
        },
        "PSNR": {
            "library": "scikit-image",
            "version": "0.24.0",
            "date": "2024-08-19 16:53:07",
            "results": {
                "4c_256_256_random_band_1.tif": 7.801028498092282,
                "4c_256_256_random_band_2.tif": 7.75118324229439,
                "4c_256_256_random_band_3.tif": 7.785848197523122,
                "4c_256_256_random_band_4.tif": 7.762412297083275
            },
            "average": 7.775,
            "stdev": 0.019
        },
        "RMSE": {
            "library": "scikit-image",
            "version": "0.24.0",
            "date": "2024-08-19 16:53:07",
            "results": {
                "4c_256_256_random_band_1.tif": 26694.50541651717,
                "4c_256_256_random_band_2.tif": 26847.72648228625,
                "4c_256_256_random_band_3.tif": 26740.79206290665,
                "4c_256_256_random_band_4.tif": 26813.04036306841
            },
            "average": 26774.016,
            "stdev": 59.962
        }
    },
    "kmeans++S2-10-10-42": {
        "library": "scikit-learn",
        "version": "1.5.1",
        "date": "2024-09-11 17:18:17",
        "original bands": [
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "11",
            "12"
        ],
        "resampled bands": [
          "05",
          "06",
          "07",
          "11",
          "12"
        ],
        "resampled_bands_factor": 2,
        "metrics": {
            "overall_accuracy": {
                "results": {
                    "S2A_MSIL1C_20200111T105421_N0208_R051_T29NNJ_20200111T123505.kmeans++-10-10-42.tif": 0.6520533690996381
                },
                "average": 0.652,
                "stdev": 0.0
            },
            "kappa_coefficient": {
                "results": {
                    "S2A_MSIL1C_20200111T105421_N0208_R051_T29NNJ_20200111T123505.kmeans++-10-10-42.tif": 0.5610928393084549
                },
                "average": 0.561,
                "stdev": 0.0
            }
        }
    }
}
```

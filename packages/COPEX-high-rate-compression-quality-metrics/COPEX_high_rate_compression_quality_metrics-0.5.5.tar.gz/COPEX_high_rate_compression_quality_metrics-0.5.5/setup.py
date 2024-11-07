from setuptools import setup, find_packages
from COPEX_high_rate_compression_quality_metrics import utils

setup(
    name='COPEX_high_rate_compression_quality_metrics',
    version=utils.get_lib_version(),
    packages=find_packages(),
    include_package_data=True,  # Inclure les fichiers définis dans MANIFEST.in
    install_requires=[
        'importlib_metadata==8.2.0',
        'lpips==0.1.4',
        'matplotlib==3.9.2',
        'numpy==1.26.4',
        'scikit-image==0.24.0',
        'scikit-learn==1.5.1',
        'torch==2.4.0',
        'imagecodecs==2024.6.1'
    ],
    author='VisioTerra',
    author_email='info@visioterra.fr',
    description='COPEX high rate compression quality metrics',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/VisioTerra/COPEX_high_rate_compression_quality_metrics',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
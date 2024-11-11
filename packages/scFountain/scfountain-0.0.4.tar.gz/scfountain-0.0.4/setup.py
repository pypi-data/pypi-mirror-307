
# encoding=utf-8
from setuptools import setup, find_packages
import pathlib

#here = pathlib.Path(__file__).parent.resolve()

setup(
    name="scFountain",
    version="0.0.4",
    description="Rigorous integration of single-cell ATAC-seq data using regularized barycentric mapping",
    long_description='Single-cell assay for transposase-accessible chromatin using sequencing (scATAC-seq) deciphers genome-wide chromatin accessibility, providing profound insights into gene regulation mechanisms. With the rapid advance of sequencing technology, scATAC-seq data typically encompasses numerous samples generated under various conditions, leading to complex and multifactorial batch effects, thus necessitating reliable batch integration tools. Although numerous batch integration tools exist for single-cell RNA sequencing (scRNA-seq) data, their effectiveness on scATAC-seq data has proven limited due to the characteristic differences between scRNA-seq and scATAC-seq data. Existing integration methods for scATAC-seq data suffer from several fundamental limitations, such as disrupting the  biological heterogeneity and focusing solely on low-dimensional correction, which can lead to data distortion and hinder downstream analysis. Here we propose Fountain, a deep learning framework for scATAC-seq data integration via rigorous barycentric mapping. Fountain regularizes barycentric mapping with geometric data information to achieve biological heterogeneity-preserving integration. Through comprehensive experiments on multiple datasets involving various laboratory protocols, sample composition and species, we demonstrate the advantages of Fountain over existing methods in batch correction and biological conservation. Additionally, the trained Fountain model can integrate data from new batches alongside already integrated data without retraining, thereby facilitating the incorporation of additional data and enabling continuous online data integration. Moreover, we provide a reconstruction strategy to obtain batch-corrected ATAC profiles, which has been proven to  better capture cellular heterogeneity and reveal cell type-specific implications such as expression enrichment analysis and partitioned heritability analysis. ',
    license="MIT Licence",
    url="https://github.com/BioX-NKU/Fountain",
    author="BioX-NKU",
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
    keywords="scATAC-seq, batch integration, barycentric mapping, online integration, cell type-specific implication",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        'anndata>=0.8.0',
        'scanpy>=1.9.1',
        'torch>=1.12.1',
        'pandas>=1.4.2',
        'scikit-learn>=1.0.2',
        'numpy>=1.21.5',
        'scipy>=1.9.3',
        'episcanpy>=0.3.2',
        'tqdm>=4.28.1',      
    ]
)







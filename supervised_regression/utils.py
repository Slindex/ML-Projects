# File Management libraries
import tarfile
import urllib.request
from pathlib import Path

# Data Analytics libraries
import matplotlib.pyplot as plt

#ML libraries
import numpy as np


def downloadHousingData():

    zipfilePath = Path('data/housing.tgz')
    housingPath = Path('data/housing.csv')

    if not zipfilePath.is_file():
        Path('data').mkdir(parents=True, exist_ok=True)
        print('data/ directory created')

        URL = 'https://github.com/ageron/data/raw/main/housing.tgz'
        urllib.request.urlretrieve(URL, zipfilePath)
        print(f'data downloaded from {URL}')

    if not housingPath.is_file():
        with tarfile.open(zipfilePath) as housing_zip:
            housing_zip.extractall(path='data')
        print('Content Extracted into data/')

        csvPath = Path('data/housing/housing.csv')
        csvPath.rename(Path('data/housing.csv'))

        housingDirPath = Path('data/housing')
        housingDirPath.rmdir()


def saveGraph(graph_id, tight_layout=True, graph_extension='png', resolution=300):

    imagesPath = Path('images')
    imagesPath.mkdir(parents=True, exist_ok=True)

    graphPath = imagesPath/f'{graph_id}.{graph_extension}'

    if tight_layout:
        plt.tight_layout()
    
    plt.savefig(graphPath, format=graph_extension, dpi=resolution)


def randomDataSplitter(data, test_ratio=0.2):

    indexList = np.random.permutation(len(data))
    testSize = int(len(data) * test_ratio)

    testIndexes = indexList[:testSize]
    trainIndexes = indexList[testSize:]

    testSet = data.iloc[testIndexes]
    trainSet = data.iloc[trainIndexes]

    return trainSet, testSet
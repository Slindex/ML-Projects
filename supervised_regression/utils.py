# File Management libraries
import tarfile
import urllib.request
from zipfile import ZipFile
from pathlib import Path

# Data Analytics libraries
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns

# ML libraries
import numpy as np

# Math & Statistics
from math import ceil


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


def downloadCaliforniaMap():

    zipfilePath = Path('data/geodata/California_County_Boundaries.zip')
    mapPath = Path('data/geodata/California_County_Boundaries.shp')

    if not zipfilePath.is_file():
        Path('data/geodata').mkdir(parents=True, exist_ok=True)
        print('data/geodata/ directory created')

        URL = 'https://gis-calema.opendata.arcgis.com/datasets/59d92c1bf84a438d83f78465dce02c61_0.zip?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D'
        urllib.request.urlretrieve(URL, zipfilePath)
        print(f'Zip file downloaded from {URL}')

    if not mapPath.is_file():
        with ZipFile(zipfilePath, 'r') as map_zip:
            map_zip.extractall(path='data/geodata')
        print('Map Extracted into data/')


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


def thousandsFormat(x, p):
    return "{:,}".format(int(x))


def barGraph(filename, labels, values, tittle, xlabel, ylabel, color='#329D9C'):

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.bar(labels, values, color=color)

    ax.grid(True, color='grey', linewidth='0.5', axis='y', alpha=0.3)

    ax.set_axisbelow(True)

    ax.set_title(tittle, loc='center', pad=15, weight='bold', fontsize=10, fontfamily='arial')

    ax.set_xlabel(xlabel, labelpad=10, fontsize=9, fontfamily='arial')
    ax.set_ylabel(ylabel, labelpad=10, fontsize=9, fontfamily='arial')

    ax.tick_params(axis='both', which='both', bottom=False, left=False)
    ax.tick_params(axis='x', labelsize=8, labelfontfamily='arial')
    ax.tick_params(axis='y', labelsize=8, labelfontfamily='arial')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.yaxis.set_major_formatter(FuncFormatter(thousandsFormat))

    saveGraph(filename)


def multiHist(filename, df, bins=50, kde=True, bar_color='#329D9C', kde_color='#472F7D'):

    df = df.select_dtypes(include='number')

    numCols = len(df.columns)
    numRows = (numCols + 1) // 2

    height = ceil(numCols/2)*3
    figsize = (15, height)

    fig, axes = plt.subplots(nrows=numRows, ncols=2, figsize=figsize)

    fig.subplots_adjust(hspace=0.5)
    axes = axes.flatten()

    for i, column in enumerate(df.columns):
        ax = axes[i]

        sns.histplot(df[column], bins=bins, color=bar_color, alpha=1, kde=kde, line_kws={'lw': 1.5}, ax=ax) #type: ignore
        ax.lines[0].set_color(kde_color)

        ax.grid(True, color='grey', linewidth='0.5', axis='y', alpha=0.3)
        ax.set_axisbelow(True)

        ax.set_xlabel('')
        ax.set_ylabel('')

        ax.set_title(column, loc='center', pad=15, weight='bold', fontsize=12, fontfamily='arial')

        ax.tick_params(axis='x', labelsize=8, labelfontfamily='arial')
        ax.tick_params(axis='y', labelsize=8, labelfontfamily='arial')

    if numCols % 2 != 0:
        fig.delaxes(axes[-1])

    saveGraph(filename, tight_layout=False)
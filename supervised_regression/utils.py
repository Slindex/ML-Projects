# File Management libraries
import tarfile
import urllib.request
from pathlib import Path

def downloadHousingData():
    """
    Downloads the Housing data zip file from a GitHub repository, create the 'data' directory if not exists and finally extracts the content from the zip file.

    Parameters:
    None

    Returns:
    None
    """

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
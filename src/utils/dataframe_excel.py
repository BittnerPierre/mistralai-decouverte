import pandas as pd

from dotenv import load_dotenv, find_dotenv
from utils.config_loader import load_config

config = load_config()

# read local .env file
_ = load_dotenv(find_dotenv())

data_catalog = config['DATACATALOG']['DATA_CATALOG']


def get_dataset_from_excel():
    with open(data_catalog, 'rb') as file:
        df = pd.read_excel(file)
    list = []
    for row in df.to_dict(orient='records'):
        list.append(row)
    return list


def isColumnInExcel(columnName: str):
    with open(data_catalog, 'rb') as file:
        df = pd.read_excel(file)
    for row in df.to_dict(orient='records'):
        if columnName == row["Nom du champ technique"]:
            return True
    return False
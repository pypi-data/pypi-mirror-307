import json
import os

import geopandas as gpd
import requests


project_root = os.path.dirname(os.path.abspath(__file__))
drive_path = os.path.join(project_root, 'Google APIs', 'token_drive.json')
gmail_path = os.path.join(project_root, 'Google APIs', 'token_gmail.json')
sheets_path = os.path.join(project_root, 'Google APIs', 'token_sheets.json')


# Tracker
tokens = {
    "DEMAK COMERCIO, IMPORTACAO E EXPORTACAO LTDA.": {
        "code": 248302,
        "token": ""
    },
    "SG COMERCIO, IMPORTACAO E EXPORTACAO LTDA": {
        "code": 248683,
        "token": "620a874d-2ff8-4b92-9975-bcbfc3cbf2b8"
    },
    "homolog": {
        "code": "",
        "token": "11f816b7-eda3-4082-b202-c5a745c6cc1f"
    }
}

# Mapbox
mapbox_api_key = 'pk.eyJ1IjoiYW5kcmVmcmVpcmUiLCJhIjoiY2xtbTU1YjNhMGd3YTJybzJtdWluazM1biJ9.TEiRVhtnLzbqDINuHxhANQ'

# Correios
contrato_correio = "0078278236"


def token_correios() -> str:
    url = "https://api.correios.com.br/token/v1/autentica/cartaopostagem"

    payload = json.dumps({
        "numero": "0078278236"  # contrato_correio
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic NTE4Mjg4MTcwMDAxOTM6aE1oZ1l0VUpuQXAzT0NJVWpjTUI0SE53Q3h3T0JndmJaeDdtSEtQaA==',
        'Cookie': 'LBprdExt1=684195850.47873.0000'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return 'Bearer ' + response.json()['token']


# Google APIs
google_api_key: str = 'AIzaSyD-uw7IJhb5EKwibQXtAaUZ9GIFUzco6Vo'

drive_scopes = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
gmail_scopes = ["https://www.googleapis.com/auth/gmail.modify", "https://www.googleapis.com/auth/gmail.labels", "https://mail.google.com/",
                "https://www.googleapis.com/auth/spreadsheets"]
sheets_scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# Files
rodizio_polygon = gpd.read_file(os.path.join(project_root, 'Google APIs', 'shapesMiniAnel.shp'))
fretes_db_path = os.path.join(project_root, 'Google APIs', 'fretes.db')
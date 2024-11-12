import os
import pathlib
import sqlite3
import string
import csv
from functools import wraps
import time
import unicodedata
import re
import xmltodict
from google.auth.api_key import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from requests import Request
from shapely import Point, Polygon
import pandas as pd
import webbrowser
import folium
import base64
import os.path
from time import sleep
from typing import Any
from pacoFunctions import config
import googlemaps
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


#Decorator
def google_api_auth(path: str, scopes: list):
    """
    Decorator to handle Google API authentication.
    It retrieves and refreshes credentials if necessary,
    storing them for future use.

    Args:
        path (str): Path to the credentials JSON file.
        scopes (list): List of scopes required for the API.

    Returns:
        function: Decorated function with Google API credentials.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            creds = None
            if os.path.exists(f"{path}"):
                creds = Credentials.from_authorized_user_file(f"{path}", scopes)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        f"{path}", scopes
                    )
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(f"{path}", "w") as token:
                    token.write(creds.to_json())
            # Call the original function with the obtained credentials
            return func(creds, *args, **kwargs)
        return wrapper
    return decorator


def normalize_phrase(phrase: string) -> string:
    """
    :param phrase: string to have check accents removed
    :return: same phrase without accents and in lower case.
    :example:
        >>> normalize_phrase('ÁáÀàÂâÉéÈèÊêÍíÌìÓóÒòÔôÕõÚúÙù')
        'aaaaeeeeiiiooooouuuu'
        >>> normalize_phrase('ÁáÀàÂâÉéÈèÊêÍíÌìÓóÒòÔôÕõÚúÙù') == normalize_phrase('ÁáÀàÂâÉéÈèÊêÍíÌìÓóÒòÔôÕõÚúÙù')
        True
    """
    if isinstance(phrase, str):
        # phrase = remove_punctuation(phrase)
        return ''.join(x for x in unicodedata.normalize('NFKD', phrase)
                       if x in string.whitespace or x in string.printable).casefold()
    else:
        return phrase


def remove_punctuation(phrase: string) -> string:
    """
    :param phrase: string to have check punctuation removed
    :return: same phrase without punctuation
    """
    if isinstance(phrase, str):
        return (phrase.translate(str.maketrans('', '', string.punctuation))).strip()
    else:
        return phrase


def select_folder(path: str) -> str:
    """
    :param path: path_current to folder
    :return: name of selected folder in path_current
    """
    folders = [f.name for f in os.scandir(path) if f.is_dir()]
    [print(fr"[{i}] - {folder}") for i, folder in enumerate(folders)]
    while True:
        try:
            selector = input("Select one folder:\n")
            return folders[int(selector)]
        except ValueError:
            print("Invalid text. Please try again.\n")
            pass


def select_file(path: str, extension: str = '.csv') -> list:
    """
    :param path: path_current to folder with files
    :return: name of selected file in path_current
    """
    files = [f for f in pathlib.Path(path).glob(f"*{extension}")]
    [print(fr"[{i}] - {folder}") for i, folder in enumerate(files)]
    selector = input("Select one file, or [A]ll:\n").casefold()
    if selector == 'a':
        return files
    else:
        return [files[int(selector)]]


def get_deliveries(filepath: str, first_stop: list = None, last_stop: list = None) -> list:
    # Check headers:
    mandatory_headers = ["latitude", "longitude", "receiver_name", "receiver_street", "receiver_number",
                         "receiver_complement", "receiver_city", "receiver_state", "receiver_cep", "receiver_id",
                         'sender_id']
    optional_headers = ["receiver_neighborhood", "order_number", "nfe_number", "nfe_series", "nfe_key",
                        "package_value", "package_quantity", "package_weight"]

    # Open deliveries file
    while True:
        with open(rf'{filepath}', 'r', encoding='UTF-8') as f:
            reader = csv.DictReader(f)
            entregas = [row for row in reader]
        missing_headers = []
        if len(entregas) == 0:
            break
        for key in mandatory_headers:
            if key not in entregas[0].keys():
                missing_headers.append(key)
        if len(missing_headers) > 0:
            print(f'Following headers need to be renamed or added.')
            [print(header) for header in missing_headers]

            print(f'\nExpected headers are:\n')
            [print(header) for header in mandatory_headers]

            print(f'Please edit the file and press enter to continue.\n')
            input()
        else:
            break

    print(f'File opened successfully')
    if last_stop:
        [entregas.insert(0, stop) for stop in last_stop]
    if first_stop:
        [entregas.insert(0, stop) for stop in first_stop]

    return entregas


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


def regex_lube(string: str) -> str:
    """
    Replaces check non-alphanumeric characters with 'µ' character
    Removes new lines
    :param string: string to be formatted
    :return: formatted string
    """
    #Remove accents:
    normalized = normalize_phrase(string).casefold()

    #Replace non alphanumeric chars (avoiding spaces and URL chars):
    alphanumeric = "".join([re.sub(r'[^a-zA-Z0-9\s]', '*', char, re.IGNORECASE) for char in normalized])

    #Remove new lines:
    oneline = clean_newlines(alphanumeric)

    #Trim around '*':
    lubed = re.sub(r'\s*\*\s*', '*', oneline)

    return lubed


def clean_numbers(string):
    return re.sub('[^0-9]', '', string)


def clean_newlines(string):
    return re.sub('\n', '', string)


def process_xml(xml: bytes) -> dict:
    xml_dict = xmltodict.parse(xml)

    # NFe info:
    if xml_dict.get("nfeProc").get("NFe").get("infNFe").get("compra"):
        nfe_order_number = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("compra").get("xPed", "")
    else:
        nfe_order_number = "sem numero de pedido"
    nfe_number = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("ide").get("nNF", "", )
    nfe_series = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("ide").get("serie", "", )
    nfe_operation = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('ide').get("finNFe", "", )
    nfe_emission_date = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("ide").get("dhEmi", "", )
    nfe_key = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("@Id", "", )[3:]
    nfe_value = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("total").get("ICMSTot").get("vNF", '')
    nfe_value = re.sub(',', '.', nfe_value)

    # Sender (Emitente) info:
    sender_name = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("xNome", "", )
    sender_id = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("CNPJ", "", )
    sender_ie = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("IE", "", )
    sender_im = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("IM", "", )
    sender_cnae = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("CNAE", "", )
    sender_street = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("enderEmit").get("xLgr", "")
    sender_number = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("enderEmit").get("nro", "")
    sender_complement = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("enderEmit").get("xCpl", "")
    sender_neighborhood = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("enderEmit").get("xBairro", "")
    sender_city = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("enderEmit").get("xMun", "")
    sender_state = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("enderEmit").get("UF", "")
    sender_cep = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("enderEmit").get("CEP", "")
    sender_phone = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("fone", "")
    sender_email = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('emit').get("enderEmit").get("Email", "")

    # Delivery
    delivery = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("entrega", None, )
    if delivery:
        delivery_name = delivery.get("xNome", "")
        delivery_id = delivery.get("CNPJ", "")
        delivery_ie = delivery.get("IE", "")
        delivery_street = delivery.get("xLgr", "")
        delivery_number = delivery.get("nro", "")
        delivery_complement = delivery.get("xCpl", "")
        delivery_neighborhood = delivery.get("xBairro", "")
        delivery_city = delivery.get("xMun", "")
        delivery_state = delivery.get("UF", "")
        delivery_cep = delivery.get("CEP", "")
        delivery_email = delivery.get("Email", "")
        delivery_phone = delivery.get("fone", "")
    else:
        delivery_name = delivery_street = delivery_number = delivery_complement = delivery_city = delivery_state = delivery_cep = delivery_id = delivery_ie = delivery_neighborhood = delivery_email = delivery_phone = ''

    # Recipient (destinatário)
    recipient_name = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("dest").get("xNome", "", )
    recipient_id = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("dest").get("CNPJ", "", )
    recipient_ie = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("dest").get("IE", "", )
    recipient_street = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("dest").get('enderDest').get("xLgr", "", )
    recipient_number = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("dest").get('enderDest').get("nro", "", )
    recipient_complement = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("dest").get('enderDest').get("xCpl",
                                                                                                             "", )
    recipient_city = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("dest").get('enderDest').get("xMun", "", )
    recipient_state = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("dest").get('enderDest').get("UF", "", )
    recipient_cep = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("dest").get('enderDest').get("CEP", "", )
    recipient_neighborhood = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("dest").get('enderDest').get(
        "xBairro", "", )
    recipient_phone = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("dest").get('enderDest').get("fone", "", )
    recipient_email = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("dest").get("email", "", )

    # Product:
    product_list = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("det")
    if not isinstance(product_list, list):
        product_list = [product_list]

    products = []
    for product in product_list:
        product_name = product.get("prod").get("xProd", "", )
        product_code = product.get("prod").get("cProd", "", )
        product_amount = product.get("prod").get("qCom", "", )
        product_value = product.get("prod").get("vProd", "", )
        product_netweight = product.get("prod").get("pesoL", "", )
        product_grossweight = product.get("prod").get("pesoB", "", )
        product_cfop = product.get("prod").get("CFOP", "", )
        products.append({
            "product_code": product_code,
            "product_name": product_name,
            "product_amount": product_amount,
            "product_value": product_value,
            "product_netweight": product_netweight,
            "product_grossweight": product_grossweight,
            "product_cfop": product_cfop,
        })

    # Freight (Transporte)
    freight_price = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("total").get("ICMSTot").get("vFrete", "", )
    freight_taxes = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("total").get("ICMSTot").get("vTotTrib", "", )

    volumes = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("transp").get("vol", None)
    items_list = xml_dict.get("nfeProc").get("NFe").get("infNFe").get('det')

    freight_volumes = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("transp").get("vol").get('qVol', "")
    freight_volumes_identification = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("transp").get("vol").get('nVol', "")
    freight_netweight = volumes.get("pesoL", '', )
    freight_grossweight = volumes.get("pesoB", '', )
    freight_weight = max(freight_netweight, freight_grossweight)

    # Misc
    notes = xml_dict.get("nfeProc").get("NFe").get("infNFe").get("infAdic").get("infCpl", "", )

    return {
        "nfe_order_number": nfe_order_number,
        "nfe_number": nfe_number,
        "nfe_series": nfe_series,
        "nfe_key": nfe_key,
        "nfe_operation": nfe_operation,
        "nfe_value": nfe_value,
        "nfe_emission_date": nfe_emission_date,
        "sender_name": sender_name,
        "sender_id": sender_id,
        "sender_ie": sender_ie,
        "sender_im": sender_im,
        "sender_cnae": sender_cnae,
        "sender_street": sender_street,
        "sender_number": sender_number,
        "sender_complement": sender_complement,
        "sender_city": sender_city,
        "sender_state": sender_state,
        "sender_cep": sender_cep,
        "sender_neighborhood": sender_neighborhood,
        "sender_email": sender_email,
        "sender_phone": sender_phone,
        "delivery_name": delivery_name,
        "delivery_street": delivery_street,
        "delivery_number": delivery_number,
        "delivery_complement": delivery_complement,
        "delivery_city": delivery_city,
        "delivery_state": delivery_state,
        "delivery_cep": delivery_cep,
        "delivery_id": delivery_id,
        "delivery_ie": delivery_ie,
        "delivery_neighborhood": delivery_neighborhood,
        "delivery_email": delivery_email,
        "delivery_phone": delivery_phone,
        "recipient_name": recipient_name,
        "recipient_id": recipient_id,
        "recipient_ie": recipient_ie,
        "recipient_street": recipient_street,
        "recipient_number": recipient_number,
        "recipient_complement": recipient_complement,
        "recipient_city": recipient_city,
        "recipient_state": recipient_state,
        "recipient_cep": recipient_cep,
        "recipient_neighborhood": recipient_neighborhood,
        "recipient_phone": recipient_phone,
        "recipient_email": recipient_email,
        "products": products,
        "freight_price": freight_price,
        "freight_volumes": freight_volumes,
        "freight_volumes_identification": freight_volumes_identification,
        "freight_netweight": freight_netweight,
        "freight_grossweight": freight_grossweight,
        "freight_weight": freight_weight,
        "freight_taxes": freight_taxes,
        "notes": notes,
    }


def is_rodizio(address: dict) -> bool:
    location = Point(address["longitude"], address["latitude"])
    polygon = Polygon(config.rodizio_polygon['geometry'][0])
    return polygon.contains(location)


def update_clientes_db(address: dict) -> None:
    # address keys from maps_api: "street", "number", "neighborhood", "city", "state", "country", "cep", "rodizio"

    columns = [
        "latitude",
        "longitude",
        "entrega_name",
        "entrega_street",
        "entrega_number",
        "entrega_complement",
        "entrega_city",
        "entrega_state",
        "entrega_cep",
        "entrega_id",
        "entrega_neighborhood",
        "entrega_email",
        "entrega_phone",
        "sender_id",
        "sender_name",
        "inscricao_estadual",
        "nfe_number",
        "email_id",
        "rodizio"
    ]
    # Start clients dataframe
    data = get_values("1byswz40H5vx-6y8QLVSsvlgKud7aemYPTRdRA1uoh5o", "A1:P")
    df_volumes = pd.DataFrame(data[1:], columns=data[0])

    # Create df for new address:
    df_new_address = pd.DataFrame.from_dict(address, orient='index').T
    # Concatenate it:
    new_df_volumes = pd.concat([df_volumes, df_new_address]).reset_index(drop=True).drop_duplicates(subset=['entrega_id'], keep='last')

    # Append to Sheets
    values = new_df_volumes.fillna('').values.tolist()
    values.insert(0, columns)
    update_values(spreadsheet_id='1byswz40H5vx-6y8QLVSsvlgKud7aemYPTRdRA1uoh5o',
                  range_name="volumes",
                  values=values)
    return


def retry_on_failure(max_attempts, retry_delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(max_attempts):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as error:
                    print(f"Error occurred: {error}. Retrying...")
                    time.sleep(retry_delay)
            raise Exception("Maximum attempts exceeded. Function failed.")

        return wrapper

    return decorator


def safe_division(dividend, divisor, zero_division_result=0):
    try:
        return dividend / divisor
    except ZeroDivisionError:
        return zero_division_result


def pin_stops(entregas, m=None):
    """
    @param entregas: dict with keys latitude and longitude
    @param m:  folium map
    @return:
    """
    if m is None:
        m = folium.Map(location=[-22.5, -43.3], zoom_start=11)

    radius = 2

    for location in entregas:
        lat = location["latitude"]
        long = location["longitude"]

        folium.CircleMarker(
            location=[float(lat), float(long)],
            stroke=True,
            color='blue',
            weight=3,
            opacity=1,
            fill=True,
            fillColor='blue',
            fillOpacity=0.8,
            radius=radius,
        ).add_to(m)

    folium.LayerControl().add_to(m)
    m.save(fr"pins_on_map.html")
    webbrowser.open(fr"pins_on_map.html")


# Google APIs
def google_api_auth(path: str, scopes: list):
    """
    Decorator to handle Google API authentication.
    It retrieves and refreshes credentials if necessary,
    storing them for future use.

    Args:
        path (str): Path to the credentials JSON file.
        scopes (list): List of scopes required for the API.

    Returns:
        function: Decorated function with Google API credentials.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            creds = None
            if os.path.exists(f"{path}"):
                creds = Credentials.from_authorized_user_file(f"{path}", scopes)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        f"{path}", scopes
                    )
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(f"{path}", "w") as token:
                    token.write(creds.to_json())
            # Call the original function with the obtained credentials
            return func(creds, *args, **kwargs)
        return wrapper
    return decorator

# Google Drive
@google_api_auth(path=config.drive_path, scopes=config.drive_scopes)
def upload_with_conversion(creds, file_path, folder_id="", file_id="", save_name=""):
    """Upload file with conversion
    Returns: ID of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    if save_name == "":
        save_name = os.path.basename(file_path)

    extension = file_path.split(".")[-1].casefold()

    if extension in ["xls", "xlsx"]:  # EXCEL
        mime_type = "application/vnd.ms-excel"
    elif extension == "csv":  # CSV
        mime_type = "text/csv"
    else:
        print("File extension not supported.")
        return None

    retry = 0
    while True:
        try:
            # create drive api client
            service = build("drive", "v3", credentials=creds)

            file_metadata = {
                "name": save_name,
                "mimeType": "application/vnd.google-apps.spreadsheet",
                "parents": [folder_id]
            }
            media_body = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
            # pylint: disable=maybe-no-member
            if file_id == "":
                file = (
                    service.files()
                    .create(body=file_metadata, media_body=media_body, fields="id")
                    .execute()
                )
            else:
                file = (
                    service.files()
                    .update(
                        fileId=file_id,
                        body=None,
                        media_body=media_body,
                        fields="id",
                    )
                    .execute()
                )
            if file.get("id"):
                print(f'File {save_name}" has been uploaded.')
                break

        except (HttpError, FileNotFoundError) as error:
            print(f"An error occurred: {error}")
            if retry < 10:
                sleep(1)
                retry += 1
                pass
            else:
                tryagain = input("try again?")
                if tryagain.lower() == "y":
                    pass
                else:
                    return None

    return file.get("id")


@google_api_auth(path=config.drive_path, scopes=config.drive_scopes)
def copy_file(creds, file_id: str, copy_name: str, folder_id: str = None):
    """Upload file with conversion
    Returns: ID of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    retry = 0
    while True:
        try:
            # create drive api client
            service = build("drive", "v3", credentials=creds)

            file_metadata = {
                "name": copy_name,
                "mimeType": "application/vnd.google-apps.spreadsheet",
                "parents": [folder_id]
            }
            # pylint: disable=maybe-no-member
            file = (
                service.files()
                .copy(fileId=file_id, body=file_metadata)
                .execute()
            )
            if file.get("id"):
                file_id = file.get("id")
                print(f'The copy {copy_name}/{file.get("title")} has been created.')
                break

        except (HttpError, FileNotFoundError) as error:
            print(f"An error occurred: {error}")
            if retry < 10:
                sleep(1)
                retry += 1
                pass
            else:
                tryagain = input("try again?")
                if tryagain.lower() == "y":
                    pass
                else:
                    return None

    # Retrieve the existing parents to remove
    try:
        previous_parents = ",".join(file.get('parents'))
    except Exception:
        previous_parents = ''

    # Move the file to the new folder
    service.files().update(
        fileId=file_id,
        addParents=folder_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()

    return file_id


# Gmail
@retry_on_failure(max_attempts=3, retry_delay=2)
@google_api_auth(path=config.gmail_path, scopes=config.gmail_scopes)
def list_emails(creds, label_id: str = None, user: str = "me", q: str = None) -> list[dict]:
    """
    Lists email IDs as per the query.
    """
    next_page_token = None
    emails = []
    try:
        while True:
            # Call the Gmail API
            service = build("gmail", "v1", credentials=creds)
            results = service.users().messages().list(userId=user, labelIds=label_id, pageToken=next_page_token,
                                                      q=q).execute()
            emails.extend(results.get("messages", []))
            next_page_token = results.get("nextPageToken")
            if next_page_token is None:
                break

        return emails

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


@google_api_auth(path=config.gmail_path, scopes=config.gmail_scopes)
@retry_on_failure(max_attempts=3, retry_delay=2)
def get_email_content(creds, msg_id: str) -> tuple[str, str | None, dict[str, dict[str, str]]] | tuple[None, None, None]:
    def extract_text(body):
        soup = BeautifulSoup(body, 'html.parser')
        # kill check script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        text = text.replace('\n', ' ')
        text = text.replace('\xa0', ' ')

        # return unicodedata.normalize('NFC', text)
        return text

    try:
        service = build("gmail", "v1", credentials=creds)

        message = service.users().messages().get(userId="me", id=msg_id, format='full').execute()

        subject = "No Subject"
        for header in message["payload"]["headers"]:
            if header["name"] == "Subject":
                subject = str(header["value"])

        # get body data
        try:
            b64_body = message["payload"]["body"]["data"]
            decoded_body = base64.urlsafe_b64decode(b64_body)
            body = extract_text(decoded_body)
        except KeyError:
            body = None

        # get attachment ids
        attachment_ids = {}
        try:
            parts = message["payload"]["parts"]
            for part in parts:
                if len(part["filename"]) >= 5:
                    filename: str = part["filename"].casefold()
                    attachment_id: str = part["body"]["attachmentId"]
                    extension: str = filename.split('.')[-1]
                    attachment_ids.update({extension: {"filename": filename, "attachment_id": attachment_id}})
        # No attachment
        except KeyError:
            pass

        return subject, body, attachment_ids

    except UnicodeEncodeError:
        print("UnicodeEncodeError")
        return None, None, None

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

    except TimeoutError:
        return None, None, None


@google_api_auth(path=config.gmail_path, scopes=config.gmail_scopes)
@retry_on_failure(max_attempts=3, retry_delay=2)
def modify_label(creds, msg_id: str, user: str = "me", label_id_remove: str | list = None, label_id_add: str | list = None):
    if type(label_id_remove) is not list:
        label_id_remove = [label_id_remove]
    if type(label_id_add) is not list:
        label_id_add = [label_id_add]
    body = {
        "addLabelIds": label_id_add,
        "removeLabelIds": label_id_remove
    }
    try:
        service = build("gmail", "v1", credentials=creds)
        service.users().messages().modify(userId=user, id=msg_id, body=body).execute()
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


@google_api_auth(path=config.gmail_path, scopes=config.gmail_scopes)
@retry_on_failure(max_attempts=3, retry_delay=2)
def get_attachments(creds, msg_id: str, attachment_id: str, save_path: str = None, user: str = "me",
                    filename: str = 'untitled', download: bool = True, return_filecontent: bool = True) -> bytes | None:
    """"
    Gets email attachment
    Params:
        msg_id: email id
        attachment_id: attachment id
        user: user id
    """
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().attachments().get(userId=user, messageId=msg_id,
                                                               id=attachment_id).execute()

        if save_path and not os.path.exists(save_path):
            os.makedirs(save_path)

        file_base_64 = results["data"]
        bytes_file_content: bytes = base64.urlsafe_b64decode(file_base_64)

        if download:
            with open(fr'{save_path}\{filename}', 'wb') as file:
                file.write(bytes_file_content)

        if return_filecontent:
            return bytes_file_content

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


# Google Maps
def geocoding(address: str) -> dict:
    """ Returns lat, long and formated address based on a text address"""
    gmaps = googlemaps.Client(key=config.google_api_key)

    result: list[dict] = gmaps.geocode(address)
    geocode_dict = {}
    if not result:
        pass
    else:
        for component in result[0]['address_components']:
            for attribute in component["types"]:
                geocode_dict.update({f"{attribute}_long": component.get("long_name", ""),
                                     f"{attribute}_short": component.get("short_name", "")})
        geocode_dict["latitude"] = result[0]['geometry']['location']['lat']
        geocode_dict["longitude"] = result[0]['geometry']['location']['lng']
        geocode_dict["rodizio"] = is_rodizio(address=geocode_dict)

    new_keys = ["street", "number", "neighborhood", "city", "state", "country", "cep"]
    old_keys = ["route_long", "street_number_long", "sublocality_level_1_long", "administrative_area_level_2_long",
                "administrative_area_level_1_short", "country_short", "postal_code_long"]
    old_keys_alt = ["route_short", "street_number_short", "sublocality_level_1_short",
                    "administrative_area_level_2_short", "administrative_area_level_1_long", "country_long",
                    "postal_code_short"]

    address_as_list = address.split(",")
    for new_key, old_key, old_key_alt in zip(new_keys, old_keys, old_keys_alt):
        if geocode_dict.get(old_key) is not None:
            geocode_dict[new_key] = geocode_dict.pop(old_key)
        elif geocode_dict.get(old_key_alt) is not None:
            geocode_dict[new_key] = geocode_dict.pop(old_key_alt)
        else:
            try:
                match new_key:
                    case "street":
                        geocode_dict[new_key] = address_as_list[0]
                    case "number":
                        geocode_dict[new_key] = address_as_list[1]
                    case "neighborhood":
                        geocode_dict[new_key] = address_as_list[2]
                    case "city":
                        geocode_dict[new_key] = address_as_list[3]
                    case "state":
                        geocode_dict[new_key] = address_as_list[4]
                    case "country":
                        geocode_dict[new_key] = address_as_list[5]
                    case "cep":
                        geocode_dict[new_key] = address_as_list[6]
            except IndexError:
                print(f"Erro em {address=}; {address_as_list=}")
                pass

    update_clientes_db(address=geocode_dict)

    return geocode_dict


def directions(origin, destination, waypoints):
    gmaps = googlemaps.Client(key=config.google_api_key)

    results = gmaps.directions(origin, destination, waypoints=waypoints, mode='driving', alternatives=False, avoid=None,
                               language=None, units='metric', region='br', departure_time=None, arrival_time=None,
                               optimize_waypoints=True, transit_mode=None, transit_routing_preference=None,
                               traffic_model=None)
    distance = results[0]['legs'][0]['distance']['value']
    duration = results[0]['legs'][0]['duration']['value']
    polyline = results[0]['overview_polyline']['points']
    sequence: list[int] = results[0]['waypoint_order']
    return distance, duration, polyline, sequence


# Sheets
@google_api_auth(path=config.sheets_path, scopes=config.sheets_scopes)
def get_values(creds, spreadsheet_id, range_name) -> HttpError | Any:
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    try:
        service = build("sheets", "v4", credentials=creds)

        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        rows = result.get("values", [])
        # print(f"{len(rows)} rows retrieved")
        return rows
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


@google_api_auth(path=config.sheets_path, scopes=config.sheets_scopes)
def append_values(creds, spreadsheet_id, range_name, values, value_input_option='USER_ENTERED'):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    try:
        service = build("sheets", "v4", credentials=creds)

        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        # print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


@google_api_auth(path=config.sheets_path, scopes=config.sheets_scopes)
def update_values(creds, spreadsheet_id, range_name, values, value_input_option='USER_ENTERED'):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    try:
        service = build("sheets", "v4", credentials=creds)
        values = values
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        # print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


# DB Functions
# def update_frete(data: dict, file_path: str = config.fretes_db_path) -> str:
#     """
#     Código de Status
#
#         1 Arquivo Recebido
#         6 A caminho do destinatário
#         2 Entregue
#         3 Em Rota
#         18 Geração de lista
#
#     @param data: retorno do webhook da tracker
#         {
#           "data_hora_envio": "01/03/2024 15:21:19",
#           "cnpj_transportadora": "89516147000142",
#           "cnpj_embarcador": "05517785000198",
#           "data_prevista": "01/03/2024",
#           "data_agendamento": "01/03/2024",
#           "encomenda": "22558899",
#           "nota_fiscal": {
#             "numero": "987654321",
#             "serie": "1",
#             "chave": "11112222333344445555666677778888999933335555",
#             "pedido": "PED123456"
#           },
#           "recebedor": {
#             "tipo": "PORTEIRO",
#             "nome": "JOÃO DA SILVA",
#             "documento": {
#               "tipo": "OUTROS",
#               "numero": "123465789X"
#             }
#           },
#           "motorista": {
#             "cpf": "99944455588",
#             "nome": "JOSÉ SILVA",
#             "placa": "ABH-1A99"
#           },
#           "ocorrencia": {
#             "codigo": "03",
#             "descricao": "Entregue",
#             "data": "01/03/2024 15:21:19",
#             "observacao": "Entregue",
#             "comprovante": {
#               "caminho": "https://tmstransportador.blob.core.windows.net/comprovante/1.jpg"
#             },
#             "assinatura": {
#               "caminho": "https://tmstransportador.blob.core.windows.net/assinatura/1.jpg"
#             },
#             "latitude": -23.49532,
#             "longitude": -46.84704
#           }
#         }
#
#     @return:nothing
#     :param file_path:
#     """
#
#     try:
#         data_flattened = {
#             'cnpj_embarcador': data.get("cnpj_embarcador"),
#             'data_prevista': data.get("data_prevista"),
#             'data_agendamento': data.get("data_agendamento"),
#             'encomenda': data.get("encomenda"),
#             'nota_fiscal_numero': data.get("nota_fiscal").get("numero", ""),
#             'nota_fiscal_serie': data.get("nota_fiscal").get("serie", ""),
#             'nota_fiscal_chave': data.get("nota_fiscal").get("chave", ""),
#             'nota_fiscal_pedido': data.get("nota_fiscal").get("pedido", ""),
#             'recebedor_tipo': data.get("recebedor").get("tipo", ""),
#             'recebedor_nome': data.get("recebedor").get("nome", ""),
#             'recebedor_documento_tipo': data.get("recebedor").get("documento").get("tipo", ""),
#             'recebedor_documento_numero': data.get("recebedor").get("documento").get("numero", ""),
#             'motorista_cpf': data.get("motorista").get("cpf", ""),
#             'motorista_nome': data.get("motorista").get("nome", ""),
#             'motorista_placa': data.get("motorista").get("placa", ""),
#             'ocorrencia_codigo': data.get("ocorrencia").get("codigo", ""),
#             'ocorrencia_descricao': data.get("ocorrencia").get("descricao", ""),
#             'ocorrencia_data': data.get("ocorrencia").get("data", ""),
#             'ocorrencia_observacao': data.get("ocorrencia").get("observacao", ""),
#             'ocorrencia_comprovante_caminho': data.get("ocorrencia").get("comprovante").get("caminho", ""),
#             'ocorrencia_assinatura_caminho': data.get("ocorrencia").get("assinatura").get("caminho", ""),
#             'latitude': data.get("latitude"),
#             'longitude': data.get("longitude"),
#         }
#
#         con = sqlite3.connect(file_path)
#         cur = con.cursor()
#
#         columns_to_update = ", ".join([column for column in data_flattened.keys() if data_flattened[column] not in ["", None]])
#         values_to_update = ", ".join([f"'{data_flattened[column]}'" for column in data_flattened.keys() if data_flattened[column] not in ["", None]])
#         on_conflict_to_update = ", ".join([f"{column}=excluded.{column}" for column in data_flattened.keys() if data_flattened[column] not in ["", None]])
#
#         query_fretes = (
#             f"INSERT INTO Fretes ({columns_to_update})"
#             f"VALUES ({values_to_update})"
#             " ON CONFLICT (encomenda) DO "
#             f"UPDATE SET {on_conflict_to_update}")
#
#         query_ocorrencias = (
#             f"INSERT INTO Ocorrencias (ocorrencia_codigo, ocorrencia_descricao) "
#             f"VALUES (\'{data_flattened['ocorrencia_codigo']}\', \'{data_flattened['ocorrencia_descricao']}\') "
#             f"ON CONFLICT (ocorrencia_codigo) DO NOTHING;")
#
#         cur.execute(query_ocorrencias)
#         cur.execute(query_fretes)
#
#         con.commit()
#         return 'commited'
#     except Exception as e:
#         return str(e)
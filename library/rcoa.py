import datetime
import requests
from bs4 import BeautifulSoup

ROAC_HOST = "https://lifelong.rcoa.ac.uk"
LOGIN_URL = f"{ROAC_HOST}/login"
LOGBOOK_EXPORT_URL = f"{ROAC_HOST}/logbook/export"
LOGBOOK_REFRESH_URL = f"{ROAC_HOST}/logbook/refresh"
ACCOUNT_URL = f"{ROAC_HOST}/account"


def create_rcoa_session(username, password):
    session = requests.Session()

    login_page = session.get(LOGIN_URL)
    content = login_page.content

    soup = BeautifulSoup(content, "html.parser")
    input_element = soup.find_all("input")
    token_element = [e for e in input_element if e.get("name") == "_token"][0]
    token = token_element.get("value")
    if token_element is None:
        raise Exception("Failed to login")

    response = session.post(LOGIN_URL, data={"email": username, "password": password, "_token": token})

    if response.status_code >= 400:
        raise response.raise_for_status()

    return session


def download_logbook(session:requests.Session):

    export = session.get(LOGBOOK_EXPORT_URL)
    content = export.content

    file_details_header = export.headers.get("Content-Disposition")
    if file_details_header and "filename=" in file_details_header:
        filename = file_details_header.split("filename=")[1]
    elif b"Generating" in content:
        filename = f"still_generating_{datetime.datetime.now():%Y-%m-%dT%H%M%S}.txt"
        content = f"Still generating logbook export: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
    else:
        filename = f"failed_download_{datetime.datetime.now():%Y-%m-%dT%H%M%S}.html"

    return filename, content


def refresh_logbook(session:requests.Session):

    response = session.get(LOGBOOK_REFRESH_URL)
    content = response.content

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        return str(e)
    else:
        return None

def get_account_details(session:requests.Session):

    response = session.get(ACCOUNT_URL)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")

    main_section = soup.find(id="main-content")
    account_section = main_section.find_all(name="section")[0]
    html_content = str(account_section)

    return html_content

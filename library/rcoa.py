import requests
from bs4 import BeautifulSoup

ROAC_HOST = "https://lifelong.rcoa.ac.uk"
LOGIN_URL = f"{ROAC_HOST}/login"
LOGBOOK_EXPORT_URL = f"{ROAC_HOST}/logbook/export"
LOGBOOK_REFRESH_URL = f"{ROAC_HOST}/logbook/refresh"


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
    filename = export.headers.get("Content-Disposition").split("filename=")[1]
    return filename, export.content


def refresh_logbook(session:requests.Session):

    session.post(LOGBOOK_REFRESH_URL)

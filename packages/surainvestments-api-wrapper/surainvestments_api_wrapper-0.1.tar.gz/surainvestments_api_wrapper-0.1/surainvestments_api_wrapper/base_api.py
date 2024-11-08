import requests
import logging
from datetime import datetime

API_URL = "https://investment.sura.com.uy/api"
logging.basicConfig(level=logging.DEBUG)


class BaseAPI:
    def __init__(self, document, country, document_type, password, verify_ssl=False):
        # Crear una sesión de requests y deshabilitar SSL si es necesario
        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.session.trust_env = False
        self.token = None
        logging.debug("Iniciando sesión en la API de Sura")
        self.login(document, country, document_type, password)

    def login(self, document, country, document_type, password):
        login_url = f"{API_URL}/Auth/login"
        credentials = {
            "document": document,
            "country": country,
            "documentType": document_type,
            "password": password
        }

        # Realizar la solicitud de login
        response = self.session.post(login_url, data=credentials)
        response_data = response.json()

        logging.debug(f"Respuesta de login: {response_data}")

        if response_data.get("authenticationSuccessful") and "token" in response_data:
            self.token = response_data["token"]
            logging.debug(f"Token de autenticación recibido y configurado: {self.token}")
        else:
            logging.error("Error en la autenticación: Login fallido")
            raise Exception("Login failed")

    def get_auth_headers(self):
        if not self.token:
            raise Exception("Token is not available. Login first.")
        # Construir los encabezados de autorización usando el token
        return {"Token": f"{self.token}"}

    def perform_get_request(self, url, headers=None, params=None):
        logging.debug(f"Realizando solicitud GET a {url} con encabezados {headers} y parámetros {params}")

        response = self.session.get(url, headers=headers, params=params)
        logging.debug(f"Respuesta: {response.status_code} - {response.text}")

        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Error en solicitud GET: {response.status_code}")
            raise Exception(f"Failed to perform GET request: {response.status_code}")

    # Luego, modifica las funciones para usar `perform_get_request`

    def get_gadget_info(self):
        url = f"{API_URL}/cbs/GetGadgetInfo"
        headers = self.get_auth_headers()
        return self.perform_get_request(url, headers=headers)

    def get_nominal_balance_by_last_year(self, account_number, first_date, last_date, tab_id):
        url = f"{API_URL}/cbs/GetNominalBalanceByLastYear"
        headers = self.get_auth_headers()
        params = {
            "accountNumber": account_number,
            "firstDate": first_date,
            "lastDate": last_date,
            "tabId": tab_id
        }
        return self.perform_get_request(url, headers=headers, params=params)

    def get_statements(self, start_date, end_date):
        url = f"{API_URL}/Cbs/GetStatements"
        headers = self.get_auth_headers()
        params = {
            "startDate": start_date,
            "endDate": end_date
        }
        return self.perform_get_request(url, headers=headers, params=params)

    def get_investment_position(self, first_date, account_number=None, last_date=None, tab_id="4911612639"):
        url = f"{API_URL}/cbs/GetInvestmentPosition"
        params = {
            "firstDate": first_date,
            "tabId": tab_id,
            "lastDate": last_date or datetime.now().isoformat()
        }
        if account_number is not None:
            params["accountNumber"] = account_number

        headers = self.get_auth_headers()
        return self.perform_get_request(url, headers=headers, params=params)

    def get_total_account(self):
        try:
            gadget_info = self.get_gadget_info()
            total_balance = sum(instrument['balance'] for instrument in gadget_info['instruments'])
            return total_balance
        except Exception as e:
            logging.error(f"Error al calcular el balance total de la cuenta: {e}")
            raise


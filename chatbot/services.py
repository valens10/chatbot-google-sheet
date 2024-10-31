import os
import gspread
from typing import List, Optional, Dict
import logging
from gspread.exceptions import SpreadsheetNotFound
from django.conf import settings


# Configure the logger
logger = logging.getLogger(__name__)
BASE_URL = os.getenv("BASE_URL")
def initialize_gspread() -> gspread.client.Client:
  """
  Initialize a gspread client with the given credentials.
  """
  return gspread.service_account_from_dict(get_credentials())

def get_credentials() -> dict:
  """
  Return gspread credentials.
  """
  return {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
  }

def fetch_data_from_google_sheet(doc_name: str, sheet_name: Optional[str] = None) -> List[dict]:
    """
    Fetches all rows from a given Google Sheet worksheet.
    Returns an empty list if an error occurs.
    """
    try:
        # Attempt to open the Google Sheet by name
        sh = settings.GSPREAD_CLIENT.open(doc_name)
        # Get the specified worksheet or the first worksheet by default
        worksheet = sh.worksheet(sheet_name) if sheet_name else sh.get_worksheet(0)
        # Return all records from the worksheet
        return worksheet.get_all_records()

    except SpreadsheetNotFound:
        logging.error(f"The Google Sheet '{doc_name}' was not found.")
    except Exception as e:
        logging.error(f"An error occurred while fetching rows: {e}")
    
    # Return an empty list if an error occurs
    return []

def send_user_data_to_api(data: List[Dict]) -> bool:
    """
    Process a list of user data entries using the handle_user_data function.
    Returns True if processing was successful, otherwise False.
    """
    try:
        from chatbot.views import handle_user_data #Standalone
        # Directly call handle_user_data and pass [Simulation of the request]
        response_data = handle_user_data(data)

        if isinstance(response_data, list):
            logger.info('Data processed successfully.')
            return True
        
        else:
            # Log an error if the response isn't as expected
            logger.error(f'Error processing data: {response_data}')
            return False

    except Exception as e:
        # Log any unexpected exceptions
        logger.error(f'Error processing data: {e}')
        return False

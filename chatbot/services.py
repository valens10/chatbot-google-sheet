import os
import gspread
from typing import List, Optional
import logging
from gspread.exceptions import SpreadsheetNotFound
from django.conf import settings

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

def get_all_rows(doc_name: str, sheet_name: Optional[str] = None) -> List[dict]:
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

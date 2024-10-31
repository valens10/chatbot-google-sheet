import logging
import requests
from typing import List, Dict
from celery import shared_task
from chatbot.services import fetch_data_from_google_sheet, send_user_data_to_api

# Configure the logger
logger = logging.getLogger(__name__)

@shared_task
def sync_google_sheet_data(doc_name: str, sheet_name: str):
    """
    Periodically sync data from a Google Sheet to the backend API.
    1. Retrieve data from Google Sheets.
    2. Validate and format data entries.
    3. Send valid data entries as a user to the backend API.
    """
    try:
        #Fetch data from Google Sheets
        logger.info(f'Starting sync for sheet: {sheet_name}, doc_name: {doc_name}')
        data = fetch_data_from_google_sheet(doc_name, sheet_name)
        
        #Validate and format data
        formatted_data = validate_and_format_data(data)
        logger.info(f'Data retrieved')
        
        #Send formatted data to backend API if data is available
        if formatted_data:
            response = send_user_data_to_api(formatted_data)
            if response:
                logger.info(f'Successfully synced user data')
            else:
                logger.error('Failed to sync user data.')
        else:
            logger.warning('No valid data to sync.')

    except Exception as e:
        logger.error(f'An error occurred during data sync: {e}')


def validate_and_format_data(data: List[Dict]) -> List[Dict]:
    valid_entries = []
    
    for entry in data:
        try:
            normalized_entry = normalize_keys(entry)
            if is_valid_entry(normalized_entry):
                formatted_entry = format_entry(normalized_entry)
                valid_entries.append(formatted_entry)
            else:
                logger.warning(f'Skipped invalid entry')
        except Exception as e:
            logger.error(f'Error processing entry: {e}')

    return valid_entries




def is_valid_entry(entry: Dict) -> bool:
    required_fields = ['full_name', 'age', 'gender', 'alcohol_consumption', 
                       'physical_activity_level', 'smoking_status', 'diet_type']
    
    # Ensure all required fields are present and not empty or null
    if not all(field in entry and entry[field] for field in required_fields):
        return False
    return True




def format_entry(entry: Dict) -> Dict:
    formatted_entry = {
        'id': entry.get('id'),
        'full_name': entry.get('full_name'),
        'age': entry.get('age'),
        'gender': entry.get('gender'),
        'alcohol_consumption': entry.get('alcohol_consumption'),
        'physical_activity_level': entry.get('physical_activity_level'),
        'smoking_status': entry.get('smoking_status'),
        'diet_type': entry.get('diet_type'),
    }
    return formatted_entry


def normalize_keys(entry: Dict) -> Dict:
    return {k.lower().replace(' ', '_'): v for k, v in entry.items()}


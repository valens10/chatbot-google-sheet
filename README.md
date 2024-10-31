
# Chatbot Data Integration & API Synchronization

## Project Overview
This project is a Django-based solution for integrating chatbot data with a mock backend API. It retrieves user demographic and lifestyle data from a Google Sheet, processes it, and sends it to an API, which returns user, risk scores for insurance and diabetes. The data is stored on the backend using postgres database for easy future access, with Celery periodically checking for new data.

## Table of Contents
1. [Project Requirements](#project-requirements)
2. [Solution Overview](#solution-overview)
3. [Setup Instructions](#setup-instructions)
4. [Usage](#usage)
5. [Error Handling and Logging](#error-handling-and-logging)
6. [Future Improvements](#future-improvements)

## Project Requirements
The project fulfills the following requirements:
- **Data Retrieval**: Uses a Celery task to fetch new entries from a Google Sheet every 10 seconds and format them for the API.
- **API Communication**: Sets up an endpoint with Django REST Framework to accept user data and generate mock scores.
- **Data Storage**: Implements a Django model to store user data and risk scores for future retrieval.
- **Error Handling & Logging**: Includes error handling and logs interactions with the API.

## Solution Overview

1. **Data Retrieval with Celery**
   A Celery task (`sync_google_sheet_data_every_10_seconds`) runs every 10 seconds to retrieve new entries from the Google Sheet using the Google Sheets API. This task simulates a webhook by continuously updating the database with recent data.

2. **Django REST API Communication**
   A Django REST Framework endpoint (`/api/chatbot/user_data`) accepts user data and generates mock risk scores for insurance risk and diabetes risk. The scores and user data are returned in JSON format.

3. **Data Storage and Retrieval**
   The data and risk scores are stored in a Django model for easy access. This enables future retrieval of user data and the associated risk scores.

4. **Error Handling and Logging**
   Basic error handling is implemented for issues in data retrieval, submission, and database interactions. Logs capture key API interactions and errors.

## Setup Instructions

Basics
- Clone the Project:
    ```bash
     https://github.com/valens10/chatbot-google-sheet.git
     cd chatbot-google-sheet
     git checkout develop
     ```
- Install Redis (required for Celery) if not installed on your system yet
- on ubuntu
    ```bash
     sudo apt install redis-server
     redis-server # run this command to start redis with celery
     ```

1. **Environment Setup**
   - Ensure you have Django, Django REST Framework, redis-server and Celery installed.
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Configure Google Sheets API credentials:
     - Obtain OAuth credentials from Google Cloud Console.
     - Create .env file project directory
     - Place the credentials value in .env file use below template.
        ```bash
        TYPE=service_account
        PROJECT_ID=xxxxxxxxxxx
        PRIVATE_KEY_ID=xxxxxxxxxxx
        PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nxxxxxxxxxxx\n-----END PRIVATE KEY-----\n"
        CLIENT_EMAIL=xxxxxxxxxxx
        CLIENT_ID=xxxxxxxxxxx
        AUTH_URI=https://accounts.google.com/o/oauth2/auth
        TOKEN_URI=https://oauth2.googleapis.com/token
        AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
        CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/xxxxxxxxxxx
        UNIVERSE_DOMAIN=googleapis.com

        BASE_URL=http://localhost:8000
        DOC_NAME=Sample user data
        SHEET_NAME=sheet_1
        REDIS_SERVER=redis://localhost:6379/0
        BD_NAME=db_chatbot
        DB_PASS=admin
        DB_USER=postgres
        DB_PORT=5433
        DB_HOST=localhost
        ```

2. **Database Configuration**
    - Create postgres database and update `env.py`
   - Run migrations to set up the database schema:
     ```bash
     python manage.py migrate
     ```

3. **Running the Project with Celery**
   - Start the project with both Django and Celery using:
     ```bash
     py .\manage.py runserver_with_celery
     ```
   - This command runs the Django server and initializes the Celery worker to fetch data from Google Sheets every 10 seconds.

4. **Google Sheets API Configuration**
   - Ensure your Google Sheet is shared with the API service account.
   - Go to your google sheet and share with `CLIENT_EMAIL` from your google credentials.
   - Add the Document Name(required) and sheet name(optional) to your `.env` file.

## Usage
1. **Fetch Data**  
   - Celery automatically run task and `gspread` retrieves new data entries from the Google Sheet every 10 seconds.

2. **Submit Data to API**
   - Data retrieved from Google Sheets is processed and sent to the `/api/chatbot/user_data` endpoint.

3. **Access Stored Data**
   - Use a GET request to the endpoint `/api/chatbot/get_user_data_scoring_list/` to list stored user scoring data and risk scores.
   - Use a GET request to the endpoint `/api/chatbot/get_single_user_data_scoring/<int:user_id>/` to list stored single user scoring data.

## Error Handling and Logging
- **Error Handling**: Includes error handling for data retrieval, API requests, and database operations.
- **Logging**: Logs all API interactions and errors for traceability.

## Future Improvements
- **Enhanced Error Handling**: Add retries for failed API calls.
- **Webhook Replacement**: Refine the Celery task frequency or explore webhook options for real-time data updates and post data back to the sheet.
- **Enhanced packaging**: Enhance packaging with automation deployment and Docker for containerization.

# Screenshots
- Redis running to your system
  ![image](https://github.com/user-attachments/assets/c7b64515-590e-4b98-bd82-c37ec298e130)
- User data scoring list
   ![image](https://github.com/user-attachments/assets/145914fc-e02d-4168-a025-bb11dc48cce6)
  
- Single-user scoring
![image](https://github.com/user-attachments/assets/8c08ff7a-ba6c-433b-9356-05e784bdba66)

- Google sheet template for user lifestyle and demographics
  ![image](https://github.com/user-attachments/assets/7a9347e8-f737-4ebc-b9ee-79f4ed073975)

- Terminal logs on local machine
![image](https://github.com/user-attachments/assets/a0906031-e544-4873-b85e-7c827b7c92a8)







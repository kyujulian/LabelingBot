from google.oauth2.credentials import Credentials
import os

# Description: This file contains all the constants used in the project

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Spreadsheet config.
SPREADSHEET_ID = '1RH86GGQTkO5yWfFz-l_mrSQXFgdsTk3GSHplfcA3D_k'
SPREADSHEET_PAGE = 'Sheet1'

#directories
DATA_DIR = os.path.join(os.getcwd(), "data")
LOG_DIR = os.path.join(os.getcwd(), "logs")


#dataframe manipulation
LABELED = 'labeled'
ENDTOKEN = "~EOF"


#Data Settings
CLASSES = ["positivo", "negativo", "neutro", "irrelevante"]
TWEETCOL = "Text"
CLASSCOL = "Class"

#General settings
MAXVOTES = 2

#Bot settings
TIMEOUT= 120 #Tempo de expera da votação


CREDS = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    CREDS = Credentials.from_authorized_user_file('token.json', SCOPES)

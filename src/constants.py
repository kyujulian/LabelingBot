from google.oauth2.credentials import Credentials
import os

# Description: This file contains all the constants used in the project

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1DRVXSrhTQDCk3vX93uCMI706GA9It2WGxu-7r6_Bs7o'
SAMPLE_RANGE_NAME = 'A1:B5'

ENDTOKEN = "~EOF"

MAXVOTES = 2

DATA_DIR = os.path.join(os.getcwd(), "data")


LABELED = 'labeled'

#?
TWEETCOL = "Tweet"
CLASSCOL = "class"
#FIX
MAXCOL = 2

CLASSES = ["positivo", "negativo", "neutro", "irrelevante"]

CREDS = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    CREDS = Credentials.from_authorized_user_file('token.json', SCOPES)
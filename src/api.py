# Helpers
from __future__ import print_function

import os.path


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import HTTPError

import pandas as pd
import numpy as np

from utils import initialize_empty_voting

#locals
import constants
import settings


logger = settings.logging.getLogger("api")



class Sheet:

    def __init__(
        self,
        sheet_id,
        range_values
    ):
        self.sheet_id = sheet_id
        try:
            self.load_sheet( sheet_id, range_values)

            self.set_voting()


            self.range = range_values
            self.sheet_id = sheet_id

        except HttpError as err:
            print(err)

    
    def set_voting(self, new=False):
            voting_dir = os.path.join(constants.DATA_DIR, f"voting_id_{self.sheet_id}.csv")
            #checks if voting data already exists
            if os.path.exists(voting_dir) and not new: 
                print("Voting data already exists, loading from file")
                self.vote_data = pd.read_csv(voting_dir)
            
            else:
                self.init_voting_data()
    
    def reload(self, new=False):

        self.load_sheet(self.sheet_id, self.range)
        self.init_voting_data()

    def load_sheet(self, sheet_id, range_values):

            service = build("sheets", "v4", credentials=constants.CREDS)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=sheet_id,
                                        range=range_values).execute()
            read_values = result.get("values", [])

            if not(read_values):
                print("No data found.")
                return

            columns, read_values = read_values[0], read_values[1:]

            #hack to get the right number of columns in the dataframe
            if(len(read_values[0]) < len(columns)):
                read_values[0].append("")




            self.columns = columns
            self.data = pd.DataFrame(columns=columns, data=[val for val in read_values if len(val) > 0])

            self.clean()


    def set_sheet_id(self, id) :
        self.sheet_id = id
        self.reload(new=True)

    def clean(self):
            self.data[constants.CLASSCOL]  = self.data[constants.CLASSCOL].fillna(constants.ENDTOKEN)
            condition = self.data[constants.CLASSCOL].isin(constants.CLASSES) 
            self.data[constants.CLASSCOL] = self.data[constants.CLASSCOL].where(condition, constants.ENDTOKEN)
    

    def init_voting_data(self):
        print("Initializing voting data")
        self.vote_data = self.data.copy()
        self.vote_data = initialize_empty_voting(self.data)
        self.vote_data.to_csv(os.path.join(constants.DATA_DIR, f"voting_id_{self.sheet_id}.csv"), index=False)





            
        
    def add_and_write(self, tweet_index, classification, range_values="Sheet1"):
        #NEEDTOFIXTHIS
        to_replace = self.data[self.data[constants.TWEETCOL] == tweet_index].index
        self.data.loc[to_replace,constants.CLASSCOL] = classification

        self.update_sheet()

    
    def get_unclassified(self, user_position = 0):
        unclass_data = self.get_data_without_class()
        if unclass_data.empty:
            return None

        # wraps around if user_position is greater than the length of the unclassified data
        return unclass_data[constants.TWEETCOL].values[user_position % len(unclass_data)]

    def get_data_without_class(self):
        return self.data.loc[self.data[constants.CLASSCOL] == constants.ENDTOKEN]

    
    def update_sheet(self,data=None,range_values="Sheet1",value_input_option="USER_ENTERED"):

        if (data is None):
            data = self.data
        

        self.update_data = self.data.copy()
        self.update_data.loc[self.data[constants.CLASSCOL] == constants.ENDTOKEN, constants.CLASSCOL] = ""

        values = [self.columns] + self.update_data.to_numpy().tolist()
                
        try:
            service = build('sheets', 'v4', credentials=constants.CREDS)
            body = {
                "values" : values
            }

            result = service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=range_values,
                valueInputOption=value_input_option,
                body=body
            ).execute()
            print('{0} cells updated.'.format(result.get('updatedCells')))
            return result

        except HttpError as error:
            print(f"An error occured: {error}")
            return error


    def vote(self, tweet, className):
        print(f"Voting for {tweet} with {className}")
        self.vote_data.loc[self.vote_data[constants.TWEETCOL] == tweet, className] += 1
        self.vote_data.to_csv(os.path.join(constants.DATA_DIR, f"voting_id_{self.sheet_id}.csv"), index=False)
        
    def check_votes(self, tweet):

        need_update = False
        vote_class = None

        for className in constants.CLASSES:
            element = self.vote_data.loc[self.vote_data[constants.TWEETCOL] == tweet]
            count = element[className].reset_index(drop=True)[0]

            #debug
            #print("Count: \n", count)

            if count >= constants.MAXVOTES:
                vote_class = className
                need_update = True
                break
        
        if(need_update):

            print("setting vote")


            self.data.loc[self.vote_data[constants.TWEETCOL] == tweet, constants.CLASSCOL] = vote_class
            self.vote_data.loc[self.vote_data[constants.TWEETCOL] == tweet, constants.CLASSCOL] = vote_class
            self.vote_data.loc[self.vote_data[constants.TWEETCOL] == tweet, constants.LABELED] = True

            self.vote_data.to_csv(os.path.join(constants.DATA_DIR, f"voting_id_{self.sheet_id}.csv"), index=False)

            self.update_sheet()

            return True

        return False
        
        
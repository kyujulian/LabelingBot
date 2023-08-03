import constants
import numpy as np
import pandas as pd



def get_sheet_id(url):
    url = url.split("/")
    sheet_id = url[3]
    return sheet_id


def initialize_empty_voting(data):
    _classes = np.zeros( shape=(len(data), len(constants.CLASSES)), dtype=int )
    labeled = data[constants.CLASSCOL] != constants.ENDTOKEN
    labeled.name = "labeled"

    columns = constants.CLASSES  
    _classes_df = pd.DataFrame(columns=constants.CLASSES, data=_classes)

    return pd.concat([data, _classes_df,labeled],axis=1)

def update_voting(data, voting_data):
    '''
    This function takes in a dataframe of data and a dataframe of voting data
    For each row in data, if it's not present in voting_data, voting is updated with 
    the row from data
    '''
    column_names = voting_data.columns

    dynamic_default_values = [0, 0, 0, 0, 0, False]
    default_values = dict(zip(column_names[-6:], dynamic_default_values))

    result_df = pd.concat([voting_data, data], ignore_index=True)
    result_df = result_df.drop_duplicates(subset=constants.TWEETCOL, keep="first")
    result_df = result_df.fillna(default_values)

    return result_df
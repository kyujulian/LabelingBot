# from requests import HTTPError
import constants
import numpy as np
import pandas as pd
# import api


def get_sheet_id(url):
    url = url.split("/")
    sheet_id = url[3]
    return sheet_id


def initialize_empty_voting(data):
    _classes = np.zeros( shape=(len(data), len(constants.CLASSES)), dtype=int )
    labeled = data[constants.CLASSCOL] != constants.ENDTOKEN
    labeled.name = "labeled"
    
    print(labeled)
    columns = constants.CLASSES  
    _classes_df = pd.DataFrame(columns=constants.CLASSES, data=_classes)

    return pd.concat([data, _classes_df,labeled],axis=1)
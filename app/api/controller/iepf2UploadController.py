import pandas as pd
from ..model.iepf2UploadModel import IEPF2Model
from dotenv import load_dotenv
import os

load_dotenv()

ACTIVE_ROW_IDENTITY = os.getenv("ACTIVE_ROW_IDENTITY")
VALID_SHEET_NAME = os.getenv("VALID_SHEET_NAME")
MAX_DUPLICATE_ROW = int(os.getenv("MAX_DUPLICATE_ROW"))

class IEPF2Controller:

    db_columns = ["firstname", "middlename", "lastname", "father_firstname", "father_middlename", "father_lastname", "address",
                                        "country", "state", "district", "pincode", "folionumber", "accountnumber", "investmenttype", "amounttransfered",
                                        "proposeddateoftransfer", "pan", "date_of_birth", "aadhar_number", "nominee_name", "joint_holder_name",
                                        "remarks", "investment_under_litigation", "unpaid_suspense_ac", "financial_year", "cin"]
    def __init__(self):
        self.iepf2model = IEPF2Model()

    def insert(self, file_paths):
        results = []
        try:
            for fp in file_paths:
                file_extension = fp.split('.')[-1]
                if file_extension == 'xlsx' or file_extension == 'xls':

                    #Check excel file
                    try:
                        row_a = pd.read_excel(fp, skiprows=0, usecols='A', nrows=MAX_DUPLICATE_ROW, header=None, names=["Value"], sheet_name = VALID_SHEET_NAME)['Value']
                        skip_row = row_a[row_a == ACTIVE_ROW_IDENTITY].index[0]

                        excel_file = pd.ExcelFile(fp)
                        excel_data = excel_file.parse(sheet_name=VALID_SHEET_NAME, skiprows=skip_row)

                        columns = excel_data.columns
                         
                        change_columns = {}
                        for i in range(len(columns)):
                            change_columns[columns[i]] = self.db_columns[i]

                        excel_data.rename(columns = change_columns, inplace = True)
                        excel_data[self.db_columns[15]] = pd.to_datetime(excel_data[self.db_columns[15]])
                        
                        result = self.iepf2model.insert(excel_data)

                        results.append({'file' : fp, 'status' : 'File uploaded successfully', 'data' : result})

                    except (ValueError, IndexError):
                        results.append({'file' : fp, 'status' : 'Invalid file data'})
                        
                    except:
                        results.append({'file' : fp, 'status' : 'Something went wrong!'})

                else:
                    results.append({'file' : fp, 'status' : 'Invalid file type'})
                
            return {'message':'success', 'data':results}   
        except:
            return {'message':'error', 'data':results} 





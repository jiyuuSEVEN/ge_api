import pandas as pd
from ..model.iepf2UploadModel import IEPF2Model
from dotenv import load_dotenv
import os

load_dotenv()

ACTIVE_ROW_IDENTITY = os.getenv("ACTIVE_ROW_IDENTITY")
VALID_SHEET_NAME = os.getenv("VALID_SHEET_NAME")
MAX_DUPLICATE_ROW = int(os.getenv("MAX_DUPLICATE_ROW"))
CIN_ROW = int(os.getenv("CIN_ROW"))
CIN_COLUMN = os.getenv("CIN_COLUMN")

class IEPF2Controller:

    db_columns = ["firstname", "middlename", "lastname", "father_firstname", "father_middlename", "father_lastname", "address",
                                        "country", "state", "district", "pincode", "folionumber", "accountnumber", "investmenttype", "amounttransfered",
                                        "proposeddateoftransfer", "pan", "date_of_birth", "aadhar_number", "nominee_name", "joint_holder_name",
                                        "remarks", "investment_under_litigation", "unpaid_suspense_ac", "financial_year", "cin"]
    
    def __init__(self):
        self.iepf2model = IEPF2Model()

    def insert_excel_log(self, fileName, fileType, userName):
        # Creaet excel log data_frame
        excel_log = pd.DataFrame({
            "excel_name" : [fileName], "type" : fileType, "usertype" : [userName]
        })
        result = self.iepf2model.insert_excel_log(excel_log)
        return result

    def insert_excel_data(self, file_paths, file_type):
        results = []
        # try:
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
                    if(len(columns)>16):
                        excel_data[self.db_columns[17]] = pd.to_datetime(excel_data[self.db_columns[17]])
                    excel_data[self.db_columns[25]] = excel_file.parse(sheet_name=VALID_SHEET_NAME, skiprows=CIN_ROW-1, usecols=CIN_COLUMN, nrows=1, header=None, names=["Value"]).iloc[0]["Value"]

                    result = self.iepf2model.insert_excel_data(excel_data)
                    log_result = self.insert_excel_log(fp.split("/")[-1], file_type, 'admin')
                    processer_result = self.iepf2model.iepf2_processer(fp.split("/")[-1])

                    results.append({'file' : fp, 'status' : 'File uploaded successfully', 'data' : [result, log_result, processer_result.to_dict('list')]})

                except (ValueError, IndexError):
                    results.append({'file' : fp, 'status' : 'Invalid file data'})
                    
                # except:
                #     results.append({'file' : fp, 'status' : 'Something went wrong!'})

            else:
                results.append({'file' : fp, 'status' : 'Invalid file type'})
            
        return {'message':'success', 'data':results}   
        # except:
        #     return {'message':'error', 'data':results} 





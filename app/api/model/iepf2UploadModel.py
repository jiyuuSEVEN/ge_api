from .dbConnection import get_connection
import pandas as pd

class IEPF2Model:
    def __init__(self):
        self.engine = get_connection()

    def insert_excel_data(self, excel_data):
        result = excel_data.to_sql(con=self.engine, name='iepf2', if_exists='append', index=False)
        return result

    def insert_excel_log(self, excel_log):
        result = excel_log.to_sql(con=self.engine, name='excel_log', if_exists='append', index=False)
        return result

    def iepf2_processer(self, fileName):
        query = "call iepf.iepf2_processer('"+fileName+"');"
        result = pd.read_sql_query(query, self.engine)
        return result
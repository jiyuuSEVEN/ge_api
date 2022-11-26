from .dbConnection import get_connection
import pandas as pd

class IEPF2Model:
    def __init__(self):
        self.engine = get_connection()

    def insert_excel_data(self, excel_data, cin):
        query = "SELECT d.id,d.proposed_date,d.dividend_amount,c.cin FROM iepf.dividend_master d JOIN iepf.company_master c ON d.security_code = c.security_code WHERE c.cin = '"+cin+"';"
        dividend_master = pd.read_sql_query(query, self.engine)
        dividend_master['proposed_date'] = pd.to_datetime(dividend_master['proposed_date'])

        excel_data['dividend_count'] = excel_data.apply(lambda row: dividend_master[\
                            (dividend_master['proposed_date'] > row["proposeddateoftransfer_start"]) &\
                            (dividend_master['proposed_date'] < row["proposeddateoftransfer_end"])]['proposed_date'].count(), axis=1)
                            
        result = excel_data.to_sql(con=self.engine, name='iepf2', if_exists='append', index=False)
        return result

    def insert_excel_log(self, excel_log):
        result = excel_log.to_sql(con=self.engine, name='excel_log', if_exists='append', index=False)
        return result

    def iepf2_processer(self, fileName):
        query = "call iepf.iepf2_processer('"+fileName+"');"
        result = pd.read_sql_query(query, self.engine)
        return result
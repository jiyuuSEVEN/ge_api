from .dbConnection import get_connection
import pandas as pd

class IEPF2Model:
    def __init__(self):
        self.engine = get_connection()

    def check_filename(self, file_name):
        query = "SELECT COUNT(*) as is_duplicate FROM excel_log WHERE excel_name = '" + file_name + "' AND status = 1 LIMIT 1;"
        result = pd.read_sql_query(query, self.engine)
        return result.loc[0,'is_duplicate']

    def insert_excel_log(self, excel_log):
        result = excel_log.to_sql(con=self.engine, name='excel_log', if_exists='append', index=False)
        return result

    def insert_excel_data(self, excel_data, cin, file_name):
        # get dividend master data
        query = "SELECT d.id,d.proposed_date,d.dividend_amount,c.cin FROM iepf.dividend_master d JOIN iepf.company_master c ON d.security_code = c.security_code WHERE c.cin = '"+cin+"';"
        dividend_master = pd.read_sql_query(query, self.engine)
        dividend_master['proposed_date'] = pd.to_datetime(dividend_master['proposed_date'])

        # add xfer log id, start and end date to excel_data
        excel_data['dividend_count'] = excel_data.apply(lambda row: dividend_master[\
                            (dividend_master['proposed_date'] > row["proposeddateoftransfer_start"]) &\
                            (dividend_master['proposed_date'] < row["proposeddateoftransfer_end"])]['proposed_date'].count(), axis=1)

        get_logid_query = "select id from excel_log where excel_name = '" + file_name + "' order by uploadedat desc limit 1;"
        log_id = pd.read_sql_query(get_logid_query, self.engine)['id'].loc[0]
        excel_data['log_id'] = log_id

        # get multidividend data
        multi_dividend = excel_data[excel_data['dividend_count'] > 1]
        multi_dividend_result = multi_dividend.to_sql(con=self.engine, name='multiple_dividend', if_exists='append', index=False)

        # get singledividend data
        single_dividend = excel_data[excel_data['dividend_count'] == 1]
        single_dividend_result = single_dividend.to_sql(con=self.engine, name='iepf2', if_exists='append', index=False)

        # update excel log
        data_processed = str(single_dividend_result + multi_dividend_result)
        file_type = 'multiple dividend' if (multi_dividend_result > 0) else ('single dividend' if(single_dividend_result > 0) else 'no dividend')

        self.update_excel_log(data_processed, file_type, file_name)

        return single_dividend_result, multi_dividend_result

    def iepf2_processer(self):
        query = "CALL iepf.iepf2_processer();"
        with self.engine.connect() as connection:
            result = connection.execute(query)
            return result

    def update_excel_log(self, data_processed, file_type, file_name):
        query = "UPDATE excel_log SET dataprocessed = " + data_processed + ", file_type = '" + file_type + "', status = 1 WHERE excel_name = '" + file_name + "';"
        with self.engine.connect() as connection:
            result = connection.execute(query)
            return result
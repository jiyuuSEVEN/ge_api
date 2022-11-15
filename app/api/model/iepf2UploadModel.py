from .dbConnection import get_connection

class IEPF2Model:
    def __init__(self):
        self.engine = get_connection()

    def insert(self, excel_data):
        result = excel_data.to_sql(con=self.engine, name='iepf2', if_exists='append', index=False)
        return result
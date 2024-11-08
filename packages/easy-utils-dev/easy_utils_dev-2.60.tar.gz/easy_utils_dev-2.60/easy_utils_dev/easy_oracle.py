

import oracledb
from easy_utils_dev.encryptor import initCryptor

class OracleDb :
    def __init__(self) :
        self.encrypt = initCryptor()
        self.connection = None
        pass

    def get_pw(self , legacy=False) :
        if not legacy :
            return self.encrypt.dec_base64('Tm9raWFOZm10KzIwMjErMTIh')
        return self.encrypt.dec_base64('YWx1KzEyMz8=')   


    def connect(self , host , port=4999 , user='wdm' , legacy=False) :
        connection = oracledb.connect(
            user=user,
            password=self.get_pw(legacy),
            host=host,
            port=port,
            service_name="OTNE"
        )
        self.connection = connection
        return connection , connection.cursor()
    
    def execute_dict(self,  query , connection=None) :
        if not connection :
            connection = self.connection
        cursor = connection.cursor()
        cursor.execute(query)
        # Get column names
        columns = [col[0] for col in cursor.description]
        # Fetch all rows and create a list of dictionaries
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        return data
    
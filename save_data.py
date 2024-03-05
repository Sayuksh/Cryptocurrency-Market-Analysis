import psycopg2
import pandas as pd
from sqlalchemy import create_engine
hostname="localhost"
port_id=5432
username="postgres"
pwd="ayush"
database='cryptodata'


def save_data_to_database(data,table,task):
    try:
        conn=psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id
            )
        cur=conn.cursor()
        
        engine = create_engine(f'postgresql://{username}:{pwd}@{hostname}:{port_id}/{database}')
        data.to_sql(f"{table}",engine,if_exists=f"{task}",index=False)
    
    except Exception as error:
     print(error)
     return False
    
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close
    return True




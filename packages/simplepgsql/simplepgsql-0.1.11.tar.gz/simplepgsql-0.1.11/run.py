import pandas as pd
from simplepgsql import PgSQLWizard, SimplePgSQL
from simplepgsql import Query
import configparser

if __name__ == "__main__":
    # read data from config file
    config = configparser.ConfigParser()
    config.read("config.ini")
    conn_params = {
        "host": config['DB']['DB_HOST'],
        "database": config['DB']['DB_NAME'],
        "user": config['DB']['DB_USER'].strip(),
        "password": config['DB']['DB_PASSWORD'].strip(),
        "port": config['DB']['DB_PORT'],
    }

    _query_params = {
        'schema': "public",
        'table': "film_list",
        'columns': ["title", "price"],
        # 'aggregate': {
        #     "price": "SUM"
        # },
        # 'where': {
        #     "length": (">", 60)
        # },
        # 'order_by': {"price": 'DESC'},
        # 'group_by': ["category", "price"],
        'limit': 100,
    }

    _query = Query().from_params(**_query_params)
    pgsql = PgSQLWizard(**conn_params, return_type='pd.DataFrame')
    data = pgsql.read(_query)
    print(data)


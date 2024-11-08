import logging
from adsToolBox.loadEnv import env
from adsToolBox.dbPgsql import dbPgsql
from adsToolBox.dbMssql import dbMssql
from adsToolBox.pipeline import pipeline
from adsToolBox.logger import Logger
from adsToolBox.global_config import set_timer

logger = Logger(None, logging.DEBUG, "EnvLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

dict_pg = {'database': env.PG_DWH_DB
                          , 'user': env.PG_DWH_USER
                          , 'password': env.PG_DWH_PWD
                          , 'port': env.PG_DWH_PORT
                          , 'host': env.PG_DWH_HOST}

logger_connection = dbPgsql(dict_pg, None)
logger_connection.connect()

logger = Logger(logger_connection, logging.INFO, "AdsLogger", "LOGS",
                    "LOGS_details")
set_timer(True)
source = dbPgsql(dict_pg, logger)

destination = {
    'name': 'test',
    'db': dbMssql({'database':env.MSSQL_DWH_DB, 'user':env.MSSQL_DWH_USER,
                   'password':env.MSSQL_DWH_PWD, 'port':env.MSSQL_DWH_PORT_VPN
                    , 'host':env.MSSQL_DWH_HOST_VPN}, logger),
    'table': 'insert_test_2',
    'cols': ['name', 'email']
}
destination["db"].connect()
destination["db"].sqlExec('''
IF OBJECT_ID('dbo.insert_test_2', 'U') IS NOT NULL 
    DROP TABLE dbo.insert_test_2;

CREATE TABLE dbo.insert_test_2 (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);
''')

query = '''
SELECT name, email FROM insert_test;
'''

# Déclaration du pipeline
pipe = pipeline({
    'db_source': source, # La source du pipeline
    'query_source': query, # La requête qui sera exécutée sur cette source
    'db_destination': destination, # La destination du pipeline
    'mode': 'executemany', # en mode bulk, plus rapide
    'checkup': True, # Vérifie par la suite si la table destination
}, logger)

rejects = pipe.run()

logger.info("Fin de la démonstration")
from adsToolBox.loadEnv import env
from adsToolBox.logger import Logger
from adsToolBox.dbMssql import dbMssql
from adsToolBox.dbPgsql import dbPgsql

logger = Logger(None, Logger.DEBUG, "EnvLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

logger.info("Message d'info")
logger.debug("Message de debug")
logger.warning("Message de warning")

source = dbMssql({
    'database': env.MSSQL_DWH_DB,
    'user': env.MSSQL_DWH_USER,
    'password': env.MSSQL_DWH_PWD,
    'port': env.MSSQL_DWH_PORT_VPN,
    'host': env.MSSQL_DWH_HOST_VPN
}, logger)
source.connect()
logger.set_connection(source)

logger.create_logs_tables()

source.sqlExec('''
IF OBJECT_ID('dbo.insert_test', 'U') IS NOT NULL 
    DROP TABLE dbo.insert_test;
''')
source.sqlExec('''
CREATE TABLE dbo.insert_test (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);''')

source.insert('insert_test', ['name', 'email'], ['NOM', 'MAIL'])

res = source.sqlScalaire("SELECT COUNT(*) FROM insert_test;")

print(res)

logger.log_close("Réussite", "Tout le script a fonctionné")

logger.info("Cela ne devrait pas s'afficher.")
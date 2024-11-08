from adsToolBox.loadEnv import env
from adsToolBox.logger import Logger
from adsToolBox.dbMssql import dbMssql

logger = Logger(Logger.DEBUG, "EnvLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')

logger.info("TEST")
logger.debug("TEST")
logger.warning("WARNING")
logger.error("ERROR")
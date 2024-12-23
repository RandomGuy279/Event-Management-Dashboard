from .db_setup import dbConn
from .logger_setup import logger
from .config import configData


def addDefaultUser():
    dbConn.upsertData("users", configData["defaultUser"], configData["defaultUser"])
    logger.info("Default admin user is added.")
    return
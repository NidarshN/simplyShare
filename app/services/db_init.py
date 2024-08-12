import pymysql
from app.utils import get_database_client
import logging
import os

logger = logging.getLogger(__name__)

def init_table(create_query = '', table_name=''):
    """
    Function to create a table in the database
    
    Params:
    =======
    create_query (str): Query string to create a table in the database
    table_name (str): Name of the table

    Returns:
    ========
    bool : Return true if the table was created successfully else false
    """
    dbConn = get_database_client()
    if(dbConn is None):
        return False
    try:
        cursor = dbConn.cursor()
        cursor.execute(create_query)
        dbConn.commit()
        cursor.close()
        logger.info(f'Table {table_name} created successfully!')
        return True
    except:
        logger.exception(f'Error creating {table_name} table!')
    finally:
        dbConn.close()
        logger.info('Exited Table Creation!')

def initialize_tables():
    """
    Function to create the required tables in the database
    
    Params:
    =======
    None

    Returns:
    ========
    (bool) : Returns true if the tables were created successfully else false
    """
    user_table_query = os.getenv('CREATE_USERS_QUERY')
    fileshare_table_query = os.getenv('CREATE_FILESHARE_QUERY')
    table_users = 'users'
    table_fileshare = 'fileshare'
    user_status = init_table(user_table_query, table_users)
    fileshare_status = init_table(fileshare_table_query, table_fileshare)

    if(user_status and fileshare_status):
        logger.info(f'{table_users}, {table_fileshare} created successfully')
        return True
    else:
        return False



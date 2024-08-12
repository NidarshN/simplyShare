from app.config import Config
import boto3
import logging
import pymysql


logger = logging.getLogger(__name__)


def get_aws_resource_client(aws_resource_name=''):
    """
    Function to establish a connection to an AWS Resource

    Params:
    =======
    aws_resource_name (str): The name of the AWS Resource

    Returns:
    ========
    client (boto3.client): Boto3 client for the AWS Resource Connection
    """
    client = None
    try:
        client = boto3.client(service_name=aws_resource_name,
                                aws_access_key_id=Config.AWS_ACCESS_ID,
                                aws_secret_access_key=Config.AWS_USER_ACCESS_KEY,
                                region_name=Config.AWS_SERVICE_REGION)
        return client
    except:
        logger.exception(f'Unable to connect to the AWS {aws_resource_name} resource!')
        return client
    finally:
        logger.info('Exiting AWS Resource Client Connection!')

def get_database_client():
    """
    Function to establish a connection to the MySQL database

    Params:
    =======
    None

    Returns:
    ========
    dbClient (Connection): Connection client for the MySQL databse
    """
    dbClient = None
    try:
        dbClient = pymysql.connect(host=Config.AWS_RDS_ENDPOINT,
                        user=Config.AWS_RDS_USERNAME,
                        password=Config.AWS_RDS_PASSWORD,
                        database=Config.AWS_RDS_DB_NAME)
        return dbClient
    except:
        logger.exception('Unable to connect to RDS Database Resource!')
        return dbClient
    finally:
        logger.info('Exiting RDS Database Client Connection!')

def fetch_query(query_string = '', query_params = '', fetch_type = 'fetch_all'):
    """
    Function to fetch results from a database using query

    Params:
    =======
    query_string (str): Query string to be executed in the database

    Returns:
    ========
    query_results (tuple): Results of the query performed in the database
    """
    query_results = None
    try:
        if(query_string == ''):
            raise Exception('Query String Empty!')
        dbConnection = get_database_client()
        dbCursor = dbConnection.cursor()
        if(query_params == ''):
            dbCursor.execute(query_string)
        else:
            dbCursor.execute(query_string, query_params)
        if(fetch_type == 'fetch_one'):
            query_results = dbCursor.fetchone()
        else:
            query_results = dbCursor.fetchall()
        logger.info(f'fetch query: {query_results}')
        return query_results
    except:
        logger.exception('Unable to execute the fetch results for Query!')
        return query_results
    finally:
        dbConnection.close()
        logger.info('Exiting Run Database Fetch Query!')

def insert_query(query_string = '', query_params = '', insert_many = False):
    """
    Function to insert records into the database
    
    Params:
    =======
    query_string (str): Query string to be executed in the database

    Returns:
    ========
    rowcount (int): Returns the number of rows affected by the query
    """
    query_result = 0
    try:
        if(query_string == ''):
            raise Exception('Query String Empty')
        dbConnection = get_database_client()
        dbCursor = dbConnection.cursor()
        if(insert_many):
            dbCursor.executemany(query_string, query_params)
        else:
            dbCursor.execute(query_string, query_params)
        dbConnection.commit()
        query_result = dbCursor.rowcount
        logger.info(f'{query_result} rows inserted!')
        return query_result
    except:
        logger.exception('Unable to insert records into the database!')
        return query_result
    finally:
        dbConnection.close()
        logger.info('Exiting Run Database Insert Query!')

def run_query(query_string = '', query_params = ''):
    """
    Function to insert records into the database
    
    Params:
    =======
    query_string (str): Query string to be executed in the database

    Returns:
    ========
    rowcount (int): Returns the number of rows affected by the query
    """
    query_result = 0
    try:
        if(query_string == ''):
            raise Exception('Query String Empty')
        dbConnection = get_database_client()
        dbCursor = dbConnection.cursor()
        dbCursor.execute(query_string, query_params)
        dbConnection.commit()
        query_result = dbCursor.rowcount
        logger.info(f'{query_result} rows affected!')
        return query_result
    except:
        logger.exception('Unable to run query into the database!')
        return query_result
    finally:
        dbConnection.close()
        logger.info('Exiting Run Query!')
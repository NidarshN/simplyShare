from app.utils import fetch_query, insert_query, run_query
import logging
import os
from flask_bcrypt import Bcrypt

logger = logging.getLogger(__name__)
db_bcrypt = Bcrypt()

def validateUser(username, password):
    """
    Function to validate the user's credential stored in the database
    
    Params:
    =======
    username (str): username of the user
    password (str): password of the user
    
    Returns:
    ========
    (bool) : True if the user credentials are valid otherwise False
    """
    query_string = 'SELECT username, password FROM users WHERE username=%s'
    query_params = [username]
    query_results = fetch_query(query_string, query_params, 'fetch_one')
    if (query_results is None or len(query_results) == 0):
        logger.error('Invalid username or password!')
        return False
    logger.info(f'Password Hash Result: {db_bcrypt.check_password_hash(query_results[1], password)}')
    if (username == query_results[0] and 
        db_bcrypt.check_password_hash(query_results[1], password)):
        return True
    else:
        return False

def isUsernameUnique(username):
    """
    Function to check if username is unique in the database
    
    Params:
    =======
    username (str): username of the user
    
    Returns:
    ========
    (bool) : True if username is unique otherwise False
    """
    query_string = 'SELECT username FROM users WHERE username=%s '
    query_params = [username]
    query_results = fetch_query(query_string, query_params, 'fetch_one')
    if(query_results is None or len(query_results) == 0):
        logger.info(f'{username} is unique!')
        return True
    
    if(username == query_results[0]):
        logger.error(f'{username} is not unique!')
        return False
    
def insert_user(userdetails=None):
    """
    Function to insert a user record into the users table
    
    Params:
    =======
    userdetails (dict): Dictionary containing user details. Default None
    
    Returns:
    ========
    (bool) : True if record was successfully inserted else False
    """
    if(userdetails is None):
        logger.info('Received empty user details!')
        return False
    else:
        query_string = 'INSERT INTO users(name, username, email, password, bucketname) values (%s, %s, %s, %s, %s)'
        query_params = list(userdetails.values())
        query_results = insert_query(query_string=query_string, 
                                        query_params=query_params,
                                        insert_many=False)
        if(query_results is None or query_results <= 0):
            logger.error('Unable to insert query into the users table!')
            return False
        else:
            logger.info('Insertion to users table successful!')
            return True
        
def file_insert(user='', filename='', file_url=None, bucketname='', emaillist=[]):
    fileid = f'{user}-{filename}-{bucketname}'
    logger.info(f'file_insert: {bucketname}')
    logger.info(f'file_insert: {fileid}')
    is_file_inserted = insert_filedetails(filename, fileid, file_url, bucketname)
    if(is_file_inserted == False):
        return False
    logger.info(f'file_inser: {emaillist}')
    is_fileshare_inserted = insert_fileshare(user, fileid, bucketname, emaillist)
    return is_fileshare_inserted 


def insert_filedetails(filename='', fileid='', file_url = None, bucketname=''):
    logger.info(f'insert_filedetails: {bucketname}')
    try:
        query_string = 'INSERT INTO filedetails(fileid, filename, fileurl, bucketname) values (%s, %s, %s, %s)'
        query_params = [fileid, filename, file_url, bucketname]
        query_results = insert_query(query_string, query_params)
        if(query_results is None or query_results <= 0):
            logger.error(f'Unable to insert file details into the table!')
            return False
        else:
            logger.info('Inserted file details into the table successfully!')
            return True
    except:
        logger.exception(f'Unable to insert file details into the table!')
        return False
    finally:
        logger.info('Exiting insert_filedetails!')


def insert_fileshare(user='', fileid='', bucketname='', emaillist=[]):
    logger.info(f'insert_fileshare: {emaillist}')
    try:
        is_insert_many = False
        query_string = 'INSERT INTO fileshare(sender, fileid, bucketname, recipient) values (%s, %s, %s, %s)'
        logger.info(f'inside insert_fileshare: {emaillist} , {len(emaillist)}')
        if(len(emaillist) <= 1):
            query_params = [user, fileid, bucketname, emaillist]
            is_insert_many = False
            logger.info(f'inser_fileshare: {query_params}')
        else:
            query_params = [[user, fileid, bucketname, recipient] for recipient in emaillist]
            is_insert_many = True
            logger.info(f'inser_fileshare: {query_params}')
        query_results = insert_query(query_string, query_params, insert_many=is_insert_many)
        if(query_results is None or query_results <= 0):
            logger.error(f'Unable to insert file details into the table!')
            return False
        else:
            logger.info('Inserted file share record into the table successfully!')
            return True
    except:
        logger.exception(f'Unable to insert file share record into the table!')
        return False
    finally:
        logger.info('Exiting insert_fileshare!')

def get_bucket_name(username=''):
    """
    Function to get the user's bucket name
    
    Params:
    =======
    username (str) : User's username
    
    Returns:
    ========
    bucket_name (str) : User's bucket name
    """
    if(username == ''):
        return None
    else:
        query_string = 'SELECT bucketname FROM users WHERE username = %s'
        query_params = [username]
        query_results = fetch_query(query_string, query_params, 'fetch_one')
        logger.info(f'Bucket Query: {query_results} ')
        if(query_results is None or len(query_results) == 0):
            logger.error('Unable to fetch bucketname!')
            return None
        else:
            logger.info('Bucketname fetched successfully!')
            return query_results
        
def get_user_email(username=''):
    """
    Function to get the user's Email ID 
    
    Params:
    =======
    username (str) : User's username
    
    Returns:
    ========
    emailid (str) : User's emailid
    """
    if(username == ''):
        return None
    else:
        query_string = 'SELECT email FROM users WHERE username = %s'
        query_params = [username]
        query_results = fetch_query(query_string, query_params, 'fetch_one')
        logger.info(f'Email Query: {query_results} ')
        if(query_results is None or len(query_results) == 0):
            logger.error('Unable to fetch Email!')
            return None
        else:
            logger.info('Email fetched successfully!')
            return query_results
        
def get_username(user_email=''):
    """
    Function to get the user's username
    
    Params:
    =======
    user_email (str) : User's emailid
    
    Returns:
    ========
    username (str) : User's username
    """
    if(user_email == ''):
        return None
    else:
        query_string = 'SELECT username FROM users WHERE email = %s'
        query_params = [user_email]
        query_results = fetch_query(query_string, query_params, 'fetch_one')
        logger.info(f'Username Query: {query_results} ')
        if(query_results is None or len(query_results) == 0):
            logger.error('Unable to fetch Username!')
            return None
        else:
            logger.info('Username fetched successfully!')
            return query_results[0]
        
def get_download_file(sender_email='', recipient_email='', filename=''):
    extList = ["doc", "html", "css", "js", "json", "md", 
                "txt", "png", "jpg", "gif", "pdf", "zip",
            ]
    username = get_username(sender_email)
    if(username is None):
        return {"statusCode": 409}
    logger.info(f'Args: {sender_email} : {recipient_email} : {filename} : {username}')
    file_share_query = f"SELECT * FROM fileshare WHERE sender='{username}' AND recipient='{recipient_email}' AND fileid LIKE '%{filename}%'"
    query_results = fetch_query(file_share_query, '','fetch_one')
    if(len(query_results) <= 0):
        return {"statusCode": 409}
    fileid = query_results[2]
    file_details_query = f"SELECT filename, fileurl FROM filedetails WHERE fileid = '{fileid}'"
    fd_query_results = fetch_query(file_details_query, '','fetch_one')
    logger.info(f'File Info: {fd_query_results}')
    if(len(fd_query_results) > 0):
        file_name, file_link = fd_query_results
        ext = file_name.split('.')[1]
        icon_class = f'fileIcon bx bxs-file-{ext}' if ext in extList else f'fileIcon bx bxs-file'
        logger.info(f'File details filename: {file_name}, fileurl: {file_link}')
        return {"statusCode": 200, "sender": username, "recipient": recipient_email, "filename": file_name, "fileurl": file_link, "iconclass": icon_class}
    else:
        logger.info('Unable to fetch file details!')
        return {"statusCode": 409}
    
def get_fileshared_status(fileid=''):
    query_string = "SELECT FLOOR(SUM(CASE WHEN isdownloaded = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS download_percentage FROM fileshare WHERE fileid = %s";
    query_params = [fileid]
    query_results = fetch_query(query_string,query_params,'fetch_one')
    if(len(query_results) > 0):
        logger.info(f'get_fileshared_status: {query_results}')
        query_results = int(query_results[0])
    else:
        logger.info(f'get_fileshared error: {query_results}')
        logger.error('Unable to fetch share updates for file!')
    return query_results

def update_fileshare_status(sender='', recipient='', fileid=''):
    update_query_string = "UPDATE fileshare SET isdownloaded=TRUE WHERE sender=%s AND recipient=%s AND fileid = %s"
    update_params = [sender, recipient, fileid]
    update_results = run_query(update_query_string, update_params)
    if(update_results> 0):
        logger.info(f'Updated the fileshare isdownload status!')
        return True
    else:
        logger.info(f'Unable to update the fileshare isdownload status!')
        return False

def get_details_fileurl(fileurl=''):
    tem

def update_fileshare(sender='', recipient='', filename='', fileurl=''):
    temp_id = fileurl.split('.')[0]
    temp_id = temp_id.split('//')[1]
    fileid = f'{sender}-{filename}-{temp_id}'

    update_result = update_fileshare_status(sender, recipient, fileid)
    if(update_result == False):
        update_result = update_fileshare_status(sender, recipient, fileid)
    
    query_result = get_fileshared_status(fileid)
    return (query_result == 100), temp_id, fileid

def delete_file_db(fileid=''):
    query_string = 'DELETE FROM filedetails WHERE fileid=%s'
    query_param = [fileid]
    query_result = run_query(query_string, query_param)
    if(query_result > 0):
        logger.info(f'File Deleted Successfully!')
        return True
    else:
        logger.info(f'Unable to delete file from database!')
        return False

def prepare_payload(query_result, user, payload_type = 'OWN'):
    # usr_email = get_user_email(user)
    # payload_list = []
    # for result in query_result:
    #     payload = {}
    #     if(len(result) == 0):
    #         return [{}]
    #     if(payload_type == 'OWN'):
    #         payload["sender"] = user
    #         payload['recipient'] = ''
    #     elif(payload_type == 'SHARED'):
    #         sender = result[1].split('-')[0]
    #         payload['sender'] = sender
    #         payload["recipient"] = usr_email
    #     payload["filename"] = result[2]
    #     payload["fileurl"] = result[3]
    #     payload_list.append(payload)

    if(payload_type == 'OWN'):
        payload_list = []
        for result in query_result:
            payload = {}
            if(len(result) == 0):
                return [{}]
            payload['sender'] = user
            payload['recipient'] = ''
            payload['filename'] = result[2]
            payload['fileurl'] = result[3]
            payload_list.append(payload)
    elif(payload_type == 'SHARED'):
        usr_email = get_user_email(user)
        payload_list = []
        for result in query_result:
            payload = {}
            if(len(result) == 0):
                return [{}]
            sender = result[1].split('-')[0]
            payload['sender'] = sender
            payload['recipient'] = usr_email[0]

            payload['filename'] = result[2]
            payload['fileurl'] = result[3]
            payload_list.append(payload)
    return payload_list
        

def get_file_share_list(user=''):
    user_email = get_user_email(user)
    logger.info(f'gfsl {user} : {user_email}')
    own_query_string = 'SELECT * FROM filedetails WHERE fileid IN (SELECT DISTINCT fileid FROM fileshare WHERE sender = %s)'
    own_query_params = [user]
    own_query_result = fetch_query(own_query_string, own_query_params, 'fetch_all')
    own_payload = {}
    if(len(own_query_result) > 0):
        logger.info(f'Fetched own files successfully for user: {user} : {len(own_query_result)}')
        own_payload = prepare_payload(own_query_result, user, 'OWN')
    else:
        logger.error(f'Unable to Fetch Own files for user: {user}')
    
    shared_query_string = 'SELECT * FROM filedetails WHERE fileid IN (SELECT DISTINCT fileid FROM fileshare WHERE recipient = %s)'
    shared_query_params = [user_email]
    shared_query_result = fetch_query(shared_query_string, shared_query_params, 'fetch_all')
    shared_payload = {}
    if(len(shared_query_result) > 0):
        logger.info(f'Fetched shared files successfully for user: {user} {user_email}: {len(shared_query_result)}')
        shared_payload = prepare_payload(shared_query_result, user, 'SHARED')
    else:
        logger.error(f'Unable to Fetch shared files for user: {user} {user_email}')
    
    logger.info(f'Own: {own_payload}')
    logger.info(f'Shared: {shared_payload}')


    payload = {
        'own': own_payload,
        'shared': shared_payload
    }

    return payload
    
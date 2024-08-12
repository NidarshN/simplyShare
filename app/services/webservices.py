import boto3
from app.utils import get_aws_resource_client
from app.services.db import get_bucket_name, get_user_email, file_insert
import logging
import os
import json
import time

logger = logging.getLogger(__name__)

def create_s3_bucket(bucket_name):
    """
    Function to create a named AWS S3 bucket

    Params:
    =======
    bucket_name (str) : Name of the AWS S3 bucket to be created

    Returns:
    ========
    status_code (int) : Status code to indicate if the bucket is created successfully or not
    """
    s3_client = get_aws_resource_client(aws_resource_name='s3')
    try:
        response = s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-1',
            },
            ObjectLockEnabledForBucket=False,
            ObjectOwnership='ObjectWriter'
        )
        if(response != None 
            and response['ResponseMetadata'] != {} 
            and response['ResponseMetadata']['HTTPStatusCode'] == 200):
            public_access_response = s3_client.put_public_access_block(Bucket=bucket_name, 
                                                            PublicAccessBlockConfiguration={
                                                                'BlockPublicAcls': False,
                                                                'IgnorePublicAcls': False, 
                                                                'BlockPublicPolicy': False, 
                                                                'RestrictPublicBuckets': False})
            public_acl_response = s3_client.put_bucket_acl(ACL='public-read-write',Bucket=bucket_name)
            if(public_access_response['ResponseMetadata']['HTTPStatusCode'] == 200
                and public_acl_response['ResponseMetadata']['HTTPStatusCode'] == 200):
                logger.info(f'Bucket: {bucket_name} created successfully!')
                return 1
        else:
            logger.error(f'Bucket: {bucket_name} creation encountered an error!')
            return 0
    except s3_client.exceptions.BucketAlreadyOwnedByYou as e:
        logger.exception(f'Bucket: {bucket_name} already owned by you! {e.response}')
        return 2
    except s3_client.exceptions.BucketAlreadyExists as e:
        logger.exception(f'Bucket: {bucket_name} already exists! {e.response}')
        return 2
    except:
        logger.exception(f'Bucket: {bucket_name} creation is not successful!')
        return 0
    finally:
        logger.info('Exiting create_s3_bucket!')
        s3_client.close()

def upload_file_bucket(user='', filepath=''):
    """
    Function to upload a file to the user's owned bucket
    
    Params:
    =======
    user (str) : User's username
    filepath (str) : Path of the file to upload
    
    Returns:
    ========
    (bool) : True if file upload is successful otherwise False
    """
    filename = os.path.basename(filepath)
    logger.info(f'filename : {filename}')
    bucketname = get_bucket_name(user)
    bucketname = bucketname[0]
    logger.info(f'Bucket name: {bucketname}')
    if(bucketname is not None):
        s3_client = get_aws_resource_client(aws_resource_name='s3')
        try:
            response = s3_client.upload_file(Filename=filepath, 
                                    Bucket=str(bucketname),
                                    Key=filename,
                                    ExtraArgs={'GrantRead': 'uri="http://acs.amazonaws.com/groups/global/AllUsers"'})
            return bucketname
        except:
            logger.exception(f'Unable to upload file {filename}!')
            return None
        finally:
            logger.info('Exiting upload_file_bucket!')
            s3_client.close()
    else:
        return None
        
def get_signed_url(filepath='', bucketname=''):
    filename = os.path.basename(filepath)
    file_link = f'https://{bucketname}.s3.{os.getenv("AWS_SERVICE_REGION")}.amazonaws.com/{filename}'
    return filename, file_link
    
def send_notification(user='', emaillist =[], file_url=''):
    try:
        user_email = get_user_email(user)
        logger.info(f'send_notification: {user_email}')
        user_email = user_email[0]
        lambda_client = get_aws_resource_client('lambda')
        lambda_payload = {"user_email": user_email, "emaillist": emaillist, "link": file_url} #TODO: Needs update
        response = lambda_client.invoke(
                        FunctionName=os.getenv('AWS_LAMBDA_NAME'),
                        InvocationType='Event',
                        Payload=json.dumps(lambda_payload)
                    )
        logger.info(f'Lambda Response: {response}')
        if(response is not None and response['StatusCode'] >= 200):
            logger.info(f'LambdaSES invoked successfully for {user} !')
            return True
        else:
            return False
    except:
        logger.exception(f'LambdaSES invocation failed for {user} !')
        return False
    finally:
        logger.info('Exiting send_notification!')

def upload_and_notify(user='', filepath='', emaillist=[]):
    if(user == ''
            or filepath == ''
            or emaillist == []):
        return False
    
    uploaded_bucket = upload_file_bucket(user, filepath)
    logger.info(f'Uploaded Bucket: {uploaded_bucket}')
    if(uploaded_bucket is None):
        return False
    filename, file_url = get_signed_url(filepath, uploaded_bucket)
    logger.info(f'Unsigned URL: {file_url}')
    if(file_url == None):
        return False
    logger.info(f'upload_notify: {emaillist}')
    
    is_notified = send_notification(user, emaillist, filename)
    logger.info(f'Is Notified: {is_notified}')
    if(is_notified == False):
        return is_notified
    logger.info(f'before file_insert: {emaillist}')
    is_file_inserted = file_insert(user, filename, file_url, uploaded_bucket, emaillist)
    logger.info(f'Is Inserted: {is_file_inserted}')
    return is_file_inserted
    
def is_email_verified(email = ''):
    """
    Function to verify email address in AWS SES Identities

    Params:
    =======
    email (str) : Email to be verified

    Returns:
    ========
    (bool) : True if the email is verified otherwise False
    """
    if(email == ''):
        return False
    
    try:
        ses_client = get_aws_resource_client('ses')
        response = ses_client.list_identities(
            IdentityType = 'EmailAddress',
        )
        logger.info(f'Response SES {response}')
        logger.info(f"Email Check : {email in response['Identities']}")
        if(response is None 
                or response['Identities'] is None 
                or response['Identities'] == []):
            return False
        logger.info(f'Response SES {response}')
        if(email in response['Identities']):
            return True
        else:
            ses_client.verify_email_identity(
                EmailAddress = email)
            time.sleep(5)
            verify_res = verify_ses_email(email)
            logger.info(f'Email {email} verification result is {verify_res}!')
            return verify_res
    except:
        logger.exception('Unable to perform email verification');
        return False
    finally:
        logger.info('Exiting is_email_verified')
        ses_client.close()

def verify_ses_email(email=''):
    """
    Function to verify the user has confirmed the email verification request
    
    Params:
    =======
    email (str) : email to be verified
    
    Returns:
    ========
    (bool) : True if the user has confirmed email verification request otherwise False
    """
    if(email == ''):
        return False
    
    isVerified = False
    try:
        ses_client = get_aws_resource_client('ses')
        response = ses_client.get_identity_verification_attributes(
                        Identities=[email,]
                    )
        if(response is not None 
            and response['VerificationAttributes'] != {}):
            status = response['VerificationAttributes'][email]['VerificationStatus']
            isVerified = True if status == 'Success' else False
            logger.info(f'Email verification: {isVerified}')
            return isVerified
        else:
            logger.info('Email verification failed!')
            return False
    except:
        logger.exception('Email verification failed!')
        return False
    finally:
        logger.info('Exiting verify_ses_email!')
        ses_client.close()

def delete_file_bucket(filename='', bucketname=''):
    """
    Function to delete a file from the user's owned bucket
    
    Params:
    =======
    filename (str) : Name of the file to be deleted
    bucketname (str) : Name of the bucket
    
    Returns:
    ========
    (bool) : True if file is deleted successfully otherwise False
    """
    logger.info(f'Bucket name: {bucketname}')
    s3_client = get_aws_resource_client(aws_resource_name='s3')
    try:
        response = s3_client.delete_object(Bucket=str(bucketname),
                        Key=filename)
        logger.info(f'Delete File from bucket: {response}')
        if(response is not None 
            and response['ResponseMetadata']['HTTPStatusCode'] == 204):
            return True
        else:
            return False
    except:
        logger.exception(f'Unable to delete file {filename}!')
        return None
    finally:
        logger.info('Exiting delete_file_bucket!')
        s3_client.close()
        

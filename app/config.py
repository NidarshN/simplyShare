import os
from datetime import timedelta


class Config(object):

    AWS_ACCESS_ID = os.getenv('AWS_ACCESS_ID')
    AWS_USER_ACCESS_KEY = os.getenv('AWS_USER_ACCESS_KEY')
    AWS_SERVICE_REGION = os.getenv('AWS_SERVICE_REGION')
    AWS_DEFAULT_OUTPUT_FORMAT = os.getenv('AWS_DEFAULT_OUTPUT_FORMAT')

    AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

    AWS_SNS_TOPIC_NAME = os.getenv('AWS_SNS_TOPIC_NAME')
    AWS_SNS_TOPIC_ARN = os.getenv('AWS_SNS_TOPIC_ARN')

    AWS_RDS_INSTANCE_ID = os.getenv('AWS_RDS_INSTANCE_ID')
    AWS_RDS_USERNAME = os.getenv('AWS_RDS_USERNAME')
    AWS_RDS_PASSWORD = os.getenv('AWS_RDS_PASSWORD')
    AWS_RDS_ENDPOINT = os.getenv('AWS_RDS_ENDPOINT')
    AWS_RDS_PORT = os.getenv('AWS_RDS_PORT')
    AWS_RDS_DB_NAME = os.getenv('AWS_RDS_DB_NAME')

    AWS_LAMBDA_NAME = os.getenv('AWS_LAMBDA_NAME')

    LOGS_PATH = os.getenv('LOGS_PATH')
    UPLOAD_FOLDER = os.getenv('UPLOAD_PATH')

    # MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH'))
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=3)
    SESSION_TYPE = os.getenv('SESSION_TYPE')
    SECRET_KEY = os.getenv('SECRET_KEY')
    PROJECT_NAME = os.getenv('PROJECT_NAME')
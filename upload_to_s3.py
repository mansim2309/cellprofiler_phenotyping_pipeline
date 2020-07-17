import boto3
import botocore
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIAXDHAIW77BMWXFAVM'
SECRET_KEY = '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'
bucket = 'theriotbucket'
s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
file_to_be_downloaded = 'test.csv'
downloaded_file = '/Users/mansimehrotra/Desktop/test.csv'

def upload_to_aws(local_file, bucket, s3_file, s3_client):
    try:
        s3_client.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def download_from_s3(file_to_be_downloaded, bucket, s3_client, downloaded_file):
    try:
        s3_client.download_file(bucket, file_to_be_downloaded, downloaded_file )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

uploaded = upload_to_aws('/Users/mansimehrotra/Desktop/theriot_lab/resources/u26a_ar014d_analysisImage.csv', bucket, 'test.csv', s3_client)
downloaded = download_from_s3(file_to_be_downloaded, bucket, s3_client, downloaded_file)

import boto3
import botocore
from botocore.exceptions import NoCredentialsError
import os
import shutil
import numpy as np
import skimage.io
from PIL import Image
import time

ACCESS_KEY = 'AKIAXDHAIW77BMWXFAVM'
SECRET_KEY = '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'
bucket = 'theriotbucket'
#s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

def downloadDirectoryFroms3(bucket, remoteDirectoryName, ACCESS_KEY, SECRET_KEY):
    s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    bucket = s3_resource.Bucket(bucket)
    removeDir = True

    #download from S3
    for object in bucket.objects.filter(Prefix=remoteDirectoryName):
        if removeDir:
            shutil.rmtree(os.path.dirname(object.key))
            removeDir = False
            if not os.path.exists(os.path.dirname(object.key)):
                os.makedirs(os.path.dirname(object.key))
            continue
        #print(object.key)
        start = time.process_time()
        bucket.download_file(object.key, object.key)
        print("Time Taken to Download :" ,time.process_time() - start)

        #save to local
        start = time.process_time()
        im_in = Image.open(object.key)
        for ch in range(1, 5):
            if ch > 1:
                im_in.seek(ch - 1)
            im_out = np.asarray(im_in)
            #print(object.key[8:-8])
            fname_out = 'Ch_Testing/' + object.key[8:-8] + '_ch' + str(ch) + '.tif'
            print(fname_out)
            skimage.io.imsave(fname_out, im_out, check_contrast=False)
            print("Time Taken to process one channel image :", time.process_time() - start)
            start = time.process_time()
            #upload to S3
            try:
                bucket.upload_file(fname_out, fname_out)
                print("Upload Successful")
                print("Time Taken to upload one channel image :", time.process_time() - start)
            except FileNotFoundError:
                print("The file was not found")
            except NoCredentialsError:
                print("Credentials not available")

            #delete from local
            os.remove(fname_out)
        os.remove(object.key)

downloadDirectoryFroms3(bucket, 'Testing', ACCESS_KEY, SECRET_KEY)
import boto3
import botocore
from botocore.exceptions import NoCredentialsError
import os
import shutil
import numpy as np
import skimage.io
from PIL import Image
import time

#input code here for fetching access key and secret key
bucket = 'theriotbucket'
#s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
time_download = []
time_channel_splitting = []
time_upload = []


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
        start_d = time.time()

        bucket.download_file(object.key, object.key)

        end_d = time.time()
        time_diff_d  = (end_d - start_d) * 1000
        print("Time Taken to Download in ms :", time_diff_d)
        time_download.append(time_diff_d)

        #save to local
        start_ch = time.time()
        i = 0

        im_in = Image.open(object.key)

        for ch in range(1, 5):
            if i != 0:
                start_ch = time.time()

            if ch > 1:
                im_in.seek(ch - 1)
            im_out = np.asarray(im_in)

            fname_out = 'Ch_Testing/' + object.key[8:-8] + '_ch' + str(ch) + '.tif'
            print(fname_out)
            skimage.io.imsave(fname_out, im_out, check_contrast=False)

            end_ch = time.time()
            time_diff_ch = (end_ch - start_ch) * 1000
            print("Time Taken to Process one channel image in ms :", time_diff_ch)

            time_channel_splitting.append(time_diff_ch)
            i += 1

            start_up = time.time()

            #upload to S3
            try:
                bucket.upload_file(fname_out, fname_out)
                print("Upload Successful")
                end_up = time.time()
                time_diff_up = (end_up - start_up) * 1000
                print("Time Taken to Upload one channel image in ms :", time_diff_up)
                time_upload.append(time_diff_up)

            except FileNotFoundError:
                print("The file was not found")
            except NoCredentialsError:
                print("Credentials not available")

            #delete from local
            os.remove(fname_out)
        os.remove(object.key)


start_overall = time.time()
downloadDirectoryFroms3(bucket, 'Testing', ACCESS_KEY, SECRET_KEY)
end_overall = time.time()

time_diff_overall = ( end_overall - start_overall ) * 1000

print("Time taken for overall execution in ms: ", time_diff_overall)
print("Time array donwload :", time_download)
print("Time array upload : ", time_upload)
print("Time array process channel : ", time_channel_splitting)

import boto3
import botocore
from botocore.exceptions import NoCredentialsError
import time
import multiprocessing
import numpy as np
import skimage.io
from PIL import Image
from logger import Logger
import os


ACCESS_KEY = 'AKIAXDHAIW77BMWXFAVM'
SECRET_KEY = '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'
bucket_name = 'theriotbucket'

s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
bucket = s3_resource.Bucket(bucket_name)


def get_objects_in_folder(folderpath):

    files = []
    objects = list(bucket.objects.filter(Prefix=folderpath))
    checkpoints = []

    with open('checkpoint.txt') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        checkpoints.append(lines[i].strip('\n'))

    for i in range(1,len(objects)):
        if objects[i].key not in checkpoints:
            files.append(objects[i].key)

    return files


def download_from_s3(filename):
    try:
        print("Downloading file : {} ".format(filename))

        Logger.get_logger().info("Starting Processing for file  : {} ".format(filename))

        Logger.get_logger().info("Downloading file : {} ".format(filename))

        bucket.download_file(filename, filename)
        Logger.get_logger().info("File Downloaded  : {} ".format(filename))

        Logger.get_logger().info("Splitting into channels : {} ".format(filename))
        split_into_channels(filename)

        Logger.get_logger().info("Saving Checkpoints : {} ".format(filename))
        save_checkpoint(filename)
        Logger.get_logger().info("Checkpoint Saved : {} ".format(filename))

        Logger.get_logger().info("Removing file from local  : {} ".format(filename))
        os.remove(filename)

        Logger.get_logger().info("Finished Processing for file  : {} ".format(filename))

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


def split_into_channels(filename):
    im_in = Image.open(filename)

    for ch in range(1, 5):
        if ch > 1:
            im_in.seek(ch - 1)
        im_out = np.asarray(im_in)

        fname_out = '2020-03-05_u26a_midiscreen/' + 'u26a_20x-0.75_DAPI-TRITC-Cy5-Ph_Channel_WholePlate_1/' + filename[72:-8] + '_ch' + str(ch) + '.tif'
        print(fname_out)
        skimage.io.imsave(fname_out, im_out, check_contrast=False)
        Logger.get_logger().info("For file : {} , channel: {} , splitting success ".format(filename, ch))
        Logger.get_logger().info("Uploading file : {} ".format(fname_out))
        bucket.upload_file(fname_out, fname_out)
        Logger.get_logger().info("Uploading Success : {} ".format(fname_out))
        Logger.get_logger().info("Removing file from local  : {} ".format(fname_out))
        os.remove(fname_out)


def save_checkpoint(filename):
    print("Saving Checkpoint for filename : ", filename)
    f = open("checkpoint.txt", "a+")
    f.write(filename)
    f.write("\n")
    f.close()


if __name__ == '__main__':

    # Get all the filenames from whole plate directory which are not present in checkpoint.txt
    filenames = get_objects_in_folder('2020-03-05_u26a_midiscreen/' + "u26a_20x-0.75_DAPI-TRITC-Cy5-Ph_WholePlate_1")
    start = time.time()

    # Parallel Approach 1
    # procs = []
    # for file in filenames:
    #     proc = Process(target=download_from_s3, args=(file,))
    #     procs.append(proc)
    #     proc.start()
    #
    # for proc in procs:
    #     proc.join()


    # Parallel Approach 2

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(download_from_s3, filenames)
    pool.close()
    pool.join()

    end = time.time()
    diff = (end - start)

    print("Time taken : ", diff)

import numpy as np
#import bokeh
import boto3
from boto3 import Session
import botocore
from botocore.exceptions import NoCredentialsError
import time
import subprocess
import glob
from dask_cloudprovider import FargateCluster
from dask.distributed import Client, LocalCluster

def get_objects_in_folder(folderpath):
    files = []
    session = Session()
    credentials = session.get_credentials()
    current_credentials = credentials.get_frozen_credentials()
    ACCESS_KEY = current_credentials.access_key
    SECRET_KEY = current_credentials.secret_key
    
    bucket_name = 'theriotbucket'
    s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    bucket = s3_resource.Bucket(bucket_name)
    objects = list(bucket.objects.filter(Prefix=folderpath))
    for i in range(1,len(objects)):
        files.append(objects[i].key)
    return files


def download_from_s3(filename):
    print('Entered function')
    roots = []  
    roots.append(filename + '_ch1.tif')
    roots.append(filename + '_ch2.tif')
    roots.append(filename + '_ch3.tif')
    roots.append(filename + '_ch4.tif')
    session = Session()
    credentials = session.get_credentials()
    current_credentials = credentials.get_frozen_credentials()
    ACCESS_KEY = current_credentials.access_key
    SECRET_KEY = current_credentials.secret_key
    bucket_name = 'theriotbucket'
    s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    bucket = s3_resource.Bucket(bucket_name)
    import os
    ifoldername = '/input/FOV_6x6_' + filename[8:]
    print(roots[0])
    print(ifoldername)
    ofoldername = 'Output_' + filename[8:]
    if not os.path.exists(ifoldername):
        os.mkdir(ifoldername)
    if not os.path.exists(ofoldername):
        os.mkdir(ofoldername)
    bucket.download_file('docker_052020_v1_working_all_imgset.cppipe', ifoldername + '/docker_052020_v1_working_all_imgset.cppipe')
    bucket.download_file('u26a-A2-center6x6_IllumActin_fitPoly_v1.npy', ifoldername + '/u26a-A2-center6x6_IllumActin_fitPoly_v1.npy')
    bucket.download_file('u26a-A2-center6x6_IllumDNA_fitPoly_v1.npy', ifoldername + '/u26a-A2-center6x6_IllumDNA_fitPoly_v1.npy')
    bucket.download_file('u26a-A2-center6x6_IllummCh_fitPoly_v1.npy', ifoldername + '/u26a-A2-center6x6_IllummCh_fitPoly_v1.npy')
    npy1 = ifoldername + '/u26a-A2-center6x6_IllumDNA_fitPoly_v1.npy'
    npy2 = ifoldername + '/u26a-A2-center6x6_IllumActin_fitPoly_v1.npy'
    npy3 = ifoldername + '/u26a-A2-center6x6_IllummCh_fitPoly_v1.npy'
    try:
        for f in roots:
            file_to_be_downloaded = ifoldername + '/' + f[8:]
            print(file_to_be_downloaded)
            print("Downloading file : {} ".format(f))
            bucket.download_file(f, file_to_be_downloaded)
        checkpoint_file = save_checkpoint(roots, ifoldername, npy1, npy2, npy3)
        print("Entering subprocess call")
        cp_pipeline_downloaded_file = ifoldername + '/' + 'docker_052020_v1_working_all_imgset.cppipe'
        p = subprocess.call(["cellprofiler",
                         "--image-directory", ifoldername,
                        "--output-directory", ofoldername,
                        "--pipeline", cp_pipeline_downloaded_file,
                        "--file-list", checkpoint_file])
        print("Finished subprocessing")
        for filename in os.listdir(ofoldername):
            bucket.upload_file(ofoldername + '/' + filename, 'Output/' + filename)
            #print(filename)
        print("Upload Successful")
        import shutil
        shutil.rmtree(ifoldername)
        shutil.rmtree(ofoldername)  
    
    except botocore.exceptions.ClientError as e:        
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

def save_checkpoint(filename, ifoldername, npy1, npy2, npy3):
    checkpoint_file = ifoldername + '/' + "checkpoint.txt"
    f = open(checkpoint_file, "w+")
    for fn in filename:
        print("Saving Checkpoint for filename : ", fn)
        fname = 'file:///' + ifoldername + '/' + fn[8:]
        f.write(fname)
        f.write("\n")
    f.write('file:///' + npy1)
    f.write("\n")
    f.write('file:///' + npy2)
    f.write("\n")
    f.write('file:///' + npy3)
    f.write("\n")
    f.close()
    return checkpoint_file


if __name__ == '__main__':
    root_names = []
    # Get all the filenames from Testing directory which are not present in checkpoint.txt
    #sample filename: FOV_6x6/u26a_20x1.0_acq1_A2-Pos_021_021_ch1.tif
    filenames = get_objects_in_folder('FOV_6x6/')
    print('DOwnloaded files from S3 folder')
    s_filenames = sorted(filenames)
    arr_filenames = []
    img_set_count = int(len(s_filenames)/4)
    for i in range(img_set_count):
        #print(i)
        base_index = 4 * i
        arr_filenames.append([s_filenames[base_index], s_filenames[base_index+1], s_filenames[base_index+2], s_filenames[base_index+3]])
    #start = time.time()
        root_names.append(s_filenames[base_index][0:39])
    print(root_names)
    
    print("&&&&&&&&&&&&&&&&&&& bEFORE fargate processing &&&&&&&&&")
   
#fargate
#    cluster = FargateCluster(image="mansim23/cellprofiler:071320")
#    cluster = FargateCluster()
#    task_role_arn="arn:aws:iam::487949121534:user/Mansi",
#    execution_role_arn="arn:aws:iam::487949121534:role/ecsTaskExecutionRole",
#    n_workers=1,
#    scheduler_cpu=256,
#    scheduler_mem=512,
#    worker_cpu=256,
#    worker_mem=512,
#    scheduler_timeout="1 minute",)   
#    cluster.adapt(minimum_jobs=1, maximum_jobs=100)
#    client = Client(cluster.scheduler_address, processes = False)

#local
    cluster = LocalCluster()

#client
    client = Client(cluster.scheduler_address)
    print(client.scheduler_info()['services'])
    
#map functions
    futures = client.map(download_from_s3, root_names)
    print(len(futures))
    print([future.result() for future in futures])

#check final run
    print("&&&&&&&&&&######## after fargate computing ###########")

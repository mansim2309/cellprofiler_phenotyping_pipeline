import boto3

ACCESS_KEY = 'AKIAXDHAIW77BMWXFAVM'
SECRET_KEY = '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'
bucket_name = 'theriotbucket'

s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
bucket = s3_resource.Bucket(bucket_name)


def get_objects_in_folder(folderpath1, folderpath2, folderpath3):
    acq1 = {}
    acq2 = {}
    acq3 = {}
    objects1 = list(bucket.objects.filter(Prefix=folderpath1))
    for file in objects1:
        f = file.key.split('/')[2].split('MMStack_')
        if(len(f)>1):
            acq1[f[1]] = file.key

    objects2 = list(bucket.objects.filter(Prefix=folderpath2))
    for file in objects2:
        f = file.key.split('/')[2].split('MMStack_')
        if(len(f)>1):
            acq2[f[1]] = file.key

    objects3 = list(bucket.objects.filter(Prefix=folderpath3))
    for file in objects3:
        f = file.key.split('/')[2].split('MMStack_')
        if(len(f)>1):
            acq3[f[1]] = file.key

    # #common in acq1 and acq2
    # for k1 in acq1:
    #     for k2 in acq2:
    #         if(k1 == k2):
    #             print(acq2[k2])
    #
    # #common in acq2 and acq3
    # for k2 in acq2:
    #     for k3 in acq3:
    #         if(k2 == k3):
    #             print(acq3[k3])
    print(acq1)
    print(acq2)
    print(acq3)
    plate1 = set(acq1)
    plate2 = set(acq2)
    plate3 = set(acq3)
    print("Duplicates in Acq2")
    for name in plate1.intersection(plate2):
        print(acq2[name])
    print("Duplicates in Acq3")
    for name in plate2.intersection(plate3):
        print(acq3[name])

#filenames = get_objects_in_folder("2020-03-05_u26a_midiscreen/u26a_20x-0.75_DAPI-TRITC-Cy5-Ph_Channel_WholePlate_1/")
get_objects_in_folder("2020-03-05_u26a_midiscreen/u26a_20x-0.75_DAPI-TRITC-Cy5-Ph_Channel_WholePlate_1/", "2020-03-05_u26a_midiscreen/u26a_20x-0.75_DAPI-TRITC-Cy5-Ph_Channel_WholePlate_2/", "2020-03-05_u26a_midiscreen/u26a_20x-0.75_DAPI-TRITC-Cy5-Ph_Channel_WholePlate_3/")
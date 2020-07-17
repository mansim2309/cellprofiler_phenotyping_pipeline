-- To ls the number of files
aws s3 ls s3://theriotbucket/2020-03-05%2520u26a%2520midiscreen/u26a_20x-0.75_DAPI-TRITC-Cy5-Ph_WholePlate_3/ --recursive | find /c /v ""

-- To copy from local dir to S3
aws s3 cp u26a_20x-0.75_DAPI-TRITC-Cy5-Ph_WholePlate_3 s3://theriotbucket/2020-03-05%2520u26a%2520midiscreen/u26a_20x-0.75_DAPI-TRITC-Cy5-Ph_WholePlate_3 --recursive

-- To connect to S3
aws s3 sync s3-test s3://theriotbucket 
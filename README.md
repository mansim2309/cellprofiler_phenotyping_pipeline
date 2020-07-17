## 1. Created a Dockerfile that had all the dependencies to run python3 and cellprofiler -> Dockerfile_cellprofiler (/home/ec2-user/docker)

## 2. Created an docker image from the above Dockerfile: docker build - < Dockerfile_cellprofiler

## 3a. If using LocalCluster():
  ### (1) create a docker container from the above created image 
    #### (i) docker run -it -> creates a container id 
    #### (ii) docker start 
    #### (iii) docker excec -it bin/bash -> enters the docker container 
   ### (2) In parallel, mount a common folder that contains all the resources you need -> OPTIONAL 
    #### (i) --volume : -- ENTERED DOCKER 
   ### (3) Check code 
    #### (i) cd /input -> input is the folder that has been mounted and is shared with EC2 
    #### (ii) vim localcluster_071520.py -> view the code and validate that dask is creating workers for parallel computing. The function that we have parallelized is called "process_cellprofiler" 
   #### (4) python3 localcluster_071520.py -> run the code 
   #### (5) cd ../output -> View the results of cellprofiler segmentation 
   #### (6) docker commit -> Open EC2 is a separate tab and commit docker container 
   #### (7) exit docker

## 3b. If using Fargate(imageid): Runs directly on local/EC2. No docker dependency 
  ### (1) Run python script directly. The internal (automatic) steps are as follows: 
    #### (i) The code will read the dockerimage supplied to Fargate and automatically spin the number of workers requested. In our case, min of 10 and max 100. 
    #### (ii) Fargate internally runs docker on each of the workers that will execute the code and save the results 
    #### (iii) View the results directly on S3.

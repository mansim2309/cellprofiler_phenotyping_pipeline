cd ~/Desktop/theriot_lab/resources/


chmod 400 pythoncolormap.pem


ssh -i "~/Desktop/theriot_lab/resources/pythoncolormap.pem" ec2-user@ec2-3-19-32-218.us-east-2.compute.amazonaws.com


scp -i "~/Desktop/theriot_lab/resources/pythoncolormap.pem" -r ~/Desktop/theriot_lab/resources/images/ ec2-user@ec2-3-19-32-218.us-east-2.compute.amazonaws.com


C ~/Desktop/theriot_lab/resources/<file> ec2-user@ec2-3-19-32-218.us-east-2.compute.amazonaws.com



scp -i  "~/Desktop/theriot_lab/resources/pythoncolormap.pem" ec2-user@ec2-3-19-32-218.us-east-2.compute.amazonaws.com:~/Data/threshold.png ~/Desktop/theriot_lab/output/



# to run this script:
# cp deploy_project.py dir_of_pulumi_project/
# cd dir_of_pulumi_project
# source venv/bin/activate
# pulumi login
# export CUSTOMER=myapp
# python deploy_project.py --resource s3
# python deploy_project.py --resource ec2
# python deploy_project.py --resource eks

import os
import sys
import argparse
import shutil

# we use arguments to pass the value of types of aws resources to deploy
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--resource', help='resource to deploy in aws e.g. s3, ec2, eks')
# parse arguments otherwise show help
arg_value = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
print("deploying {}".format(arg_value.resource))


# we use var CUSTOMER instead of var PROJECT because projects already have their life in pulumi
try:  
   os.environ["CUSTOMER"]
except KeyError: 
   print ("Please set the environment variable CUSTOMER")
   sys.exit(1)

customer = os.environ["CUSTOMER"]
print("CUSTOMER: " + os.environ["CUSTOMER"])


# copy source code files
source = "../boilerplates/{}.py".format(arg_value.resource)
destination = "__main__.py"
shutil.copy(source, destination)


# Create infrastructure for every stage
stages = ["test", "dev", "prod"]
for stage in stages:
    print("########## Processing infrastructure for the following stage: " + stage + " ...")  

    os.system('pulumi stack init %s' % stage)
    os.system('pulumi stack select %s' % stage)
    os.system('pulumi stack ls')
    os.system('pulumi config set customer %s' % customer)
    os.system('pulumi config set ami ami-080e1f13689e07408')
    os.system('pulumi config set eks_arn arn:aws:iam::123456789011:role/eksClusterRole')
    # set config namespace to aws for standard aws vars
    os.system('pulumi config set aws:region us-east-1')
    os.system('pulumi preview')
    os.system('pulumi up --yes')
    os.system('pulumi stack')



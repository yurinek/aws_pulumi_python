# aws_pulumi_python

This project deploys AWS infrastructure resources using Pulumi + Python


## Prerequisits

- Linux OS
- Python 3.0+
- pip3
- AWS account
- AWS user role with permission to create an EKS cluster (id (arn) of this role will be provided by eks_arn variable)
- created account at app.pulumi.com for remote backend
- manually created pulumi project and its directory should exist
```
mkdir pulumi-test-project
cd pulumi-test-project
# following templates can be used
pulumi new aws-python --name pulumi-test-project --description "first project" --stack initialstack #(template used in this project)
# pulumi new kubernetes-aws-python --name pulumi-test-project --description "first project" --stack initialstack #(this template evaluates aws crosswalk provider)
```


## Install Pulumi

```
./install.sh
```


## Deploy project

```
cp deploy_project.py pulumi-test-project
cd pulumi-test-project
source venv/bin/activate
pulumi login
export CUSTOMER=myapp
# to deploy s3 buckets in 3 stages test, dev, prod
python deploy_project.py --resource s3
# to deploy ec2 vms in 3 stages test, dev, prod
python deploy_project.py --resource ec2
# to deploy eks k8s cluster in 3 stages test, dev, prod
python deploy_project.py --resource eks
```


## Destroy project

```
pulumi stack select test
pulumi destroy
pulumi stack select dev
pulumi destroy
pulumi stack select prod
pulumi destroy
```


## Comparison to plain Terraform

### Pulumi advantages

-   Pulumi automatically captures dependencies when you pass an output from one resource as an input to another resource
-   easier and better thought-out stages (environment) management than in Terraform:  
    Pulumi Stacks concept is easier than Terraform Workspaces.  
    in Terraform special workspace variable is needed for state file name to distinguish between stages, Pulumi does it automatically
-   Pulumi offers remote backend in their cloud by default. in Terraform its local backend by default.
-   Pulumi is open source and it uses common languages.
-   Secrets Management with encryption in the state file.
-   same code can be deployed in different stages (stacks) without the need for code change as randomly generated suffixes are prepended on aws resource names.
-   multiple Pulumi provider for the same cloud can be used e.g. for AWS there are: aws native, aws classic, aws crosswalk
-   bigger projects can be split up into separate files as python modules. 

### Pulumi disadvantages

-   partially no documentation on howto install pulumi python modules. depends on provider. each provider has its own documentation structure
-   yaml language doesnt support all the features unlike the other languages
-   in general Pulumi is more complex and less known tool than Terraform. Employees need to know at least one script language.
-   not possible to create a new pulumi project in a none interactive mode e.g. for CI/CD pipelines.
-   toggling between different stacks takes long as data is retrieved from Pulumi cloud.
-   many pulumi forum pages are not found but are indexed in web-search-engine
-   documentation of usage examples contains wrong syntax
-   documentation is ai generated and has many errors. it requires too much cpu power to be loaded in browser which takes too long
-   pulumi stack init as an upsert is not supported: if stack exists select it, if stack is absent then create it


## Tested with

pulumi version v3.111.1  
pulumi_aws-6.27.0-py3-none-any.whl

#!/bin/bash

image_name="yurinek/aws-iac-tools"


echo "########## Running container and gearing it up with current scripts..."

docker run -dit "$image_name" bash
container_id=$(docker container ls --latest --quiet)
dir_name=$(basename $(pwd))
# copy current directory to container  
docker cp . $container_id:/root/$dir_name
# copy aws profile to container
docker cp ~/.aws $container_id:/root/.aws


echo "########## Connecting to latest container..."

docker container exec -it $container_id bash











































#snippet-added

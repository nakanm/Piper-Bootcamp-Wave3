#!/usr/bin/env python3

import os
import boto3
import time
import datetime

thumb_path = "/home/ec2-user/Piper-Wave3/static/"

def upload_to_ECS(path, file, contenttype, acl):
    ecs_endpoint_url = "https://object.ecstestdrive.com"
    ecs_access_key_id = "your ECS access key id"
    ecs_secret_access_key = "your secret access key"
    ecs_bucket_name = "your bucket name"

    print("upload to ECS: " + file)

    s3 = boto3.resource("s3",
    endpoint_url = ecs_endpoint_url,
    aws_access_key_id = ecs_access_key_id,
    aws_secret_access_key = ecs_secret_access_key)

    s3.Bucket(ecs_bucket_name).upload_file(path + file, file,
    ExtraArgs={"ContentType": contenttype, "ACL": acl})

    print("Done")
  


if os.path.isdir(thumb_path):
    files = os.listdir(thumb_path)
    for filename in files:
       upload_to_ECS(thumb_path, filename, "image/png", "public-read")
    
print("Operation completed")

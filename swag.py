#!/usr/bin/python3

import boto3
import subprocess
import configloader as config

def run_remote_command(ip_address, command):
    print("Executing command on {}: {}".format(ip_address, command))
    return subprocess.check_output(["ssh", 
        "-i", config.get_private_key_file(),
        "-o", "StrictHostKeyChecking no",
        "{}@{}".format(config.get_user(), ip_address),
        command]).decode("utf-8")

def get_ip_address(instance, is_public_ip_for_ssh):
    if is_public_ip_for_ssh:
        return instance.public_ip_address

    return instance.private_ip_address

def find_instances(ec2, environment, service):
    # TODO implement a cache
    return ec2.instances.filter(Filters=[
        {"Name": "tag:env", "Values": [environment]},
        {"Name": "tag:Name", "Values": [service]}
        ])


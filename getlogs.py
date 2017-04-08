#!/usr/bin/python3

import boto3
import subprocess
import sys
import configloader as config
import common
import argparse
import datetime

# Define functions
def find_instances(ec2, environment, service):
    # TODO implement a cache
    return ec2.instances.filter(Filters=[
        {"Name": "tag:env", "Values": [environment]},
        {"Name": "tag:Name", "Values": [service]}
        ])

def formatted_date():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")

def find_ip_addresses(ec2, environment, service, is_public_ip_for_ssh):
    instances = find_instances(ec2, environment, service)
    return [common.get_ip_address(instance, is_public_ip_for_ssh) for instance in instances]

def retrieve_log(ip_address, log_file_location):
    print("Getting logs from " + ip_address)
    return common.run_remote_command(ip_address, "cat " + log_file_location)

def create_log(environment, service, ip_address, log_content):
    log_name = "{}_{}-{}-{}".format(environment, service, ip_address, formatted_date())
    return {"log_name": log_name, "log_content": log_content}

def save_log(output_location, log):
    filename = "{}/{}".format(output_location, log["log_name"])
    print("Saving result in " + filename)

    with open(filename, "w") as text_file:
        text_file.write(log["log_content"])

    return filename

def show_log(filename, output_application):
    print("Opening {} with {}".format(filename, output_application))
    subprocess.Popen([output_application, filename])

def main():
    # Deal with inputs
    if len(sys.argv) != 3:
        print("Usage: ./getlogs.py [ENVIRONMENT] [SERVICE NAME]")
        exit(1)

    environment = sys.argv[1]
    service = sys.argv[2]
    
    # Get EC2 client
    ec2 = boto3.resource("ec2")

    # Retrieve logs from instances
    ip_addresses = find_ip_addresses(ec2, environment, service, config.is_public_ip_for_ssh())

    print("Getting logs for service=[{}] in environment=[{}]".format(service, environment))
    logs = [create_log(environment, service, ip_address, 
        retrieve_log(ip_address, config.get_log_file_location())) for ip_address in ip_addresses]

    for log in logs:
        filename = save_log(config.get_output_location(), log)
        show_log(filename, config.get_output_application())

if __name__ == "__main__":
    main()

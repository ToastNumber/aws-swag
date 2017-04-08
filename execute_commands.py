#!/usr/bin/python3

import boto3
import subprocess
import sys
import configloader as config
import swag
import argparse
from datetime import datetime

# Define functions
def create_output_name(environment, service, ip_address, time):
    return "{}_{}-{}-{}".format(environment, service, ip_address, time.strftime("%Y-%m-%dT%H:%M"))
   
def save_output(output_location, output_name, output):
    filename = "{}/{}".format(output_location, output_name)
    print("Saving result in " + filename)

    with open(filename, "w") as text_file:
        text_file.write(output)

    return filename

def show_output(filename, output_application):
    print("Opening {} with {}".format(filename, output_application))
    subprocess.Popen([output_application, filename])

def main():
    # Deal with inputs
    args = sys.argv[1:]
    if not (len(args) == 3 or len(args) == 4):
        print("Usage: ./execute_command.py ENVIRONMENT SERVICE COMMAND [OUTPUT APPLICATION]")
        exit(1)

    environment = args[0]
    service = args[1]
    command = args[2]
    output_application = args[3] if len(args) == 4 else None
    
    ec2 = boto3.resource("ec2")

    for instance in swag.find_instances(ec2, environment, service):
        ip_address = swag.get_ip_address(instance, config.is_public_ip_for_ssh())
        output = swag.run_remote_command(ip_address, command)

        output_name = create_output_name(environment, service, ip_address, datetime.now())
        filename = save_output(config.get_output_location(), output_name, output)

        if output_application:
            show_output(filename, output_application)
        else:
            print("<======================================>")
            print("Displaying output for " + ip_address)
            print("----------------------------------------")
            print(output)

if __name__ == "__main__":
    main()

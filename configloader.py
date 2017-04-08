#!/usr/bin/python3

import yaml

def load_config():
    with open("config.yaml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

config = load_config()

def get_user():
    return config["user"]

def get_private_key_file():
    return config["private_key_file"]

def is_public_ip_for_ssh():
    return config["use_public_ip_for_ssh"]

def get_output_location():
    return config["output_location"]

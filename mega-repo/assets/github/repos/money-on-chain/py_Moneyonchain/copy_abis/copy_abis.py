#!/usr/bin/env python

# cd copy_abis
# python copy_abis.py --config <config_file.json>

import os
import json
import shutil
import argparse

# get named parameters
parser = argparse.ArgumentParser(description='Copy ABIs and bytecode from source folder to dest folder')
parser.add_argument('--config', type=str, help='config file (JSON)')
args = parser.parse_args()

# validate config file
if not os.path.isfile(args.config):
    exit("Invalid path: config")

# read config file
config = {}
with open(args.config, "r") as config_file:
    config = json.load(config_file)

# trim ending slashes
src = config["src"].rstrip("/")
dest = config["dest"].rstrip("/")

# validate directories
if not os.path.isdir(src):
    exit("Invalid path: src")

if not os.path.isdir(dest):
    exit("Invalid path: dest")

print("Copying ABIs and BIN:")
print("---------------------")
print(f"Source: {src}")
print(f"Destination: {dest}")
print(f"Config file: {args.config}")

# make sure dest exists
os.makedirs(dest, exist_ok=True)

# copy files
# list dir if (only files) and (ending with .json)
input_files = sorted([f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))
                        and f.endswith(".json")
                        and ("include" in config and f in config["include"])])

print(f"File count: {len(input_files)}")
print()
i = 1

for f_name in input_files:
    print(f"  [{i}] {f_name[:-5]}", end="")

    fsrc = os.path.join(src, f_name)
    fdest_abi = f_name.replace(".json", ".abi")
    fdest_bin = f_name.replace(".json", ".bin")

    with open(fsrc, "r") as json_file:
        data = json.load(json_file)

    # if not len(data['abi']):
    #     print(" -- [warning: empty ABI] ", end="")

    with open(os.path.join(dest, fdest_abi), "w") as abi_file:
        # read json and extract abi
        json.dump(data['abi'], abi_file, indent=2)

    if not len(data['bytecode']):
        print(" -- [warning: empty bytecode] ", end="")

    with open(os.path.join(dest, fdest_bin), "wt") as bin_file:
        # read json and extract bytecode
        bin_file.write(data['bytecode'])

    print(" -- OK")
    i = i + 1

print()
print("Done!")
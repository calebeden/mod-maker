###########################################
# Author: calebeden
# File: main.py
# Created on Fri Jun 17 2022
###########################################

import microblocks
import mobheads
import json


def main():
    option = input("Which version number would you like to increase? 0=Major 1=Minor 2=Patch ")
    while option not in ("0","1","2"):
        print(f"{option} is not a valid option. Please try again.")
        option = input("Which version number would you like to increase? 0=Major 1=Minor 2=Patch ")
    
    with open('version.json', 'r') as infile:
        previous_version = json.load(infile)
    version = [0,0,0]
    match option:
        case "0":
            version[0] = previous_version[0] + 1
        case "1":
            version[0] = previous_version[0]
            version[1] = previous_version[1] + 1
        case "2":
            version[0] = previous_version[0]
            version[1] = previous_version[1]
            version[2] = previous_version[2] + 1

    
    verify = input(f"Are you sure you want to change from version {previous_version} to {version} ")
    if verify.lower() == 'y':
        with open("version.json", "w") as outfile:
            json.dump(version, outfile)
        mobheads.main()
        microblocks.main()


if __name__ == "__main__":
    main()

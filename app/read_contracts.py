import os
import utils as utils

def read_contracts():
    # THE PATH TO THE BINARY INTERFACES
    # NOTE THAT THIS PATH REFLECTS THE DOCKER CONTAINER
    path = 'resources/contracts/'

    # FIND ALL CONTRACT ABI'S, THEN REMOVE MIGRATIONS
    files = os.listdir(utils.abs_dir_of_caller(path))

    latest = {}

    # LOOP THROUGH THE FILES
    for file in files:

        # EXTRACT THE FILENAME & OPEN THE JSON FILE
        header = file[0:-5].lower()
        content = utils.load_json(path + file)

        # EXTRACT THE NETWORK OPTIONS
        network_list = list(content['networks'].keys())

        # IF THE CONTRACT DOES NOT HAVE AN ADDRESS
        if len(network_list) == 0:
            address = 'undefined'

        # IF IT DOES, EXTRACT IT
        else:
            address = content['networks'][network_list[0]]['address']

        # INDEX THE ADDRESS & ABI UNDER THE FILENAME
        latest[header] = {
            'address': address,
            'abi': content['abi']
        }

    return latest

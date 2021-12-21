# IoT-Microservice
This is software intended to run on an IoT device to allow management remotely but indirecty from a user interface, over ethereum.
This is intended to be used with an [management UI](https://github.com/vinicentus/flutter_iot_ui) for the devices running this software. It interacts with a [private ethereum network](https://github.com/vinicentus/geth-docker) and [smart contracts deployed on it](https://github.com/vinicentus/oracle-manager). 

This software will run on a Raspberry Pi with vrious sensors connected. It will preiodicaly store measurements from those sensors and send them to a User Interface when requested.

Here is a diagram of the data flow when using storj as the backend:
![image](/docs/big%20storj%20sequence%20diagram.png)

## Getting started

### Prerequisites
A raspberry Pi running Raspberry Pi OS.
Any of the following sensors connected and installed:
* Sensirion SCD30, connected direclty to GPIO pins using i2c
* Sensirion SCD41, connected directly to GPIO pins using i2c
* Sensirion SPS30, connected through USB
* sensorion SVM30, connected through a sensirion sensor bridge, that is connected thourgh USB
    *  This has very limited support and is not recommended

python3, sqlite3 (both are either installed by default or can be installed using apt)

a running [geth ethereum chain](https://github.com/vinicentus/geth-docker)

An already deployed version of [Smart Contract Backend](https://github.com/vinicentus/oracle-manager). We need the files from this contract deployment because they contain their ABI and the addresses they have been deplyed to. This is generated automatically when deploying using truffle.

### Installation steps

* clone the repository, recursively with sumbodules, into a folder of your choice `git clone --recurse-submodules`.

* create a python venv and activate `python -m venv venv`, `source venv/bin/activate`

* if using the SCD41:
    * run [build.py](app/oracle/raspberry_pi_i2c_scd4x_python/build.py). This compiles the driver 

* if using SCD30:
    * TODO: (follow driver installation instructions)

* install all dependencies using `pip install –r requirements.txt`

* create the folder `app/oracle/secrets`

* generate RSA keys, run [generate_pems.py](app/oracle/generate_pems.py)

* change the shebang of all files that contain this line: `#!/home/pi/git-repos/IoT-Microservice/venv/bin/python3` to match your specific environment, this is needed for the next steps to work

* add the lines corresponding to your used sensors to `/etc/rc.local` from [rc.local](app/rc.local)
    * Remember to edit the paths to match your environment
    * run the added lines manually or restart device to make the changes take effect

* add necessary lines to crontab, run `sudo crontab -e`, then copy over the lines corresponding to your used sensors from [crontab](app/crontab). The crontabs should be active after saving and exiting the text editor.
    * Remember to edit the paths to match your environment

* copy over the the contracts folder with all the generated json ABI files from the deployment process into `app/resources/contracts/`. It should now contain a json file for every single contract, containing the contract's ABI and address

* edit the [init_settings.yaml](app/resources/init_settings.yaml) file to match the network configuration. The ethereum key used here must be, (and is by default), the same key that is used by the geth node that deploys the contracts, see node4 in [geth-docker](https://github.com/vinicentus/geth-docker). If you changed that key, copy it over to this file.

There are some additional setup steps that are detailed in the readme file of the [management UI](https://github.com/vinicentus/flutter_iot_ui).
### First time run
* activate your python venv if not already activated

* initialize smart contracts by `python3 init.py`

* Generate a config file for this device from the [UI](https://github.com/vinicentus/flutter_iot_ui) and copy it over to [device_settings.yaml](app/resources/device_settings.yaml), or edit the values already present.
    * If editing this yourself, make sure to use the same ethereum key and public address as for the UI. If you didn't already change it in the User Interface's `settings.json` file, then make sure to change this from the default value in both places.
 
### How to run
After initializing the smart contracts above, and configuring them using the [UI](https://github.com/vinicentus/flutter_iot_ui), you can start the main service that performs tasks using `python3 launcher.py`
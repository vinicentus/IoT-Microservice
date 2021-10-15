# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import utils as utils
import blockchain as blockchain_utils
import device as device_utils

# %% [markdown]
# ### LOAD RESOURCES

# %%
device_settings = utils.load_yaml('resources/device_settings.yaml')

# %%
latest = utils.load_json('resources/ABI.json')

# %% [markdown]
# ### CONNECT TO ETHEREUM GATEWAY

# %%
web3 = blockchain_utils.connect(device_settings)

# %% [markdown]
# ### SERIALIZE MANAGER CONTRACTS

# %%
user_manager = blockchain_utils.contract(
    latest['usermanager'], web3, device_settings)


# %%
oracle_manager = blockchain_utils.contract(
    latest['oraclemanager'], web3, device_settings)


# %%
task_manager = blockchain_utils.contract(
    latest['taskmanager'], web3, device_settings)


# %%
token_manager = blockchain_utils.contract(
    latest['tokenmanager'], web3, device_settings)


# %% [markdown]
# ### ADD A USER WITH THE ADDRESS FROM CONFIG.YAML

# %%
result = user_manager.write({
    'func': 'create',
    'params': []
})

print(result)

# %% [markdown]
# ### ADD AN ORACLE FOR THE CURRENT USER
# ### THIS USES THE HASH OF IDENTIFIER.YAML

# %%
# Create device using generated hash from idenifiers.yaml
oracle_device = device_utils.create(device_settings)


# %%
# Create device in contract
result = oracle_manager.write({
    'func': 'create',
    'params': [
        oracle_device.unique_id,
        1  # This sets the required price for a task on this device
    ]
})

print(result)


# %%
# FETCH & SERIALIZE ORACLE CONTRACT
temp_contract = blockchain_utils.contract({
    'address': oracle_manager.read({
        'func': 'fetch_oracle',
        'params': oracle_device.unique_id
    }),
    'abi': latest['oracle']['abi']
}, web3, device_settings)


# %%
# VERIFY ORACLE CONTRACT EXISTENCE
if temp_contract.address != '0x0000000000000000000000000000000000000000':
    oracle_device.set_contract(temp_contract)

else:
    print('THE ORACLE IS NOT REGISTERED, ABORTING..')
    sys.exit(0)


# %%
# Activate the device/oracle
# Note that this toggles the active status,
# and so can also be used to deactivate the oracle
result = oracle_device.write({
    'func': 'toggle_active',
    'params': []
})

print(result)


# %%
# Check that the oracle is active
active = oracle_device.read('active')
print(active)


# %%

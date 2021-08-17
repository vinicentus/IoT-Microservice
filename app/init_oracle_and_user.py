# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import utils as utils
import blockchain as blockchain_utils
import device as device_utils

# %% [markdown]
# ### LOAD RESOURCES

# %%
settings = utils.load_yaml('resources/settings.yaml')


# %%
latest = utils.load_json('resources/latest.json')

# %%
device_info = utils.load_yaml('resources/identifier.yaml')

# %% [markdown]
# ### CONNECT TO ETHEREUM GATEWAY

# %%
web3 = blockchain_utils.connect(settings)

# %% [markdown]
# ### SERIALIZE MANAGER CONTRACTS

# %%
user_manager = blockchain_utils.contract(latest['usermanager'], web3, settings)


# %%
oracle_manager = blockchain_utils.contract(
    latest['oraclemanager'], web3, settings)


# %%
task_manager = blockchain_utils.contract(latest['taskmanager'], web3, settings)


# %%
token_manager = blockchain_utils.contract(
    latest['tokenmanager'], web3, settings)


# %% [markdown]
# ### ADD A USER WITH THE ADDRESS FROM CONFIG.YAML

# %%
user_manager.write({
    'func': 'create',
    'params': []
})

# %% [markdown]
# ### ADD AN ORACLE FOR THE CURRENT USER
# ### THIS USES THE HASH OF IDENTIFIER.YAML

# %%
# Create device using generated hash from idenifiers.yaml
oracle_device = device_utils.create(device_info)

# Create device in contract
oracle_manager.write({
    'func': 'create',
    'params': [
        oracle_device.hash,
        1  # This sets the required price for a task on this device
    ]
})


# %%

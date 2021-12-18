#!/home/pi/git-repos/IoT-Microservice/venv/bin/python3
# coding: utf-8

# In[1]:


from oracle import main as oracle_software
import subprocess
import sys
import time
from websockets.exceptions import ConnectionClosedError

# In[2]:


#import nbimporter


# In[ ]:


import utils as utils
import blockchain as blockchain_utils
import device as device_utils


# ### LOAD RESOURCES

# In[ ]:


device_settings = utils.load_yaml('resources/device_settings.yaml')


# In[ ]:


# CONTAINER FOR DATA
latest = utils.read_contracts()


# ### CONNECT TO ETHEREUM GATEWAY

# In[ ]:


web3 = blockchain_utils.connect(device_settings)


# ### EXTRACT THE WHISPER API

# In[ ]:


# ### GENERATE A FRESH WHISPER ID

# In[ ]:


# ### CREATE DEVICE OUTLINE

# In[ ]:


oracle = device_utils.create(device_settings)


# ### SERIALIZE NECESSARY MANAGER CONTRACTS

# In[ ]:


oracle_manager = blockchain_utils.contract(
    latest['oraclemanager'], web3, device_settings)


# In[ ]:


task_manager = blockchain_utils.contract(
    latest['taskmanager'], web3, device_settings)


# ### FETCH & SERIALIZE ORACLE CONTRACT

# In[ ]:


temp_contract = blockchain_utils.contract({
    'address': oracle_manager.read({
        'func': 'fetch_oracle',
        'params': oracle.unique_id
    }),
    'abi': latest['oracle']['abi']
}, web3, device_settings)


# ### VERIFY ORACLE CONTRACT EXISTENCE

# In[ ]:


if temp_contract.address != '0x0000000000000000000000000000000000000000':
    oracle.set_contract(temp_contract)

else:
    print('THE ORACLE IS NOT REGISTERED, ABORTING..')
    sys.exit(0)


# ### GLOBAL TASK BACKLOG

# In[ ]:


raw = oracle.read('fetch_backlog')


# In[ ]:


backlog = utils.filter_backlog(raw)


# ### GLOBAL ACTIVE STATUS

# In[ ]:


active = oracle.read('active')


# ### UDATE DEVICE STATUS & DETAILS

# In[ ]:


def update_details():

    # FETCH GLOBAL VARS
    global active
    global backlog

    # EXTRACT RELEVANT VALUES
    latest_active = oracle.read('active')

    # IF ACTIVE STATUS HAS CHANGED
    if (latest_active != active):

        # UPDATE ACTIVE STATUS
        active = latest_active

        # SEND MSG
        print('ACTIVE STATUS CHANGED TO:', latest_active)

    # UPDATE BACKLOG
    raw_backlog = oracle.read('fetch_backlog')
    backlog = utils.filter_backlog(raw_backlog)


# ### UPDATE MIDDLEWARE

# In[ ]:


def update_middleware():

    # PRINT REACTION
    print('\nMIDDLEWARE UPDATE TRIGGERED')

    # TRIGGER UPDATE SCRIPT
    subprocess.call('./patcher')

    # CLOSE LANCHER
    sys.exit(0)


# ### PERFORM TASK

# In[ ]:


def perform_task(task, func):

    # SHOW MSG
    print('STARTING TASK:', task)

    # SERIALIZE THE TASK CONTRACT
    task_contract = blockchain_utils.contract({
        'address': task,
        'abi': latest['task']['abi']
    }, web3, device_settings)

    # FETCH & DECODE TASK PARAMS
    params = task_contract.read('params')
    decoded = utils.decode(params)

    try:
        # PERFORM ORACLE TASK
        result = func(task, decoded)

        # SUBMIT THE TASK RESULT
        task_manager.write({
            'func': 'complete',
            'params': [task, result]
        })
        # SHOW MSG
        print('TASK COMPLETED')
    except Exception as e:
         # TODO: don't return error info, because it might be sensitive info?
        errorString = 'TASK COMPLETED WITH ERROR: {}'.format(e)
        # TODO: format this as base64 and possibly encrypt it as well!
        task_manager.write({'func': 'complete',
                            'params': [task, errorString]})
        # SHOW MSG
        print(errorString)


# ### CONTRACT EVENTS

# In[ ]:


update_event = oracle.event('middleware')


# In[ ]:


modification_event = oracle.event('modification')


# ### WHISPER EVENT

# In[ ]:


# ### MIDDLEWARE EVENT LOOP

# In[6]:


print('AWAITING EVENTS...\n')

# DYNAMICALLY IMPORT THE ORACLE SOFTWARE
#oracle_software = import_file('oracle/main.py')
func = oracle_software.perform_task

while(True):

    # VARIABLE MODIFICATION EVENT
    for event in modification_event.get_new_entries():
        update_details()

    # UPDATE MIDDLEWARE EVENT
    for event in update_event.get_new_entries():
        update_middleware()

    # IF THE DEVICE IS SET TO ACTIVE
    if (active):

        # PERFORM TASKS IN BACKLOG
        for task in backlog:
            perform_task(task, func)


# In[ ]:

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


# ### GLOBAL DISCOVERY STATUS

# In[ ]:


discoverable = oracle.read('discoverable')


# ### GLOBAL DISCOVERY CONFIG

# In[ ]:


encoded = oracle.read('config')


# In[ ]:


discovery_config = utils.decode(encoded)


# ### UDATE DEVICE STATUS & DETAILS

# In[ ]:


def update_details():

    # FETCH GLOBAL VARS
    global active
    global discoverable
    global discovery_config
    global backlog

    # EXTRACT RELEVANT VALUES
    latest_active = oracle.read('active')
    latest_discoverable = oracle.read('discoverable')
    latest_config = utils.decode(oracle.read('config'))

    # IF ACTIVE STATUS HAS CHANGED
    if (latest_active != active):

        # UPDATE ACTIVE STATUS
        active = latest_active

        # SEND MSG
        print('ACTIVE STATUS CHANGED TO:', latest_active)

    # IF DISCOVERABLE STATUS HAS CHANGED
    if (latest_discoverable != discoverable):

        # UPDATE ACTIVE STATUS
        discoverable = latest_discoverable

        # SEND MSG
        print('DISCOVERABLE STATUS CHANGED TO:', latest_discoverable)

    # IF DISCOVERABLE STATUS HAS CHANGED
    if (latest_config != discovery_config):

        # UPDATE ACTIVE STATUS
        discovery_config = latest_config

        # SEND MSG
        print('DISCOVERY CONFIG CHANGED')

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

    # PERFORM ORACLE TASK
    result = func(task, decoded)

    # SUBMIT THE TASK RESULT
    try:
        task_manager.write({
            'func': 'complete',
            'params': [task, result]
        })
        # SHOW MSG
        print('TASK COMPLETED')
    except Exception as e:
        errorString = 'TASK COMPLETED WITH ERROR: {}'.format(e)
        # TODO: format this as base64 and possibly encrypt it as well!
        task_manager.write({'func': 'complete',
                            'params': [task, errorString]})
        # SHOW MSG
        print(errorString)


# ### DISCOVERY RESPONSES

# In[ ]:


def process_message(event):

    # SERIALIZE EVENT PARAMS
    author = web3.toHex(event['sig'])
    payload = web3.toText(event['payload'])

    # DECODE THE PAYLOAD
    data = utils.decode(payload)

    # REQUIRED KEYS FOR VALID MESSAGE
    required = ['type', 'discovery']

    # DECODED KEYS
    keys = list(data.keys())

    # THE REQUEST KEYWORD FOR THE PAYLOAD TYPE
    keyword = 'request'

    # IF THE KEYSETS MATCH & THE TYPE IS A REQUEST
    if (required == keys and data['type'] == keyword):

        # CHECK MATCHES IN DISCOVERY PARAMS
        discovery_result = utils.compare_discovery(
            data['discovery'], discovery_config)

        # IF EVERYTHING MATCHED
        if (discovery_result.count(False) == 0):

            # SHOW MSG
            print('DISCOVERY REQUEST DETECTED')

            # ENCODE A JSON RESPONSE
            response = utils.encode({
                'type': 'response',
                'source': payload,
                'oracle': oracle.unique_id
            })

            # SLEEP FOR 2 SECONDS
            time.sleep(2)

            # RESPOND TO REQUEST
            shh.post({
                'symKeyID': device_settings['whisper']['symkey'],
                'payload': web3.toHex(text=response),
                'topic': web3.toHex(text=device_settings['whisper']['topic']),
                'sig': whisper_id,
                'powTarget': 2.5,
                'powTime': 2
            })


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

#!/home/pi/IoT-Microservice/venv/bin/python3
# coding: utf-8

# In[7]:


import json
import hashlib


# ### CREATE NEW DEVICE

# In[5]:


class create():
    def __init__(self, data):
        self.hash = hash_id(data)
    
    # LOCATE & SET DEVICE CONTRACT ADDRESS
    def set_contract(self, contract):
        self.contract = contract
    
    # REDIRECT TO PARENT
    def read(self, details):
        return self.contract.read(details)
    
    # REDIRECT TO PARENT
    def write(self, details):
        return self.contract.write(details)
    
    # REDIRECT TO PARENT
    def event(self, name):
        return self.contract.event(name)


# ### HASH DEVICE IDENTIFIER

# In[13]:


def hash_id(data):
    
    # REMOVE WHITESPACES
    to_string = json.dumps(data, separators=(',', ':'))
    
    # ENCODE THE STRING WITH UTF8
    encoded = to_string.encode('utf-8')
    
    # HASH ENCODED DATA
    hashed = hashlib.sha256(encoded).hexdigest()
    
    return hashed


# In[ ]:





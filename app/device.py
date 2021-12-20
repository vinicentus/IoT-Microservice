# In[7]:


import json
import hashlib


# ### CREATE NEW DEVICE

# In[5]:


class create():
    def __init__(self, data):
        self.unique_id = json_encode(data)
    
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


# ### DEVICE IDENTIFIER

# In[13]:


def json_encode(data):

    id_data = data['id']
    
    # REMOVE WHITESPACES
    to_string = json.dumps(id_data, separators=(',', ':'))
    
    return to_string


# In[ ]:





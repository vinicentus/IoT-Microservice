#!/usr/bin/env python
# coding: utf-8

# In[2]:


import utils as utils
import blockchain as blockchain


# ### LOAD RESOURCES

# In[3]:

# We need to use special credentials with more permisisons here...
settings = utils.load_yaml('resources/init_settings.yaml')


# In[4]:


latest = utils.load_json('resources/ABI.json')


# ### CONNECT TO ETHEREUM GATEWAY

# In[5]:


web3 = blockchain.connect(settings)


# ### SERIALIZE MANAGER CONTRACTS

# In[6]:


user_manager = blockchain.contract(latest['usermanager'], web3, settings)


# In[7]:


oracle_manager = blockchain.contract(latest['oraclemanager'], web3, settings)


# In[8]:


task_manager = blockchain.contract(latest['taskmanager'], web3, settings)


# In[9]:


token_manager = blockchain.contract(latest['tokenmanager'], web3, settings)


# ### INIT TOKEN MANAGER

# In[10]:


token_symbol = 'ArcaCoin'
token_price = 5000
token_capacity = 10000


# In[11]:


token_manager.write({
    'func': 'init',
    'params': [
        token_symbol,
        token_price,
        token_capacity,
        task_manager.address
    ]
})


# ### INIT TASK MANAGER

# In[12]:


task_token_fee = 2


# In[13]:


task_manager.write({
    'func': 'init',
    'params': [
        task_token_fee,
        user_manager.address,
        oracle_manager.address,
        token_manager.address
    ]
})


# ### INIT USER MANAGER

# In[14]:


user_manager.write({
    'func': 'init',
    'params': [task_manager.address]
})


# ### INIT ORACLE MANAGER

# In[15]:


oracle_manager.write({
    'func': 'init',
    'params': [
        user_manager.address,
        task_manager.address
    ]
})


# In[ ]:





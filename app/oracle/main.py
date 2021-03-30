#!/home/matti/IoT-Microservice/venv/bin/python3.8
# coding: utf-8

import oracle.serviceManager as sm
# ### PERFORM THE TASK

# In[1]:


def perform_task(task, params):
    print('\tORACLE TRIGGERED')
    print(params)
    #data = sm.execute(params)
    return 'foo'


# In[ ]:





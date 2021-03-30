#!/usr/bin/env python
# coding: utf-8

from serviceManager import execute
# ### PERFORM THE TASK

# In[1]:


def perform_task(task, params):
    print('\tORACLE TRIGGERED')
    data = execute(params)
    return data


# In[ ]:





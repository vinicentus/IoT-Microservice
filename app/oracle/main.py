#!/usr/bin/env python3
# coding: utf-8

import oracle.serviceManager as sm
# ### PERFORM THE TASK

# In[1]:


def perform_task(task, params):
    print('\tORACLE TRIGGERED')
    print(params)
    data = sm.execute(**params)
    print(type(data))
    return data[:10]


# In[ ]:





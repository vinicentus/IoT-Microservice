
#!/home/matti/IoT-Microservice/venv/bin/python3.8
# coding: utf-8

import serviceManager
# ### PERFORM THE TASK

# In[1]:


def perform_task(task, params):
    print('\tORACLE TRIGGERED')
    data = serviceManager.execute(params)
    return data


# In[ ]:





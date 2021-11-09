#!/home/pi/git-repos/IoT-Microservice/venv/bin/python3
# coding: utf-8

from . import serviceManager as sm
# ### PERFORM THE TASK

# In[1]:


def perform_task(task, params):
    print('\tORACLE TRIGGERED')
    print(params)
    try:
        # Check for invalid data
        # In the future we might want to start rate limiting if we get many tasks with invalid parameters.
        # TODO: we should probably retry some tasks
        data = sm.execute(**params)
        print(type(data))
        return data
    except TypeError as error:
        # TODO: format this as base64 and possibly encrypt it as well!
        errorString = 'Error in task excecution: {}'.format(error)
        print(errorString)
        return errorString


# In[ ]:

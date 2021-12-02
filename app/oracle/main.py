#!/home/pi/git-repos/IoT-Microservice/venv/bin/python3
# coding: utf-8

from . import serviceManager as sm
from . import storj_test as storj_manager
# ### PERFORM THE TASK

# In[1]:


def perform_task(task: str, params: dict):
    print('\tORACLE TRIGGERED')
    print(params)
    try:
        # Check for invalid data
        # In the future we might want to start rate limiting if we get many tasks with invalid parameters.
        # TODO: we should probably retry some tasks

        # Parse data to select handler
        if (params['task_return_type'] == 'storj'):
            print('Task type is STORJ!')

            # TODO: add params
            # Use experimental storj service manager
            data = storj_manager.execute_storj()
        else:
            # Remove new task_return_type value because the old execute function can't handle it
            params.pop('task_return_type')

            # Use original ethereum-based upload method
            data = sm.execute(**params)
        return data
    except TypeError as error:
        # TODO: format this as base64 and possibly encrypt it as well!
        errorString = 'Error in task excecution: {}'.format(error)
        print(errorString)
        return errorString


# In[ ]:

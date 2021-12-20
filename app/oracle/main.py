from . import serviceManager as sm
from . import storjServiceManager as storj_manager
# ### PERFORM THE TASK

# In[1]:


def perform_task(task: str, params: dict):
    print('\tORACLE TRIGGERED')
    print(params)

    # TODO: Check for invalid data
    # TODO: In the future we might want to start rate limiting if we get many tasks with invalid parameters.
    # TODO: we should probably retry some tasks

    # Parse data to select handler
    if (params['task_return_type'] == 'storj'):
        print('Task type is STORJ!')
        # Remove new task_return_type value because this new storj execute function can't handle it
        params.pop('task_return_type')

        # Use experimental storj service manager
        data = storj_manager.execute_storj(**params)
    else:
        # Remove new task_return_type value because the old execute function can't handle it
        params.pop('task_return_type')

        # Use original ethereum-based upload method
        data = sm.execute(**params)
    return data


# In[ ]:

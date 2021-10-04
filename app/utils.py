#!/home/pi/IoT-Microservice/venv/bin/python3
# coding: utf-8

# In[43]:


import yaml
import json
import base64
import hashlib
import zipfile
import os
import inspect

# In[2]:


def abs_dir_of_caller(path):
    # Absolute path for the directory of the file of the caller
    # Example: this function is called from another file /home/example/project/test.py. Then the absolute_dir_path is /home/example/project/
    # old method: os.path.dirname(__file__)
    absolute_file_path = inspect.stack()[1].filename
    absolute_dir_path = os.path.dirname(absolute_file_path)
    complete_path = os.path.join(absolute_dir_path, path)
    return complete_path


# ### LOAD YAML FILE

# In[3]:


def load_yaml(path):
    complete_path = abs_dir_of_caller(path)

    with open(complete_path, mode='r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


# ### LOAD & SAVE JSON FILE

# In[4]:


def load_json(path):
    complete_path = abs_dir_of_caller(path)
    
    with open(complete_path) as json_file:
        return json.load(json_file)


# In[5]:


def save_json(data, path):
    complete_path = abs_dir_of_caller(path)
    
    with open(complete_path, 'w') as outfile:
        json.dump(data, outfile)


# ### ENCODE & DECODE FOR BASE64

# In[6]:


def encode(data):
    
    # STRINGIFY & CONVERT TO BYTES
    stringified = json.dumps(data)
    to_bytes = str.encode(stringified)
    
    # ENCODE
    encoded = base64.b64encode(to_bytes)
    
    # RETURN AS STRING
    return encoded.decode()


# In[7]:


def decode(compressed):
    
    # ATTEMPT TO DECODE & PARSE AS JSON
    try:
        to_bytes = base64.b64decode(compressed)
        return json.loads(to_bytes)
    
    # OTHERWISE, RETURN EMPTY OBJECT
    except:
        return {}


# ### FILTER ZEROS FROM BACKLOG

# In[8]:


def filter_backlog(data):
    
    # FILTER ZEROS
    filtered = filter(lambda x: x != '0x0000000000000000000000000000000000000000', data)
    
    # CONVERT TO LIST & RETURN
    return list(filtered)


# ### COMPARE DISCOVERY PARAMS

# In[9]:


def compare_discovery(data, base):
    
    # RESULT CONTAINER
    result = []
    
    # LOOP THROUGH DATA KEYS
    for key in data:
        
        # IF THE KEY EXISTS IN THE BASE DICT
        if key in base:
            
            # IF THE VALUE IS SAME IN BOTH DATASET
            if data[key] == base[key]:
                result.append(True)
                
            # OTHERWISE, DEFAULT TO FALSE
            else:
                result.append(False)
                
        # OTHERWISE, DEFAULT TO FALSE
        else:
            result.append(False)
            
    # FINALLY RETURN RESULT
    return result


# ### CHECKSUM STUFF

# In[40]:


def generate_checksum(path):
    with open(path, 'rb') as file:
        return hashlib.sha256(file.read()).hexdigest()


# In[11]:


def verify_checksums(prefix):
    
    # LOAD CHECKSUMS & EXTRACT FILENAMES
    checksums = load_json(prefix + 'checksums.json')
    files = list(checksums.keys())
    
    # RESULT CONTAINER
    results = []
    
    # LOOP THROUGH FILES
    for file in files:
        
        # GENERATE CHECKSUM FOR FILE
        checksum = generate_checksum(prefix + file)
        
        # VERIFY & PUSH RESULT
        results.append(checksum == checksums[file])
    
    # IF ALL FILES PASS, RETURN TRUE
    if (results.count(False) == 0):
        return True
    
    # OTHERWISE, RETURN FALSE
    return False


# ### ZIP / UNZIP DIRECTORY

# In[13]:


def unzip(path, target):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(target)


# In[42]:


def create_zip(files, prefix, path):
    with zipfile.ZipFile(prefix + path, 'w') as zipF:
        for file in files:
            zipF.write(os.path.join(prefix, file), file, compress_type=zipfile.ZIP_DEFLATED)


# ### DECRYPT PRIVATE KEY

# In[17]:


def decrypt_key(path, password, web3):
    with open(path) as keyfile:
        encrypted_key = keyfile.read()
        private_key = web3.eth.account.decrypt(encrypted_key, password)

        return web3.toHex(private_key)


# ### GETHER FILES IN DIRECTORY

# In[4]:


def gather_files(directory):
    container = []
    
    # LOOP THROUGH FILES
    for subdir, dirs, files in os.walk(directory[:-1]):
        for file in files:
            
            # CONSTRUCT FULL PATH
            filepath = subdir + os.sep + file

            # REMOVE THE PREFIX
            filepath = filepath.replace(directory, '')
            
            # APPEND TO THE CONTAINER
            container.append(filepath)
            
    return container


# In[ ]:





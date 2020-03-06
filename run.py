import os
import json
from generic import GenericObject

'''
    EXAMPLE 1: Load JSON file from disk and convert to an object

    Load up niclist.json and convert it to JSON
'''
loaded_json = None
with open("niclist.json", 'r') as input_file:
    filedata = input_file.readlines()
    filedata = "\n".join(filedata)
    loaded_json = json.loads(filedata)

if loaded_json:
    '''
        Now that we have the JSON object, we can create a Generic object which will 
        enable us to treat it like a class with properties.
    '''
    nic_data = GenericObject(loaded_json)

    '''
        Test teh find_property by looking for the property whitelist. Given the JSON
        file that is loaded, this SHOULD return 3 of them.
    '''
    print("FIND PROPERTY: whitelist")
    white_lists = GenericObject.find_property(nic_data,"whitelist")
    for lit in white_lists:
        print(lit.whitelist)

    '''
        Now just simply dump it to see what it looks like
    '''
    print("\nDUMP OBJECT: NIC LIST")
    GenericObject.dumpObject(nic_data)

    '''
        Now we can iterate over it, assumit it has the information we expected
    '''
    print("\nEXAMPLE 1:")
    if GenericObject.has_property(nic_data,["nic_list"]):
        for nic in nic_data.nic_list:
            print("NIC : ", nic.name)
            for ip in nic.whitelist:
                print("  ", ip)

'''
    EXAMPLE 2: Create a dictionary and turn it into a class that you can access
    properties by name
'''
print("\nEXAMPLE 2:")
dumm_dict = {
    "name" : "1289378F67A",
    "location" : "eastus",
    "skus" : {
        "normal" : "abcdefc",
        "advanced" : "123fsd"
    }
}

dummy_generic = GenericObject(dumm_dict)

print("name =", dummy_generic.name,"location =", dummy_generic.location)
if GenericObject.has_property(dummy_generic, ["skus", "advanced"]):
    print("skus.advanced =", dummy_generic.skus.advanced)

'''
    EXAMPLE 3: Create a list
'''
print("\nEXAMPLE 3:")
dummy_list = [1,2,3,4]
dummy_generic = GenericObject(dummy_list)
print(dummy_generic.list)
'''
    EXAMPLE 4: Using Azure CLI

    NOTE: YOU MUST HAVE THE AZURE-CLI INSTALLED AND BE 
          LOGGED INTO AN AZURE ACCOUNT.
'''
print("\nEXAMPLE 4 : REST CALL PARSING (AZURE)")

stm = os.popen("az account list --all")
content = "".join(stm.readlines())
acct_list = json.loads(content)
# Now we have the JSON as a dictionary/list
acct_generic = GenericObject(acct_list)

# Find all of the sub ID's, but since we know name is there where 
# there is an id, lets print that too!
obs = GenericObject.find_property(acct_generic, "id")
print("Total Subscriptions : ", len(obs))
for ob in obs:
    print(ob.id,'=',ob.name)
    break

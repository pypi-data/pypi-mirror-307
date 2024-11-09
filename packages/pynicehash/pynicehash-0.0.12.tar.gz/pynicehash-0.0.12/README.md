# pynicehash
This is a library to interact with the nicehash API v2 in python.

# feature
For now pynicehash support only rig management, get and set mining rig state.

# usage

```
nh = pynicehash.NiceHash(api_url, organisation_id, api_key, api_secret)

rigs = nh.get_rigs()

for rig in rigs:
  print (rig.name)
  for device in rig.devices:
    print (device.name)
```
# configuration
When creating the NiceHash object you have to pass your connection credential.
**api_url** you have two choice:
* https://api-test.nicehash.com for testing, in testing you probably will not have any mining rig.
* https://api2.nicehash.com for production.

**organisation_id**
The organisation_id is the the id you can find in you page where you create you api key.

**api_key**
You have to select miningg rig permission when creating the API key
The key you generate in you account profile

**api_secret**
The secret you generate in you account profile

## screenshot
Here is a screen shot of the location for the organisation id and where to create the API key.
![api_creation](https://github.com/nslythe/pynicehash/raw/main/assets/api_creation.png)

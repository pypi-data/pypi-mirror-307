from pynicehash.miningdevice import MiningDevice

class MiningRig(object):
    def __init__(self, nicehash_api, data):
        self.nicehash_api = nicehash_api
        self.__set_data(data)
    
    def __set_data(self, data):
        self.hasV4Rigs = data.get("hasV4Rigs", False)
        self.is_managed = data.get("type", "UNMANAGED") == "MANAGED"
        self.id = data["rigId"]
        self.type = data["type"]
        self.name = "unnamed"
        if "name" in data:
            self.name = data["name"]
        else:
            if self.hasV4Rigs:
                if "mmv" in data["v4"]:
                    if "workerName" in data["v4"]["mmv"]:
                        self.name = data["v4"]["mmv"]["workerName"]

        self.status_time = data["statusTime"]
        self.miner_status = data["minerStatus"]
        if "groupName" in data:
            self.group_name = data["groupName"]
        if "unpaidAmount" in data:
            self.unpaid_amount = data["unpaidAmount"]
        if "profitability" in data:
            self.profitability = data["profitability"]
        if "localProfitability" in data:
            self.local_profitability = data["localProfitability"]
        
        if data["type"] == "MANAGED":
            self.devices: MiningDevice = []
            device_list = None
            if self.hasV4Rigs:
                device_list = data["v4"]["devices"]
            else:
                device_list = data["devices"]

            for d in device_list:
                self.devices.append(MiningDevice(self.nicehash_api, self, d))

    def update(self):
        self.__set_data(self.nicehash_api.get_rig_detail(self.id))



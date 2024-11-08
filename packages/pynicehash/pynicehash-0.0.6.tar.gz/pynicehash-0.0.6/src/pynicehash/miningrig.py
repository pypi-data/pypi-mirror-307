from pynicehash.miningdevice import MiningDevice

class MiningRig(object):
    def __init__(self, nicehash_api, data):
        self.nicehash_api = nicehash_api
        self.__set_data(data)
    
    def __set_data(self, data):
        self.id = data["rigId"]
        self.type = data["type"]
        self.name = "unnamed"
        if "name" in data:
            self.name = data["name"]
        else:
            if "v4" in data:
                if "mmv" in data["v4"]:
                    if "workerName" in data["v4"]["mmv"]:
                        self.name = data["v4"]["mmv"]["workerName"]

        self.status_time = data["statusTime"]
        self.miner_status = data["minerStatus"]
        self.group_name = data["groupName"]
        self.unpaid_amount = data["unpaidAmount"]
        self.profitability = data["profitability"]
        self.local_profitability = data["localProfitability"]
        
        self.devices: MiningDevice = []
        for d in data["v4"]["devices"]:
            self.devices.append(MiningDevice(self.nicehash_api, self, d))

    def update(self):
        self.__set_data(self.nicehash_api.get_rig_detail(self.id))




import enum
from . import mining_status

class DeviceMiningStatusEnum(enum.Enum):
    OFFLINE = -1
    INACTIVE = 1
    MINING = 2
    BENCHMARKING = 3
    DISABLED = 4

class MiningDevice(object):
    def __init__(self, nicehash_api, parent_rig, data):
        self.nicehash_api = nicehash_api
        self.parent_rig = parent_rig
        self.id = data["dsv"]["id"]
        self.name = data["dsv"]["name"]
        self.device_type = data["dsv"]["deviceClass"]
        self.status = DeviceMiningStatusEnum(data["mdv"]["state"])
        
        self.temperature = -1
        for o in data["odv"]:
            if o["key"] == "Temperature":
                self.temperature = o["value"]
                break

        self.load = -1
        for o in data["odv"]:
            if o["key"] == "Lost":
                self.load = o["value"]
                break

        # self.rpm = data["revolutionsPerMinute"]
        # self.rpm_percentage = data["revolutionsPerMinutePercentage"]
        # self.power_mode = data["powerMode"]["enumName"]
        # self.power_usage = data["powerUsage"]
        # self.intensity = data["intensity"]["enumName"]
    
    def start_mining(self):
        self.nicehash_api.set_device_status(self, mining_status.MiningStatus.START)

    def stop_mining(self):
        self.nicehash_api.set_device_status(self, mining_status.MiningStatus.STOP)

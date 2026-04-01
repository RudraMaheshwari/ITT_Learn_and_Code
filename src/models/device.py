from src.config.constants import DEVICE_STATUS_ACTIVE, WIFI_STATUS_CONNECTED

class Device:

    def __init__(self, device_id: str, status: str, wifi_status: str):
        self.device_id = device_id
        self._status = status
        self._wifi_status = wifi_status

    def is_active(self) -> bool:
        return self._status == DEVICE_STATUS_ACTIVE

    def is_connected(self) -> bool:
        return self._wifi_status == WIFI_STATUS_CONNECTED


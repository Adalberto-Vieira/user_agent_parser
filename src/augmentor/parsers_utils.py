import pandas as pd
from enum import Enum
from user_agents import parse


class DeviceTypes(Enum):
    MOBILE = "Mobile"
    COMPUTER = "Computer"
    TABLET = "Tablet"
    OTHER = "Other"


class ParserUtils:
    def parse_user_agent(self, agent_str):
        try:
            if agent_str == '""':
                raise Exception("Empty double quotation")
            user_agent = parse(agent_str)
            details = {
                "Device Type": self._select_device_type(user_agent),
                "Browser Type": user_agent.browser.family,
                "Browser Version": user_agent.browser.version_string,
                "Failure": False,
            }
        except Exception as e:
            details = {
                "Device Type": None,
                "Browser Type": None,
                "Browser Version": None,
                "Failure": True,
            }
            print(f"Failed processing of a row with error: {e}")
        return pd.Series(details)

    @classmethod
    def _select_device_type(cls, user_agent):
        if user_agent.is_mobile:
            return DeviceTypes.MOBILE.value
        if user_agent.is_pc:
            return DeviceTypes.COMPUTER.value
        if user_agent.is_tablet:
            return DeviceTypes.TABLET.value
        return DeviceTypes.OTHER.value

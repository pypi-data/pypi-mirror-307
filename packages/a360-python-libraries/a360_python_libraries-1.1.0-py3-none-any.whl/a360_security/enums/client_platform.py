from enum import Enum


class ClientPlatform(str, Enum):
    WEB = "web"
    MOBILE = "mobile"
    DESKTOP = "desktop"

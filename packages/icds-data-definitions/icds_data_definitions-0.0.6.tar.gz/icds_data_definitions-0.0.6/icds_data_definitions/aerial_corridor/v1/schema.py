from pydantic import BaseModel
from enum import Enum

# Version: 0.0.1
DATA_DEFINITIONS_VERSION = "0.0.1"

class AvailabilityEnum(str, Enum):
    unknown = 'unknown'
    healthy = 'healthy'
    unhealthy = 'unhealthy'


class VersionAvailabilityRead(BaseModel):
    "A class to hold version and availability of DSS"
    
    version: str
    availability: AvailabilityEnum


from typing import Dict
from pydantic import BaseModel
from metrik.connectors.common.types import ConnectorTypes


class AWSTimestreamConfig(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str
    database_name: str
    retention_options: Dict[str, int] = {
        "MemoryStoreRetentionPeriodInHours": 1,
        "MagneticStoreRetentionPeriodInDays": 365,
    }
    reporter_type: ConnectorTypes=ConnectorTypes.AWSTimestream
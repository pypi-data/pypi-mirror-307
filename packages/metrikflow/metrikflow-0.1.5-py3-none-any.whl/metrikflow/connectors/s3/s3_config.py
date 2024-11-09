from pydantic import BaseModel
from metrikflow.connectors.common.types import ConnectorTypes


class S3Config(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str
    buckets_namespace: str
    reporter_type: ConnectorTypes=ConnectorTypes.S3
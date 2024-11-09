from pydantic import BaseModel
from metrikflow.connectors.common.types import ConnectorTypes
from typing import Optional


class AWSLambdaConfig(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str
    reporter_type: ConnectorTypes=ConnectorTypes.AWSLambda
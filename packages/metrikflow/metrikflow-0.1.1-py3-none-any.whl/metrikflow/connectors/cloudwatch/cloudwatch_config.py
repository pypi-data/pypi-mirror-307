from typing import List
from pydantic import BaseModel
from metrikflow.connectors.common.types import ConnectorTypes


class _CloudwatchTarget(BaseModel):
    arn: str
    id: str

class CloudwatchConfig(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str
    iam_role_arn: str
    schedule_rate: str=None
    cloudwatch_targets: List[_CloudwatchTarget]
    aws_resource_arns: List[str]=[]
    cloudwatch_source: str='hedra'
    submit_timeout: int=60
    reporter_type: ConnectorTypes=ConnectorTypes.Cloudwatch
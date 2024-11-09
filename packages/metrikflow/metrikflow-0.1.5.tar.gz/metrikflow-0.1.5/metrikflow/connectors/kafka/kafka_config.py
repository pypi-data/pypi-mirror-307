from typing import Any, Dict, Optional

from pydantic import BaseModel

from metrikflow.connectors.common.types import ConnectorTypes


class KafkaConfig(BaseModel):
    host: str='localhost:9092'
    client_id: str='metrikflow'
    group_id: str='metrikflow'
    metrics_partition: int=0
    compression_type: Optional[str]
    timeout: int=1000
    idempotent: bool=True
    options: Dict[str, Any]={}
    reporter_type: ConnectorTypes=ConnectorTypes.Kafka
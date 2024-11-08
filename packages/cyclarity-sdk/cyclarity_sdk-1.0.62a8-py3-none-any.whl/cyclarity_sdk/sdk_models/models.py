from typing import Optional
from pydantic import BaseModel
from enum import Enum
from cyclarity_sdk.sdk_models.types import ExecutionStatus  # noqa

''' Test step definitions'''


class ExecutionMetadata(BaseModel):
    execution_id: str
    agent_id: Optional[str] = None
    test_id: str
    step_id: Optional[str] = None
    step_name: Optional[str] = None
    step_version: Optional[str] = None
    iteration_index: Optional[str] = "0"


class ExecutionState(BaseModel):
    '''Data structure to be send via topic::execution-state'''
    execution_metadata: ExecutionMetadata
    percentage: int
    status: ExecutionStatus
    error_message: Optional[str] = ''


class RunningEnvType(str, Enum):
    IOT = "iot_device"
    BATCH = "batch"


'''Execution definitions'''


class PackageType(str, Enum):
    # Supported types for test step deployment
    PIP = "PIP"
    ZIP = "ZIP"


class MessageType(str, Enum):
    # Supported types for test step deployment
    LOG = "LOG"
    TEST_STATE = "TEST_STATE"
    EXECUTION_STATE = "EXECUTION_STATE"
    FINDING = "FINDING"
    TEST_ARTIFACT = "TEST_ARTIFACT"
    EXECUTION_OUTPUT = "EXECUTION_OUTPUT"

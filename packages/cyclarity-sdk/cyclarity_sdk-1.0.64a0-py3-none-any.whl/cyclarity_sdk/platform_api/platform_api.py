from cyclarity_sdk.platform_api.Iplatform_connector import IPlatformConnectorApi
from cyclarity_sdk.platform_api.connectors.cli_connector import CliConnector
from cyclarity_sdk.sdk_models.artifacts import TestArtifact, TestReportDescription, ArtifactType
from cyclarity_sdk.sdk_models.findings import Finding, PTFinding, FindingModelType
from cyclarity_sdk.sdk_models import ExecutionState, ExecutionStatus
from cyclarity_sdk.sdk_models import MessageType, ExecutionMetadata
from typing import Optional
import warnings


def deprecated(func):
    def wrapper(*args, **kwargs):
        warnings.warn(f"{func.__name__} is deprecated", category=FutureWarning)
        return func(*args, **kwargs)
    return wrapper


class PlatformApi:
    def __init__(
        self,
        platform_connector: Optional[IPlatformConnectorApi] = None
    ):
        if not platform_connector:
            platform_connector = CliConnector()
        self.set_connector(platform_connector)

    def get_execution_meta_data(self) -> ExecutionMetadata:
        return self.platform_connector.get_execution_meta_data()

    def set_execution_meta_data(self, execution_metadata: ExecutionMetadata):
        self.platform_connector.set_execution_meta_data(execution_metadata)

    def set_connector(self, platform_connector: IPlatformConnectorApi):
        # set the platform communicator
        self.platform_connector = platform_connector

    def send_test_report_description(self, description: str):  # noqa
        execution_metadata = self.platform_connector.get_execution_meta_data()

        test_report_description = TestReportDescription(
            type=ArtifactType.REPORT_DESCRIPTION,
            description=description
        )

        artifact = TestArtifact(
            execution_metadata=execution_metadata,
            type=MessageType.TEST_ARTIFACT,
            data=test_report_description
        )

        return self.platform_connector.send_artifact(artifact)

    def send_finding(self, pt_finding: PTFinding):
        execution_metadata = self.platform_connector.get_execution_meta_data()

        finding = Finding(
            metadata=execution_metadata,
            model_type=FindingModelType.PT_FINDING,
            data=pt_finding,
            type=MessageType.FINDING
        )

        return self.platform_connector.send_finding(finding)

    @deprecated
    def send_execution_state(self, percentage: int, status: ExecutionStatus, error_message: str = ""):  # noqa
        execution_metadata = self.platform_connector.get_execution_meta_data()
        execution_state = ExecutionState(
            execution_metadata=execution_metadata,
            percentage=percentage,
            status=status,
            error_message=error_message
        )

        return self.platform_connector.send_state(execution_state)

    def report_test_progress(self, percentage: int):
        '''
        use this function to reflect the progress (in percentage) of the step in the platform.
        '''
        execution_metadata = self.platform_connector.get_execution_meta_data()
        execution_state = ExecutionState(
            execution_metadata=execution_metadata,
            percentage=percentage,
            status=ExecutionStatus.RUNNING
        )
        return self.platform_connector.send_state(execution_state)

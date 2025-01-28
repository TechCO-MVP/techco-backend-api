import os
import boto3

from src.domain.profile import ProfileFilterProcessQueryDTO


def start_filter_profile_use_case(profile_process_dto: ProfileFilterProcessQueryDTO) -> dict:
    """Start filter profile use case."""
    step_functions = boto3.client("stepfunctions")
    state_machine_arn = os.environ.get("PROFILE_FILTER_PROCESS_ARN")

    response = step_functions.start_execution(
        stateMachineArn=state_machine_arn, input=profile_process_dto.model_dump_json()
    )

    if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise Exception("Error starting state machine")

    # save the process id in the database and the dto
    # TODO: Save in dynamodb
    return {"process_id": response["executionArn"]}

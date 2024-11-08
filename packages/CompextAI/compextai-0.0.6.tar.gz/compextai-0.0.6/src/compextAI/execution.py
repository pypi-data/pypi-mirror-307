from compextAI.api.api import APIClient

class ThreadExecutionStatus:
    status: str

    def __init__(self, status:str):
        self.status = status

def get_thread_execution_status(client:APIClient, thread_execution_id:str) -> str:
    response = client.get(f"/threadexec/{thread_execution_id}/status")

    status_code: int = response["status"]
    data: dict = response["data"]

    if status_code != 200:
        raise Exception(f"Failed to get thread execution status, status code: {status_code}, response: {data}")
    
    return ThreadExecutionStatus(data["status"])

def get_thread_execution_response(client:APIClient, thread_execution_id:str) -> dict:
    response = client.get(f"/threadexec/{thread_execution_id}/response")

    status_code: int = response["status"]
    data: dict = response["data"]

    if status_code != 200:
        raise Exception(f"Failed to get thread execution response, status code: {status_code}, response: {data}")
    
    return data

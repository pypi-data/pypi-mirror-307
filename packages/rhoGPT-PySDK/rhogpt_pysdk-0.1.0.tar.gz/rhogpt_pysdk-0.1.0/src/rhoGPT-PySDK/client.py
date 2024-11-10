from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

import requests


class RhoGPTError(Exception):
    """Base exception for RhoGPT SDK."""


class UnauthorizedError(RhoGPTError):
    """Exception raised for unauthorized access."""


class NotFoundError(RhoGPTError):
    """Exception raised when a resource is not found."""


class BadRequestError(RhoGPTError):
    """Exception raised for bad requests."""


class ServerError(RhoGPTError):
    """Exception raised for server-side errors."""


@dataclass
class User:
    id: str
    email: str
    name: str
    provider: str
    providerUserId: str
    createdAt: str
    updatedAt: str


@dataclass
class APIKey:
    id: str
    userId: str
    createdAt: str
    expiresAt: Optional[str]
    revoked: bool


@dataclass
class Task:
    id: str
    planId: str
    title: str
    description: str
    taskType: str
    status: str
    result: str
    feedback: str
    createdAt: str
    updatedAt: str
    order: int


@dataclass
class Plan:
    id: str
    projectId: str
    summary: str
    currentStage: str
    createdAt: str
    updatedAt: str
    tasks: List[Task] = field(default_factory=list)


@dataclass
class Project:
    id: str
    instruction: str
    status: str
    summary: str
    createdAt: str
    updatedAt: str
    plan: Plan
    userId: str


@dataclass
class Progress:
    totalTasks: int
    completedTasks: int
    currentTask: Optional[Task]
    percentage: float


def _handle_response(response: requests.Response) -> Any:
    """
    Handle the HTTP response, raising exceptions for error codes.

    :param response: The HTTP response object.
    :return: The JSON-decoded response content.
    """
    if response.status_code in [200, 201]:
        try:
            return response.json()
        except ValueError:
            return response.text
    elif response.status_code == 400:
        raise BadRequestError(response.json().get("error", "Bad Request"))
    elif response.status_code == 401:
        raise UnauthorizedError(response.json().get("error", "Unauthorized"))
    elif response.status_code == 404:
        raise NotFoundError(response.json().get("error", "Not Found"))
    elif response.status_code == 429:
        raise RhoGPTError(response.json().get("error", "Too Many Requests"))
    elif 500 <= response.status_code < 600:
        raise ServerError(response.json().get("error", "Internal Server Error"))
    else:
        raise RhoGPTError(f"Unexpected status code: {response.status_code}")


class RhoGPTClient:
    def __init__(self, api_key: str, base_url: str = "https://rhogpt.ai/api", timeout: int = 30):
        """
        Initialize the RhoGPTClient with an API key.

        :param api_key: Your API key for authentication.
        :param base_url: The base URL of the rhoGPT API.
        :param timeout: Timeout for HTTP requests in seconds.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def create_project(self, instruction: str) -> Project:
        """
        Create a new project with the given instruction.

        :param instruction: The initial instruction or description for the project.
        :return: The created Project object.
        """
        url = f"{self.base_url}/projects"
        payload = {"instruction": instruction}
        response = requests.post(url, headers=self.headers, json=payload, timeout=self.timeout)
        data = _handle_response(response)
        project_id = data.get("projectId")
        plan_data = data.get("plan")
        plan = Plan(**plan_data) if plan_data else None
        return Project(
            id=project_id,
            instruction=instruction,
            status="",  # Status might be part of the plan or needs to be fetched separately
            summary="",
            createdAt="",
            updatedAt="",
            plan=plan,
            userId="",  # User ID might require an additional call to get authenticated user
        )

    def get_project(self, project_id: str) -> Project:
        """
        Retrieve a specific project by its ID.

        :param project_id: The UUID of the project to retrieve.
        :return: The Project object.
        """
        url = f"{self.base_url}/projects/{project_id}"
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = _handle_response(response)
        project_data = data.get("project")
        return Project(**project_data) if project_data else None

    def update_project_plan(self, project_id: str, feedback: str) -> Plan:
        """
        Update a project's plan based on user feedback.

        :param project_id: The UUID of the project whose plan is to be updated.
        :param feedback: The user-provided feedback to update the plan.
        :return: The updated Plan object.
        """
        url = f"{self.base_url}/projects/{project_id}/plan"
        payload = {"feedback": feedback}
        response = requests.put(url, headers=self.headers, json=payload, timeout=self.timeout)
        data = _handle_response(response)
        plan_data = data.get("plan")
        return Plan(**plan_data) if plan_data else None

    def get_project_plan(self, project_id: str) -> Plan:
        """
        Retrieve the plan associated with a specific project.

        :param project_id: The UUID of the project whose plan is to be retrieved.
        :return: The Plan object.
        """
        url = f"{self.base_url}/projects/{project_id}/plan"
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = _handle_response(response)
        plan_data = data.get("plan")
        return Plan(**plan_data) if plan_data else None

    def regenerate_project_plan(self, project_id: str) -> Plan:
        """
        Regenerate a project's plan based on the current state without user feedback.

        :param project_id: The UUID of the project whose plan is to be regenerated.
        :return: The regenerated Plan object.
        """
        url = f"{self.base_url}/projects/{project_id}/regenerate"
        response = requests.post(url, headers=self.headers, timeout=self.timeout)
        data = _handle_response(response)
        plan_data = data.get("plan")
        return Plan(**plan_data) if plan_data else None

    def reorder_tasks(self, project_id: str, task_order: List[str]) -> Plan:
        """
        Reorder the tasks within a project's plan based on the provided order of task IDs.

        :param project_id: The UUID of the project whose tasks are to be reordered.
        :param task_order: A list of task UUIDs in the desired order.
        :return: The updated Plan object.
        """
        url = f"{self.base_url}/projects/{project_id}/plan/reorder"
        payload = {"taskOrder": task_order}
        response = requests.post(url, headers=self.headers, json=payload, timeout=self.timeout)
        data = _handle_response(response)
        plan_data = data.get("plan")
        return Plan(**plan_data) if plan_data else None

    def create_task(self, project_id: str, description: str) -> Task:
        """
        Create a new task within a specific project.

        :param project_id: The UUID of the project where the task will be created.
        :param description: The description of the task to be created.
        :return: The created Task object.
        """
        url = f"{self.base_url}/projects/{project_id}/tasks"
        payload = {"description": description}
        response = requests.post(url, headers=self.headers, json=payload, timeout=self.timeout)
        data = _handle_response(response)
        task_data = data.get("task")
        return Task(**task_data) if task_data else None

    def delete_task(self, project_id: str, task_id: str) -> str:
        """
        Delete a specific task from a project.

        :param project_id: The UUID of the project containing the task.
        :param task_id: The UUID of the task to be deleted.
        :return: Confirmation message.
        """
        url = f"{self.base_url}/projects/{project_id}/tasks/{task_id}"
        response = requests.delete(url, headers=self.headers, timeout=self.timeout)
        data = _handle_response(response)
        return data.get("message")

    def execute_task(self, project_id: str, task_id: str, user_input: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a specific task within a project.

        :param project_id: The UUID of the project containing the task.
        :param task_id: The UUID of the task to be executed.
        :param user_input: The input provided by the user for task execution (required for certain task types).
        :return: A dictionary containing the updated Task object and project completion status.
        """
        url = f"{self.base_url}/projects/{project_id}/tasks/{task_id}/execute"
        payload = {}
        if user_input is not None:
            payload["userInput"] = user_input
        response = requests.post(url, headers=self.headers, json=payload, timeout=self.timeout)
        data = _handle_response(response)
        return data

    def provide_task_feedback(self, project_id: str, task_id: str, feedback: str) -> Dict[str, Any]:
        """
        Provide feedback on a specific task.

        :param project_id: The UUID of the project containing the task.
        :param task_id: The UUID of the task to provide feedback on.
        :param feedback: The feedback provided for the task.
        :return: A dictionary containing a confirmation message and the updated Task object.
        """
        url = f"{self.base_url}/projects/{project_id}/tasks/{task_id}/feedback"
        payload = {"feedback": feedback}
        response = requests.post(url, headers=self.headers, json=payload, timeout=self.timeout)
        data = _handle_response(response)
        return data

    def get_project_progress(self, project_id: str) -> Progress:
        """
        Retrieve the progress of a specific project.

        :param project_id: The UUID of the project whose progress is to be retrieved.
        :return: The Progress object.
        """
        url = f"{self.base_url}/projects/{project_id}/progress"
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = _handle_response(response)
        progress_data = data.get("progress")
        return Progress(**progress_data) if progress_data else None

import os
from time import sleep
import requests


def send_rest_api_request(method, endpoint, data=None):
    api_url = os.getenv("TANGENT_API_URL", "https://api.tangent.works")
    license_key = os.getenv("TANGENT_LICENSE", "")
    headers = {"Authorization": "Bearer " + license_key}

    response = requests.request(
        method, f"{api_url}{endpoint}", headers=headers, files=data
    )
    response.raise_for_status()

    return response


def wait_for_job_to_finish(job_type, job_id):
    i = 900
    while i > 0:
        status_response = send_rest_api_request("GET", f"/{job_type}/{job_id}")
        job_status = status_response.json()["status"]
        if job_status == "Finished":
            return job_status
        if job_status == "Failed":
            try:
                error_message = status_response.json()["log"][-1]["message"]
            except:
                error_message = "Unknown error"
            raise ValueError(error_message)
        i -= 1
        sleep(2)
    raise ValueError("API response timeout reached")

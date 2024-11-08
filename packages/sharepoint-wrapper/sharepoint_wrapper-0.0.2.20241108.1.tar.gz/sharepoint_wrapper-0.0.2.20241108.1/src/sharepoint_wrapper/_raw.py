import json
from datetime import datetime
from functools import wraps
from io import BytesIO
import traceback

import urllib3
from urllib import parse

from sharepoint_wrapper._constants import SCOPE


def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        return result

    return wrapper


http = urllib3.PoolManager()


def get_graph_token(
    tenant_domain: str, client_id: str, client_secret: str
) -> tuple[str, datetime]:
    url = f"https://login.microsoftonline.com/{tenant_domain}/oauth2/v2.0/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": SCOPE,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    try:
        response = http.request(
            "POST",
            url,
            headers=headers,
            body=parse.urlencode(data),
            retries=False,  # Disable automatic retries
        )
        response_data = json.loads(response.data.decode("utf-8"))

        if response.status != 200:
            error_description = response_data.get("error_description", "Unknown error")
            raise Exception(error_description)

        token = response_data.get("access_token", None)
        expires_in = response_data.get("expires_in", None)  # in seconds
        if expires_in is not None:
            expires_in = datetime.fromtimestamp(datetime.now().timestamp() + expires_in)

        return token, expires_in

    except Exception as e:
        raise Exception(f"Error during token retrieval: {str(e)}")


def get_site(tenant: str, site: str, token: str) -> str:
    url = (
        f"https://graph.microsoft.com/v1.0/sites/{tenant}.sharepoint.com:/sites/{site}"
    )
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = http.request(
            "GET",
            url,
            headers=headers,
            retries=False,  # Disable automatic retries
        )
        response_data = json.loads(response.data.decode("utf-8"))

        if response.status != 200:
            error_description = response_data["error"]["message"]
            raise Exception(error_description)

        site_id = response_data.get("id", None)
        return site_id

    except Exception as e:
        raise Exception(f"Invalid Site: {str(e)}")


def get_drives(site_id: str, token: str) -> list[str]:
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = http.request(
            "GET",
            url,
            headers=headers,
            retries=False,  # Disable automatic retries
        )
        response_data = json.loads(response.data.decode("utf-8"))

        if response.status != 200:
            error_description = response_data["error"]["message"]
            raise Exception(error_description)

        raw_drives = response_data.get("value", None)
        drives = []
        if raw_drives is not None:
            drives = [(d.get("id"), d.get("name")) for d in raw_drives]

        return drives

    except Exception as e:
        raise Exception(f"Invalid Site: {str(e)}")


def get_children(
    drive_id, token, base_path: str | None = None, category: str | None = None
):
    """
    Get Children.
    None : All | folder : Folders only | file : Files only
    """
    if base_path is not None and not base_path.startswith("/"):
        raise Exception("Base path must always begin with a slash /")
    base_path = "" if base_path is None else f":{base_path}:"
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root{base_path}/children"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = http.request(
            "GET",
            url,
            headers=headers,
            retries=False,  # Disable automatic retries
        )
        response_data = json.loads(response.data.decode("utf-8"))

        if response.status != 200:
            error_description = response_data["error"]["message"]
            raise Exception(error_description)

        raw_drives = response_data.get("value", None)
        drives = []
        if raw_drives is not None:
            drives = [
                (
                    d.get("name"),
                    d.get("webUrl"),
                    "folder" if "folder" in d else "file" if "file" in d else "unknown",
                )
                for d in raw_drives
                if (category is None) or (category is not None and category in d)
            ]

        return drives

    except Exception as e:
        raise Exception(f"Invalid Site: {str(e)}")


def get_file(
    drive_id: str,
    token: str,
    file_name: str,
    base_path: str | None = None,
) -> BytesIO:
    """
    Get File.
    """
    if base_path is not None and not base_path.startswith("/"):
        raise Exception("Base path must always begin with a slash /")

    path = (base_path or "") + "/" + file_name

    path = f":{path}:"
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root{path}/content"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = http.request(
            "GET",
            url,
            headers=headers,
            # retries=False,  # Disable automatic retries
        )

        if response.status != 200:
            response_data = json.loads(response.data.decode("utf-8"))
            error_description = response_data["error"]["message"]
            raise Exception(error_description)

        return BytesIO(response.data)

    except Exception as e:
        raise Exception(f"Invalid Site: {str(e)}")


def write_file(
    drive_id: str, token: str, file_content: BytesIO, file_name: str, base_path: str
) -> dict:
    """
    Write file to a location.
    """
    if base_path is not None and not base_path.startswith("/"):
        raise Exception("Base path must always begin with a slash /")

    path = (base_path or "") + "/" + file_name

    path = f":{path}:"
    url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root{path}/content"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = http.request(
            "PUT",
            url,
            headers=headers,
            body=file_content,
            # retries=False,  # Disable automatic retries
        )

        response_data = json.loads(response.data.decode("utf-8"))

        if response.status not in (201, 200):
            error_description = response_data["error"]["message"]
            raise Exception(error_description)

        return response_data

    except Exception as e:
        print(traceback.format_exc())
        raise Exception(f"Error uploading file: {str(e)}")

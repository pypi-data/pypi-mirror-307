from io import BytesIO
from typing import List
import requests
from sharepoint_utils.connection import SharePointConnection


def _get_id_from_name(parent_element_json, name, site=False):
    """Returns id for matching object with given name/displayName in SharePoint API response object"""
    if site:
        var = "displayName"
    else:  # drives, files
        var = "name"
    match = [x["id"] for x in parent_element_json["value"] if x[var] == name]
    assert len(match) == 1
    return match[0].split(",")[-1]


def _get_subsite_id(sharepoint_connection: SharePointConnection, subsite_name):
    parent_element_json = requests.get(
        sharepoint_connection.api_base_url + "sites",
        headers=sharepoint_connection.graph_auth_header,
    ).json()
    return _get_id_from_name(parent_element_json, subsite_name, site=True)


def _get_drive_id(sharepoint_connection: SharePointConnection, drive, subsite_id=None):
    request_url = (
        sharepoint_connection.api_base_url + "drives"
        if subsite_id is None
        else sharepoint_connection.api_base_url + f"sites/{subsite_id}/drives"
    )
    parent_element = requests.get(
        request_url, headers=sharepoint_connection.graph_auth_header
    )
    _check_json(parent_element)
    return _get_id_from_name(parent_element.json(), drive)


def _get_item_id(
    sharepoint_connection: SharePointConnection, item_path, drive_id, subsite_id=None
):
    request_url = (
        sharepoint_connection.api_base_url + f"drives/{drive_id}/root:/{item_path}"
        if subsite_id is None
        else sharepoint_connection.api_base_url
        + f"sites/{subsite_id}/drives/{drive_id}/root:/{item_path}"
    )
    response = requests.get(
        request_url,
        headers=sharepoint_connection.graph_auth_header,
    )
    assert response.ok, f"Requested item returned status code {response.status_code}"
    return response.json()["id"]


def _check_json(response):
    try:
        response.json()
    except ValueError:
        raise AssertionError(
            f"Response with status code {response.status_code} does not contain valid JSON data"
        )


def get_item(
    sharepoint_connection: SharePointConnection,
    drive: str,
    item_path: str,
    subsite=None,
    **kwargs,
) -> BytesIO:
    """
    Get a SharePoint file

    Parameters
    ----------
    * sharepoint_connection (SharePointConnection): connection to SharePoint
    * drive (str): name of drive
    * file_path (str): path to the file
    * subsite (str, optional): name of subsite where file is located, defaults to None
    * kwargs (optional): any other keyword args to pass to requests get API call

    Returns
    -------
    * BytesIO object with file content
    """
    subsite_id = (
        None if subsite is None else _get_subsite_id(sharepoint_connection, subsite)
    )
    drive_id = _get_drive_id(sharepoint_connection, drive, subsite_id=subsite_id)
    request_url = (
        sharepoint_connection.api_base_url + f"drives/{drive_id}/root:/{item_path}"
        if subsite is None
        else sharepoint_connection.api_base_url
        + f"sites/{subsite_id}/drives/{drive_id}/root:/{item_path}"
    )
    response = requests.get(
        request_url, headers=sharepoint_connection.graph_auth_header, **kwargs
    )
    assert response.ok, f"Requested item returned status code {response.status_code}"
    _check_json(response)
    download_url = response.json()["@microsoft.graph.downloadUrl"]
    download_response = requests.get(download_url)
    assert (
        download_response.ok
    ), f"Item download returned status code {download_response.status_code}"
    return BytesIO(download_response.content)


def write_item(
    sharepoint_connection: SharePointConnection,
    drive: str,
    data,
    content_type: str,
    item_name: str,
    folder_path=None,
    subsite=None,
):
    """
    Write a file to a SharePoint location

    Parameters
    ----------
    * sharepoint_connection (SharePointConnection): connection to SharePoint
    * drive (str): name of drive
    * data (Dictionary, list of tuples, bytes, or file-like object): data content of file
    * content_type (str): file content type (e.g. "text/csv")
    * item_name (str): name of file to write to SharePoint
    * folder_path (str, optional): path/to/sharepoint/folder/in/drive, defaults to None
    * subsite (str, optional): name of subsite where folder is located, defaults to None

    Returns
    -------
    * None
    """
    subsite_id = (
        None if subsite is None else _get_subsite_id(sharepoint_connection, subsite)
    )
    drive_id = _get_drive_id(sharepoint_connection, drive, subsite_id=subsite_id)
    request_url = (
        sharepoint_connection.api_base_url
        + f"drives/{drive_id}/root:/{folder_path}/{item_name}:/content"
        if subsite is None
        else sharepoint_connection.api_base_url
        + f"sites/{subsite_id}/drives/{drive_id}/root:/{folder_path}/{item_name}:/content"
    )
    headers = {**sharepoint_connection.graph_auth_header, "Content-Type": content_type}
    response = requests.put(
        request_url,
        headers=headers,
        data=data,
    )
    assert (
        response.ok
    ), f"Attempting to write item returned status code {response.status_code}"


def move_item(
    sharepoint_connection: SharePointConnection,
    drive: str,
    item_name: str,
    origin_parent_dir=None,
    target_parent_dir=None,
    subsite=None,
    allow_overwrite: bool = True,
):
    """
    Move a SharePoint item from one location to another

    Parameters
    ----------
    * sharepoint_connection (SharePointConnection): connection to SharePoint
    * drive (str): name of drive
    * item_name (str): name of the item to be moved
    * origin_parent_dir (str, optional): current path to item, defaults to None
    * target_parent_dir (str, optional): proposed new path to item, defaults to None
    * subsite (str, optional): name of subsite where item is located, defaults to None
    * allow_overwrite (bool, optional): whether to overwrite an existing item when moving, defaults to True

    Returns
    -------
    * None
    """
    subsite_id = (
        None if subsite is None else _get_subsite_id(sharepoint_connection, subsite)
    )
    drive_id = _get_drive_id(sharepoint_connection, drive, subsite_id=subsite_id)
    item_path = (
        item_name if origin_parent_dir is None else f"{origin_parent_dir}/{item_name}"
    )
    request_url = (
        sharepoint_connection.api_base_url + f"drives/{drive_id}/root:/{item_path}"
        if subsite is None
        else sharepoint_connection.api_base_url
        + f"sites/{subsite_id}/drives/{drive_id}/root:/{item_path}"
    )
    target_folder_id = _get_item_id(
        sharepoint_connection, target_parent_dir, drive_id, subsite_id=subsite_id
    )
    data = {
        "parentReference": {"id": target_folder_id},
        "name": item_name,
    }
    params = {
        "@microsoft.graph.conflictBehavior": ("replace" if allow_overwrite else "fail"),
    }
    response = requests.patch(
        request_url,
        headers=sharepoint_connection.graph_auth_header,
        json=data,
        params=params,
    )
    if allow_overwrite:
        assert (
            response.ok
        ), f"Attempting to move item returned status code {response.status_code}; item not moved"
    else:
        assert response.ok or (
            response.json()["error"]["code"] == "nameAlreadyExists"
        ), f"Attempting to move item returned status code {response.status_code}; no nameAlreadyExists error"


def copy_item(
    sharepoint_connection: SharePointConnection,
    drive: str,
    origin_item_name: str,
    target_parent_dir: str,
    origin_parent_dir=None,
    target_item_name=None,
    subsite=None,
    allow_overwrite: bool = True,
):
    """
    Copy a SharePoint item from one location to another

    Parameters
    ----------
    * sharepoint_connection (SharePointConnection): connection to SharePoint
    * drive (str): name of drive
    * origin_item_name (str): name of the item to be copied
    * target_parent_dir (str): proposed new path to item
    * origin_parent_dir (str, optional): current path to item, defaults to None
    * target_item_name (str, optional): name for the new copy, defaults to None
    * subsite (str, optional): name of subsite where item is located, defaults to None
    * allow_overwrite (bool, optional): whether to overwrite an existing item when copying, defaults to True

    Returns
    -------
    * None
    """
    subsite_id = (
        None if subsite is None else _get_subsite_id(sharepoint_connection, subsite)
    )
    drive_id = _get_drive_id(sharepoint_connection, drive, subsite_id=subsite_id)

    origin_item_path = (
        origin_item_name
        if origin_parent_dir is None
        else f"{origin_parent_dir}/{origin_item_name}"
    )
    origin_item_id = _get_item_id(
        sharepoint_connection, origin_item_path, drive_id, subsite_id
    )
    target_dir_id = _get_item_id(
        sharepoint_connection, target_parent_dir, drive_id, subsite_id
    )

    request_url = (
        sharepoint_connection.api_base_url
        + f"drives/{drive_id}/items/{origin_item_id}/copy"
        if subsite is None
        else sharepoint_connection.api_base_url
        + f"sites/{subsite_id}/drive/items/{origin_item_id}/copy"
    )
    drive_item = {
        "parentReference": {"driveId": drive_id, "id": target_dir_id},
        "name": (
            f"{origin_item_name}" if target_item_name is None else f"{target_item_name}"
        ),
    }
    params = {
        "@microsoft.graph.conflictBehavior": ("replace" if allow_overwrite else "fail"),
    }
    response = requests.post(
        request_url,
        headers=sharepoint_connection.graph_auth_header,
        json=drive_item,
        params=params,
    )
    if allow_overwrite:
        assert (
            response.ok
        ), f"Attempting to move item returned status code {response.status_code}; item not moved"
    else:
        assert response.ok or (
            response.json()["error"]["code"] == "nameAlreadyExists"
        ), f"Attempting to move item returned status code {response.status_code}; no nameAlreadyExists error"


def get_items_in_path(
    sharepoint_connection: SharePointConnection,
    drive: str,
    folder_path=None,
    subsite=None,
    **kwargs,
) -> List[str]:
    """
    List file names in SharePoint location

    Parameters
    ----------
    * sharepoint_connection (SharePointConnection): connection to SharePoint
    * drive (str): name of drive
    * folder_path (str, optional): path/to/sharepoint/folder/in/drive, defaults to None
    * subsite (str, optional): name of subsite where folder is located, defaults to None
    * kwargs (optional): any other keyword args to pass to requests get API call

    Returns
    -------
    * List of file names as strings
    """
    subsite_id = (
        None if subsite is None else _get_subsite_id(sharepoint_connection, subsite)
    )
    drive_id = _get_drive_id(sharepoint_connection, drive, subsite_id=subsite_id)
    if folder_path is None:
        request_url = (
            sharepoint_connection.api_base_url + f"drives/{drive_id}/root/children"
            if subsite is None
            else sharepoint_connection.api_base_url
            + f"sites/{subsite_id}/drives/{drive_id}/root/children"
        )
    else:
        request_url = (
            sharepoint_connection.api_base_url
            + f"drives/{drive_id}/root:/{folder_path}:/children"
            if subsite is None
            else sharepoint_connection.api_base_url
            + f"sites/{subsite_id}/drives/{drive_id}/root:/{folder_path}:/children"
        )
    response = requests.get(
        request_url, headers=sharepoint_connection.graph_auth_header, **kwargs
    )
    assert (
        response.ok
    ), f"Request returned status code {response.status_code} for given path"
    _check_json(response)
    return [item["name"] for item in response.json()["value"]]


def get_items_date_in_path(
    sharepoint_connection: SharePointConnection,
    drive: str,
    folder_path: str,
    incl_children: bool = True,
    subsite: str = None,
    **kwargs,
) -> List[dict]:
    """
    Lists dictionary items that include name and last modified date in SharePoint location or file.

    Parameters
    ----------
    * sharepoint_connection (SharePointConnection): connection to SharePoint
    * drive (str): name of drive
    * folder_path (str): path/to/sharepoint/folder/in/drive
    * incl_children (bool, optional): a boolean of whether the API should look for children
        within folder path parameter (i.e. is a folder?), defaults to True
    * subsite (str, optional): name of subsite where folder is located, defaults to None
    * kwargs (optional): any other keyword args to pass to requests get API call

    Returns
    ----------
    List[dict]: A list of dictionaries including the keys:
        name (str): name of the file
        lastModifiedDateTime (datetime): date that the file was last modified
    """
    subsite_id = (
        None if subsite is None else _get_subsite_id(sharepoint_connection, subsite)
    )
    drive_id = _get_drive_id(sharepoint_connection, drive, subsite_id=subsite_id)
    children_str = ":/children" if incl_children else ""
    request_url = (
        sharepoint_connection.api_base_url
        + f"drives/{drive_id}/root:/{folder_path}"
        + children_str
        if subsite is None
        else sharepoint_connection.api_base_url
        + f"sites/{subsite_id}/drives/{drive_id}/root:/{folder_path}"
        + children_str
    )
    response = requests.get(
        request_url, headers=sharepoint_connection.graph_auth_header, **kwargs
    )
    assert (
        response.ok
    ), f"Request returned status code {response.status_code} for given path"
    _check_json(response)
    response_dict = response.json()
    has_multiple_items = "value" in response_dict
    if has_multiple_items:
        return [
            {"name": item["name"], "lastModifiedDateTime": item["lastModifiedDateTime"]}
            for item in response_dict["value"]
        ]
    if not has_multiple_items:
        return [
            {
                "name": response_dict["name"],
                "lastModifiedDateTime": response_dict["lastModifiedDateTime"],
            }
        ]
    return None


def create_folder(
    sharepoint_connection: SharePointConnection,
    drive: str,
    path_parent_folder: str,
    name_new_folder: str,
    subsite=None,
    allow_overwrite: bool = True,
):
    """
    Create a new folder on SharePoint

    Parameters
    ----------
    * sharepoint_connection (SharePointConnection): connection to SharePoint
    * drive (str): name of drive
    * path_parent_folder (str): path/to/sharepoint/folder/in/drive
    * name_new_folder (str): name for the new folder being created
    * subsite (str, optional): name of subsite where folder is located, defaults to None
    * allow_overwrite (bool, optional): whether to overwrite an existing folder
        with the creation of a new one, defaults to True

    Returns
    -------
    * None
    """
    subsite_id = (
        None if subsite is None else _get_subsite_id(sharepoint_connection, subsite)
    )
    drive_id = _get_drive_id(sharepoint_connection, drive, subsite_id=subsite_id)
    parent_item_id = _get_item_id(
        sharepoint_connection, path_parent_folder, drive_id, subsite_id
    )
    request_url = (
        sharepoint_connection.api_base_url
        + f"drives/{drive_id}/items/{parent_item_id}/children"
        if subsite is None
        else sharepoint_connection.api_base_url
        + f"sites/{subsite_id}/drive/items/{parent_item_id}/children"
    )
    headers = {
        **sharepoint_connection.graph_auth_header,
        "Content-Type": "application/json",
    }
    drive_item = {
        "name": name_new_folder,
        "folder": {},
        "@microsoft.graph.conflictBehavior": ("replace" if allow_overwrite else "fail"),
    }
    response = requests.post(request_url, headers=headers, json=drive_item)
    if allow_overwrite:
        assert (
            response.ok
        ), f"Attempting to move item returned status code {response.status_code}; item not moved"
    else:
        assert response.ok or (
            response.json()["error"]["code"] == "nameAlreadyExists"
        ), f"Attempting to move item returned status code {response.status_code}; no nameAlreadyExists error"


def get_txt(
    sharepoint_connection: SharePointConnection,
    drive: str,
    file_path: str,
    subsite=None,
    **kwargs,
) -> str:
    """
    Get a SharePoint txt file

    Parameters
    ----------
    * sharepoint_connection (SharePointConnection): connection to SharePoint
    * drive (str): name of drive
    * file_path (str): path to the txt file
    * subsite (str, optional): name of subsite where file is located, defaults to None
    * kwargs (optional): any other keyword args to pass to requests get API call

    Returns
    -------
    * Content of txt file as a string
    """
    txt_content = get_item(
        sharepoint_connection, drive, file_path, subsite=subsite, **kwargs
    )
    return txt_content.read().decode("utf-8")


__all__ = [name for name in globals() if not name.startswith("_")]

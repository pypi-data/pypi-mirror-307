from io import BytesIO
from unittest.mock import MagicMock, call, patch

import pytest
from sharepoint_utils import (
    get_item,
    write_item,
    move_item,
    copy_item,
    get_items_in_path,
    get_items_date_in_path,
    create_folder,
)
from sharepoint_utils.basic_utils import _get_drive_id

import requests

mock_api_responses = [
    MagicMock(
        spec=requests.Response,
        status_code=200,
        ok=True,
        json=lambda: {
            "@microsoft.graph.downloadUrl": "fake_url",
            "name": "FAKE NAME",
            "lastModifiedDateTime": "FAKE DATE",
        },
        content=b"mock content",
    ),
    MagicMock(
        spec=requests.Response,
        status_code=200,
        ok=True,
        json=lambda: {
            "@microsoft.graph.downloadUrl": "fake_url",
            "value": [{"name": "FAKE NAME", "lastModifiedDateTime": "FAKE DATE"}],
        },
        content=b"mock multi-item content",
    ),
    MagicMock(
        spec=requests.Response,
        status_code=201,
        ok=True,
        json=lambda: {
            "@microsoft.graph.downloadUrl": "fake_url",
            "name": "FAKE NAME",
            "lastModifiedDateTime": "FAKE DATE",
        },
        content=b"mock content",
    ),
    MagicMock(
        spec=requests.Response,
        status_code=204,
        ok=True,
        json=MagicMock(side_effect=ValueError("No JSON object could be decoded")),
        content=b"",
    ),
    MagicMock(
        spec=requests.Response,
        status_code=400,
        ok=False,
        json=lambda: {"error": {"code": "Bad Request"}},
        content=b"Bad Request",
    ),
    MagicMock(
        spec=requests.Response,
        status_code=401,
        ok=False,
        json=lambda: {"error": {"code": "Unauthorized"}},
        content=b"Unauthorized",
    ),
    MagicMock(
        spec=requests.Response,
        status_code=403,
        ok=False,
        json=lambda: {"error": {"code": "Forbidden"}},
        content=b"Forbidden",
    ),
    MagicMock(
        spec=requests.Response,
        status_code=404,
        ok=False,
        json=lambda: {"error": {"code": "Not Found"}},
        content=b"Not Found",
    ),
    MagicMock(
        spec=requests.Response,
        status_code=409,
        ok=False,
        json=lambda: {"error": {"code": "nameAlreadyExists"}},
        content=b"Name already exists",
    ),
    MagicMock(
        spec=requests.Response,
        status_code=500,
        ok=False,
        json=lambda: {"error": {"code": "Internal Server Error"}},
        content=b"Internal Server Error",
    ),
    MagicMock(
        spec=requests.Response,
        status_code=502,
        ok=False,
        json=lambda: {"error": {"code": "Bad Gateway"}},
        content=b"Bad Gateway",
    ),
    MagicMock(
        spec=requests.Response,
        status_code=503,
        ok=False,
        json=lambda: {"error": {"code": "Service Unavailable"}},
        content=b"Service Unavailable",
    ),
]


@pytest.mark.parametrize(
    "response",
    [res for res in mock_api_responses if (res.ok and res.status_code != 204)],
)
@patch("sharepoint_utils.basic_utils.requests.get")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_get_item_download_OK(
    mock_get_subsite_id, mock_get_drive_id, mock_requests_get, mock_connection, response
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_requests_get.return_value = response

    result = get_item(
        mock_connection,
        "mock_drive",
        "mock_item_path",
        subsite="mock_subsite",
        timeout=10,
    )

    assert isinstance(result, BytesIO), "Returned object is not a BytesIO object"
    assert (
        result.getvalue() == mock_requests_get.return_value.content
    ), "Returned content is not the same as the content from the request"
    mock_requests_get.assert_has_calls(
        [
            call(
                "https://mock.sharepoint.com/sites/mock_subsite_id/drives/mock_drive_id/root:/mock_item_path",
                headers={"Authorization": "Bearer mock_token"},
                timeout=10,
            ),
            call("fake_url"),
        ]
    )
    mock_get_subsite_id.assert_called_once_with(mock_connection, "mock_subsite")
    mock_get_drive_id.assert_called_once_with(
        mock_connection, "mock_drive", subsite_id="mock_subsite_id"
    )


@pytest.mark.parametrize(
    "response",
    [res for res in mock_api_responses if (res.ok and res.status_code != 204)],
)
@patch("sharepoint_utils.basic_utils.requests.get")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_get_item_download_ERROR(
    mock_get_subsite_id, mock_get_drive_id, mock_requests_get, mock_connection, response
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_requests_get.side_effect = [
        response,
        MagicMock(
            spec=requests.Response,
            status_code=500,
            ok=False,
            content=b"Internal Server Error",
        ),
    ]

    with pytest.raises(
        Exception,
        match=f"Item download returned status code 500",
    ):
        get_item(
            mock_connection,
            "mock_drive",
            "mock_item_path",
            subsite="mock_subsite",
        )

    mock_requests_get.assert_has_calls(
        [
            call(
                "https://mock.sharepoint.com/sites/mock_subsite_id/drives/mock_drive_id/root:/mock_item_path",
                headers={"Authorization": "Bearer mock_token"},
            ),
            call("fake_url"),
        ]
    )
    mock_get_subsite_id.assert_called_once_with(mock_connection, "mock_subsite")
    mock_get_drive_id.assert_called_once_with(
        mock_connection, "mock_drive", subsite_id="mock_subsite_id"
    )


@pytest.mark.parametrize(
    "response",
    [res for res in mock_api_responses if (not res.ok or res.status_code == 204)],
)
@patch("sharepoint_utils.basic_utils.requests.get")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_get_item_ERROR(
    mock_get_subsite_id, mock_get_drive_id, mock_requests_get, mock_connection, response
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_requests_get.return_value = response

    with pytest.raises(
        Exception,
        match=f"status code {response.status_code}",
    ):
        get_item(
            mock_connection, "mock_drive", "mock_item_path", subsite="mock_subsite"
        )

    mock_requests_get.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drives/mock_drive_id/root:/mock_item_path",
        headers={"Authorization": "Bearer mock_token"},
    )
    mock_get_subsite_id.assert_called_once_with(mock_connection, "mock_subsite")
    mock_get_drive_id.assert_called_once_with(
        mock_connection, "mock_drive", subsite_id="mock_subsite_id"
    )


@pytest.mark.parametrize("response", [res for res in mock_api_responses if res.ok])
@patch("sharepoint_utils.basic_utils.requests.put")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_write_item_OK(
    mock_get_subsite_id, mock_get_drive_id, mock_requests_put, mock_connection, response
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_requests_put.return_value = response

    write_item(
        mock_connection,
        "mock_drive",
        "mock_data",
        "mock_content_type",
        "mock_item_name",
        "mock_folder_path",
        subsite="mock_subsite",
    )

    mock_requests_put.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drives/mock_drive_id/root:/mock_folder_path/mock_item_name:/content",
        headers={
            "Authorization": "Bearer mock_token",
            "Content-Type": "mock_content_type",
        },
        data="mock_data",
    )
    mock_get_subsite_id.assert_called_once_with(mock_connection, "mock_subsite")
    mock_get_drive_id.assert_called_once_with(
        mock_connection, "mock_drive", subsite_id="mock_subsite_id"
    )


@pytest.mark.parametrize("response", [res for res in mock_api_responses if not res.ok])
@patch("sharepoint_utils.basic_utils.requests.put")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_write_item_ERROR(
    mock_get_subsite_id, mock_get_drive_id, mock_requests_put, mock_connection, response
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_requests_put.return_value = response

    with pytest.raises(
        Exception,
        match=f"status code {response.status_code}",
    ):
        write_item(
            mock_connection,
            "mock_drive",
            "mock_data",
            "mock_content_type",
            "mock_item_name",
            "mock_folder_path",
            subsite="mock_subsite",
        )

    mock_requests_put.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drives/mock_drive_id/root:/mock_folder_path/mock_item_name:/content",
        headers={
            "Authorization": "Bearer mock_token",
            "Content-Type": "mock_content_type",
        },
        data="mock_data",
    )
    mock_get_subsite_id.assert_called_once_with(mock_connection, "mock_subsite")
    mock_get_drive_id.assert_called_once_with(
        mock_connection, "mock_drive", subsite_id="mock_subsite_id"
    )


@pytest.mark.parametrize(
    "response",
    [res for res in mock_api_responses if (res.ok or (res.status_code == 409))],
)
@patch("sharepoint_utils.basic_utils.requests.patch")
@patch("sharepoint_utils.basic_utils._get_item_id")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_move_item_not_allow_override_OK(
    mock_get_subsite_id,
    mock_get_drive_id,
    mock_get_item_id,
    mock_requests_patch,
    mock_connection,
    response,
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_get_item_id.return_value = "mock_target_dir_id"
    mock_requests_patch.return_value = response

    move_item(
        mock_connection,
        "mock_drive",
        "mock_item_name",
        origin_parent_dir="mock_origin_dir",
        target_parent_dir="mock_target_dir",
        subsite="mock_subsite",
        allow_overwrite=False,
    )

    mock_requests_patch.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drives/mock_drive_id/root:/mock_origin_dir/mock_item_name",
        headers={"Authorization": "Bearer mock_token"},
        json={
            "parentReference": {"id": "mock_target_dir_id"},
            "name": "mock_item_name",
        },
        params={
            "@microsoft.graph.conflictBehavior": "fail",
        },
    )
    mock_get_subsite_id.assert_called_once_with(mock_connection, "mock_subsite")
    mock_get_drive_id.assert_called_once_with(
        mock_connection, "mock_drive", subsite_id="mock_subsite_id"
    )
    mock_get_item_id.assert_called_once_with(
        mock_connection,
        "mock_target_dir",
        "mock_drive_id",
        subsite_id="mock_subsite_id",
    )


@pytest.mark.parametrize(
    "response",
    [res for res in mock_api_responses if (not res.ok and res.status_code != 409)],
)
@patch("sharepoint_utils.basic_utils.requests.patch")
@patch("sharepoint_utils.basic_utils._get_item_id")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_move_item_not_allow_override_ERROR(
    mock_get_subsite_id,
    mock_get_drive_id,
    mock_get_item_id,
    mock_requests_patch,
    mock_connection,
    response,
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_get_item_id.return_value = "mock_target_dir_id"
    mock_requests_patch.return_value = response
    with pytest.raises(
        Exception,
        match=f"status code {response.status_code}",
    ):

        move_item(
            mock_connection,
            "mock_drive",
            "mock_item_name",
            origin_parent_dir="mock_origin_dir",
            target_parent_dir="mock_target_dir",
            subsite="mock_subsite",
            allow_overwrite=False,
        )
    mock_requests_patch.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drives/mock_drive_id/root:/mock_origin_dir/mock_item_name",
        headers={"Authorization": "Bearer mock_token"},
        json={
            "parentReference": {"id": "mock_target_dir_id"},
            "name": "mock_item_name",
        },
        params={
            "@microsoft.graph.conflictBehavior": "fail",
        },
    )
    mock_get_subsite_id.assert_called_once_with(mock_connection, "mock_subsite")
    mock_get_drive_id.assert_called_once_with(
        mock_connection, "mock_drive", subsite_id="mock_subsite_id"
    )
    mock_get_item_id.assert_called_once_with(
        mock_connection,
        "mock_target_dir",
        "mock_drive_id",
        subsite_id="mock_subsite_id",
    )


@pytest.mark.parametrize(
    "response",
    [res for res in mock_api_responses if (res.ok or (res.status_code == 409))],
)
@patch("sharepoint_utils.basic_utils.requests.post")
@patch("sharepoint_utils.basic_utils._get_item_id")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_copy_item_not_allow_override_OK(
    mock_get_subsite_id,
    mock_get_drive_id,
    mock_get_item_id,
    mock_requests_post,
    mock_connection,
    response,
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_get_item_id.side_effect = ["mock_origin_item_id", "mock_target_dir_id"]
    mock_requests_post.return_value = response

    copy_item(
        mock_connection,
        "mock_drive",
        "mock_item_name",
        "mock_target_dir",
        "mock_origin_dir",
        "mock_target_item_name",
        "mock_subsite",
        allow_overwrite=False,
    )

    mock_requests_post.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drive/items/mock_origin_item_id/copy",
        headers={"Authorization": "Bearer mock_token"},
        json={
            "parentReference": {"driveId": "mock_drive_id", "id": "mock_target_dir_id"},
            "name": ("mock_target_item_name"),
        },
        params={"@microsoft.graph.conflictBehavior": "fail"},
    )
    mock_get_subsite_id.assert_called_once_with(mock_connection, "mock_subsite")
    mock_get_drive_id.assert_called_once_with(
        mock_connection, "mock_drive", subsite_id="mock_subsite_id"
    )
    mock_get_item_id.assert_has_calls(
        [
            call(
                mock_connection,
                "mock_origin_dir/mock_item_name",
                "mock_drive_id",
                "mock_subsite_id",
            ),
            call(
                mock_connection, "mock_target_dir", "mock_drive_id", "mock_subsite_id"
            ),
        ]
    )


@pytest.mark.parametrize(
    "response",
    [res for res in mock_api_responses if (not res.ok and res.status_code != 409)],
)
@patch("sharepoint_utils.basic_utils.requests.post")
@patch("sharepoint_utils.basic_utils._get_item_id")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_copy_item_not_allow_override_ERROR(
    mock_get_subsite_id,
    mock_get_drive_id,
    mock_get_item_id,
    mock_requests_post,
    mock_connection,
    response,
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_get_item_id.side_effect = ["mock_origin_item_id", "mock_target_dir_id"]
    mock_requests_post.return_value = response
    with pytest.raises(
        Exception,
        match=f"status code {response.status_code}",
    ):
        copy_item(
            mock_connection,
            "mock_drive",
            "mock_item_name",
            "mock_target_dir",
            "mock_origin_dir",
            "mock_target_item_name",
            "mock_subsite",
            allow_overwrite=False,
        )
    mock_requests_post.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drive/items/mock_origin_item_id/copy",
        headers={"Authorization": "Bearer mock_token"},
        json={
            "parentReference": {"driveId": "mock_drive_id", "id": "mock_target_dir_id"},
            "name": ("mock_target_item_name"),
        },
        params={"@microsoft.graph.conflictBehavior": "fail"},
    )
    mock_get_subsite_id.assert_called_once_with(mock_connection, "mock_subsite")
    mock_get_drive_id.assert_called_once_with(
        mock_connection, "mock_drive", subsite_id="mock_subsite_id"
    )
    mock_get_item_id.assert_has_calls(
        [
            call(
                mock_connection,
                "mock_origin_dir/mock_item_name",
                "mock_drive_id",
                "mock_subsite_id",
            ),
            call(
                mock_connection, "mock_target_dir", "mock_drive_id", "mock_subsite_id"
            ),
        ]
    )


@pytest.mark.parametrize(
    "response",
    [
        res
        for res in mock_api_responses
        if res.content.decode() == "mock multi-item content"
    ],
)
@patch("sharepoint_utils.basic_utils.requests.get")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_get_items_path_OK(
    mock_get_subsite_id, mock_get_drive_id, mock_requests_get, mock_connection, response
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_requests_get.return_value = response

    result = get_items_in_path(
        mock_connection, "mock_drive", "mock_folder_path", "mock_subsite"
    )

    assert isinstance(result, list), "Returned object is not a list"
    assert (
        all(isinstance(item, str) for item in result) or len(result) == 0
    ), "Returned object is not a list of strings"
    mock_get_subsite_id.assert_called_once_with(mock_connection, "mock_subsite")
    mock_get_drive_id.assert_called_once_with(
        mock_connection, "mock_drive", subsite_id="mock_subsite_id"
    )
    mock_requests_get.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drives/mock_drive_id/root:/mock_folder_path:/children",
        headers={"Authorization": "Bearer mock_token"},
    )


@pytest.mark.parametrize(
    "response",
    [res for res in mock_api_responses if (res.status_code == 204) or (not res.ok)],
)
@patch("sharepoint_utils.basic_utils.requests.get")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_get_items_path_ERROR(
    mock_get_subsite_id, mock_get_drive_id, mock_requests_get, mock_connection, response
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_requests_get.return_value = response

    with pytest.raises(
        Exception,
        match=f"status code {response.status_code}",
    ):
        get_items_in_path(
            mock_connection, "mock_drive", "mock_folder_path", "mock_subsite"
        )
    mock_get_subsite_id.assert_called_once_with(mock_connection, "mock_subsite")
    mock_get_drive_id.assert_called_once_with(
        mock_connection, "mock_drive", subsite_id="mock_subsite_id"
    )
    mock_requests_get.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drives/mock_drive_id/root:/mock_folder_path:/children",
        headers={"Authorization": "Bearer mock_token"},
    )


@pytest.mark.parametrize(
    "response",
    [
        res
        for res in mock_api_responses
        if res.content.decode() == "mock multi-item content"
    ],
)
@patch("sharepoint_utils.basic_utils.requests.get")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_get_items_date_path_incl_children_OK(
    mock_get_subsite_id, mock_get_drive_id, mock_requests_get, mock_connection, response
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_requests_get.return_value = response

    mock_subsite_name = "mock_subsite"
    mock_drive_name = "mock_drive"

    result = get_items_date_in_path(
        mock_connection,
        mock_drive_name,
        "mock_folder_path",
        True,
        mock_subsite_name,
        timeout=10,
    )
    assert isinstance(result, list), "Returned object is not a list"
    assert all(
        isinstance(item, dict) for item in result
    ), "Returned object is not a list of dict"
    assert all(
        "lastModifiedDateTime" in item for item in result
    ), "Returned dictionaries don't contain the expected key"

    mock_get_subsite_id.assert_called_once_with(mock_connection, mock_subsite_name)
    mock_get_drive_id.assert_called_once_with(
        mock_connection, mock_drive_name, subsite_id=mock_get_subsite_id.return_value
    )
    mock_requests_get.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drives/mock_drive_id/root:/mock_folder_path:/children",
        headers={"Authorization": "Bearer mock_token"},
        timeout=10,
    )


@pytest.mark.parametrize(
    "response",
    [
        res
        for res in mock_api_responses
        if (
            res.ok
            and (res.status_code != 204)
            and (res.content.decode() != "mock multi-item content")
        )
    ],
)
@patch("sharepoint_utils.basic_utils.requests.get")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_get_items_date_path_nochildren_OK(
    mock_get_subsite_id, mock_get_drive_id, mock_requests_get, mock_connection, response
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_requests_get.return_value = response

    mock_subsite_name = "mock_subsite"
    mock_drive_name = "mock_drive"

    result = get_items_date_in_path(
        mock_connection,
        mock_drive_name,
        "mock_folder_path",
        False,
        mock_subsite_name,
        timeout=10,
    )
    assert isinstance(result, list), "Returned object is not a list"
    assert all(
        isinstance(item, dict) for item in result
    ), "Returned object is not a list of dict"
    assert all(
        "lastModifiedDateTime" in item for item in result
    ), "Returned dictionaries don't contain the expected key"

    mock_get_subsite_id.assert_called_once_with(mock_connection, mock_subsite_name)
    mock_get_drive_id.assert_called_once_with(
        mock_connection, mock_drive_name, subsite_id=mock_get_subsite_id.return_value
    )
    mock_requests_get.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drives/mock_drive_id/root:/mock_folder_path",
        headers={"Authorization": "Bearer mock_token"},
        timeout=10,
    )


@pytest.mark.parametrize(
    "response",
    [res for res in mock_api_responses if (res.status_code == 204) or (not res.ok)],
)
@patch("sharepoint_utils.basic_utils.requests.get")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_get_items_date_path_ERROR(
    mock_get_subsite_id, mock_get_drive_id, mock_requests_get, mock_connection, response
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_requests_get.return_value = response

    mock_subsite_name = "mock_subsite"
    mock_drive_name = "mock_drive"

    with pytest.raises(
        Exception,
        match=f"status code {response.status_code}",
    ):
        get_items_date_in_path(
            mock_connection,
            mock_drive_name,
            "mock_folder_path",
            True,
            mock_subsite_name,
            timeout=10,
        )
    mock_get_subsite_id.assert_called_once_with(mock_connection, mock_subsite_name)
    mock_get_drive_id.assert_called_once_with(
        mock_connection, mock_drive_name, subsite_id=mock_get_subsite_id.return_value
    )
    mock_requests_get.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drives/mock_drive_id/root:/mock_folder_path:/children",
        headers={"Authorization": "Bearer mock_token"},
        timeout=10,
    )


@pytest.mark.parametrize(
    "response",
    [res for res in mock_api_responses if (res.ok or (res.status_code == 409))],
)
@patch("sharepoint_utils.basic_utils.requests.post")
@patch("sharepoint_utils.basic_utils._get_item_id")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_create_folder_not_allow_override_OK(
    mock_get_subsite_id,
    mock_get_drive_id,
    mock_get_item_id,
    mock_requests_post,
    mock_connection,
    response,
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_get_item_id.return_value = "mock_parent_item_id"
    mock_requests_post.return_value = response

    create_folder(
        mock_connection,
        "mock_drive",
        "mock_parent_path",
        "mock_new_folder_name",
        "mock_subsite",
        False,
    )
    mock_get_subsite_id.assert_called_once_with(mock_connection, "mock_subsite")
    mock_get_drive_id.assert_called_once_with(
        mock_connection, "mock_drive", subsite_id=mock_get_subsite_id.return_value
    )
    mock_get_item_id.assert_called_once_with(
        mock_connection,
        "mock_parent_path",
        mock_get_drive_id.return_value,
        mock_get_subsite_id.return_value,
    )
    mock_requests_post.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drive/items/mock_parent_item_id/children",
        headers={
            "Authorization": "Bearer mock_token",
            "Content-Type": "application/json",
        },
        json={
            "name": "mock_new_folder_name",
            "folder": {},
            "@microsoft.graph.conflictBehavior": ("fail"),
        },
    )


@pytest.mark.parametrize(
    "response",
    [res for res in mock_api_responses if (res.status_code != 409) and (not res.ok)],
)
@patch("sharepoint_utils.basic_utils.requests.post")
@patch("sharepoint_utils.basic_utils._get_item_id")
@patch("sharepoint_utils.basic_utils._get_drive_id")
@patch("sharepoint_utils.basic_utils._get_subsite_id")
def test_create_folder_not_allow_override_ERROR(
    mock_get_subsite_id,
    mock_get_drive_id,
    mock_get_item_id,
    mock_requests_post,
    mock_connection,
    response,
):
    mock_get_subsite_id.return_value = "mock_subsite_id"
    mock_get_drive_id.return_value = "mock_drive_id"
    mock_get_item_id.return_value = "mock_parent_item_id"
    mock_requests_post.return_value = response

    with pytest.raises(
        Exception,
        match=f"status code {response.status_code}",
    ):
        create_folder(
            mock_connection,
            "mock_drive",
            "mock_parent_path",
            "mock_new_folder_name",
            "mock_subsite",
            False,
        )
    mock_get_subsite_id.assert_called_once_with(mock_connection, "mock_subsite")
    mock_get_drive_id.assert_called_once_with(
        mock_connection, "mock_drive", subsite_id=mock_get_subsite_id.return_value
    )
    mock_get_item_id.assert_called_once_with(
        mock_connection,
        "mock_parent_path",
        mock_get_drive_id.return_value,
        mock_get_subsite_id.return_value,
    )
    mock_requests_post.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drive/items/mock_parent_item_id/children",
        headers={
            "Authorization": "Bearer mock_token",
            "Content-Type": "application/json",
        },
        json={
            "name": "mock_new_folder_name",
            "folder": {},
            "@microsoft.graph.conflictBehavior": ("fail"),
        },
    )


@pytest.mark.parametrize(
    "response",
    [res for res in mock_api_responses if res.ok and (res.status_code != 204)],
)
@patch("sharepoint_utils.basic_utils.requests.get")
@patch("sharepoint_utils.basic_utils._get_id_from_name")
def test_get_drive_id_OK(
    mock_get_id_from_name, mock_requests_get, mock_connection, response
):
    mock_requests_get.return_value = response
    mock_get_id_from_name.return_value = "mock_drive_id"
    result = _get_drive_id(mock_connection, "mock_drive", "mock_subsite_id")
    assert isinstance(result, str), "Returned object is not a string"
    mock_requests_get.assert_called_once_with(
        "https://mock.sharepoint.com/sites/mock_subsite_id/drives",
        headers={"Authorization": "Bearer mock_token"},
    )
    mock_get_id_from_name.assert_called_once_with(response.json(), "mock_drive")

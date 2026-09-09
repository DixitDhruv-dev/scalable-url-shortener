from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@patch(
    "app.api.routes.redirect.get_original_url"
)
def test_redirect_success(mock_get_original_url):
    mock_get_original_url.return_value = "https://google.com/"

    response = client.get(
        "/abc1234",
        follow_redirects=False,
    )

    assert response.status_code == 307
    assert response.headers["location"] == "https://google.com/"


@patch(
    "app.api.routes.redirect.get_original_url"
)
def test_redirect_not_found(mock_get_original_url):
    mock_get_original_url.side_effect = ValueError(
        "Short URL not found"
    )

    response = client.get(
        "/missing",
        follow_redirects=False,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Short URL not found"


@patch(
    "app.api.routes.redirect.get_original_url"
)
def test_redirect_expired(mock_get_original_url):
    mock_get_original_url.side_effect = ValueError(
        "Short URL has expired"
    )

    response = client.get(
        "/expired",
        follow_redirects=False,
    )

    assert response.status_code == 410
    assert response.json()["detail"] == "Short URL has expired"
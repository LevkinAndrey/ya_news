from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    (pytest.lazy_fixture('url_home'),
     pytest.lazy_fixture('url_detail'),
     pytest.lazy_fixture('url_login'),
     pytest.lazy_fixture('url_logout'),
     pytest.lazy_fixture('url_signup')
     )
)
def test_pages_availability_for_anonymous_user(
        url,
        client,
):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'url',
    (pytest.lazy_fixture('url_edit'),
     pytest.lazy_fixture('url_delete')
     )
)
def test_availability_for_comment_edit_and_delete(
        url,
        parametrized_client,
        expected_status,

):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (pytest.lazy_fixture('url_edit'),
     pytest.lazy_fixture('url_delete')
     )
)
def test_redirect_for_anonymous_client(
        url,
        url_login,
        client,
):
    expected_url = f'{url_login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)

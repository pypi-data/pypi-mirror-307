"""Common utilities for the api portion of the sdk."""

import httpx

from .. import settings

__all__ = ["get", "post", "delete", "put"]


url = settings.dodata_url


def raise_on_4xx_5xx(response: httpx.Response) -> None:
    if response.is_error:
        response.read()
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise httpx.HTTPStatusError(
                message=response.text, request=response.request, response=response
            ) from e


client = httpx.Client(
    verify=False,
    auth=httpx.BasicAuth(
        username=settings.dodata_user, password=settings.dodata_password
    ),
    follow_redirects=True,
    event_hooks={"response": [raise_on_4xx_5xx]},
)

delete = client.delete
get = client.get
post = client.post
put = client.put

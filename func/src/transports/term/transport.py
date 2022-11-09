# Jormungandr
from ...domain.exceptions.transports.exception import SignTermStatusCodeNotOk

# Standards
from http import HTTPStatus

# Third party
from decouple import config
from httpx import AsyncClient


class TermTransport:
    @staticmethod
    async def sign_term(jwt: str, body: dict) -> bool:
        headers = {"x-thebes-answer": jwt}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.put(
                config("JORMUNGANDR_SIGN_TERM_URL"), headers=headers, json=body
            )
            if not request_result.status_code == HTTPStatus.OK:
                raise SignTermStatusCodeNotOk()
            return True

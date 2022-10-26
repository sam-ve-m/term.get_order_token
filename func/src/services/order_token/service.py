# Term
from ...domain.validators.term_with_order.validator import TermWithOrder
from ...domain.models.token.model import TokenModel
from ...transports.term.transport import TermTransport
from ...domain.exceptions.services.exception import ErrorToGenerateOrderToken

# Third party
from harpocrates import Harpocrates, HarpocratesStatusResponse


class OrderToken:

    @classmethod
    async def sign_term_and_get_order_token(cls, payload_validated: TermWithOrder, jwt: str, unique_id: str):
        token_model = TokenModel(payload=payload_validated, unique_id=unique_id)
        body = token_model.build_body_content_to_sign_term()
        await TermTransport.sign_term(jwt=jwt, body=body)
        jwt_content = token_model.build_harpocrates_jwt_content()
        order_token = await cls.generate_token(jwt_content=jwt_content)
        return order_token

    @staticmethod
    async def generate_token(jwt_content: dict):
        order_token, status = await Harpocrates.generate_jwt(values=jwt_content)
        if status == HarpocratesStatusResponse.SUCCESS:
            return order_token
        raise ErrorToGenerateOrderToken()


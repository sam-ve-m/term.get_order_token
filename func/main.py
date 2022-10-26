# Term
from src.domain.exceptions.base.base_exceptions import (
    ServiceException,
    TransportException,
    InternalCode,
)
from src.domain.models.response.model import ResponseModel
from src.services.jwt import JwtService
from src.domain.validators.term_with_order.validator import TermWithOrder
from src.services.order_token.service import OrderToken

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request, Response, Flask
from pydantic import ValidationError

app = Flask("__name__")


@app.route('/get_order_token', methods=["POST"])
async def sign_term_and_get_token() -> Response:
    try:
        jwt = request.headers.get("x-thebes-answer")
        raw_payload = request.json
        payload_validated = TermWithOrder(**raw_payload)
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        new_order_token = await OrderToken.sign_term_and_get_order_token(
            payload_validated=payload_validated, jwt=jwt, unique_id=unique_id
        )
        response = ResponseModel(
            result=new_order_token,
            success=True,
            message="Order token generated with successfully",
            code=InternalCode.SUCCESS,
        ).build_http_response(status_code=HTTPStatus.OK)
        return response

    except ServiceException as err:
        Gladsheim.error(error=err, message=err.msg)
        response = ResponseModel(
            success=err.success, message=err.msg, code=err.code
        ).build_http_response(status_code=err.status_code)
        return response

    except TransportException as err:
        Gladsheim.error(error=err, message=err.msg)
        response = ResponseModel(
            success=err.success, message=err.msg, code=err.code
        ).build_http_response(status_code=err.status_code)
        return response

    except ValidationError as err:
        Gladsheim.error(error=err)
        response = ResponseModel(
            success=False,
            message="Invalid params",
            code=InternalCode.INVALID_PARAMS,
        ).build_http_response(status_code=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error has occurred",
        ).build_http_response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

app.run()

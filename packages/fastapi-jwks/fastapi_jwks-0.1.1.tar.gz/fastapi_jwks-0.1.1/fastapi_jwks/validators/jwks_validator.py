from functools import cached_property
from typing import Any, Generic, TypeVar

import httpx
import jwt
from cachetools import TTLCache, cached
from fastapi import HTTPException
from jwt import algorithms
from loguru import logger
from pydantic import BaseModel

from fastapi_jwks.models.types import JWKSConfig, JWTDecodeConfig

DataT = TypeVar("DataT", bound=BaseModel)


class JWKSValidator(Generic[DataT]):
    def __init__(self, decode_config: JWTDecodeConfig, jwks_config: JWKSConfig):
        self.decode_config = decode_config
        self.jwks_config = jwks_config
        self.client = self._create_client()

    def _create_client(self) -> httpx.Client:
        client_kwargs = {}
        if self.jwks_config.ca_cert_path:
            client_kwargs["verify"] = self.jwks_config.ca_cert_path
        return httpx.Client(**client_kwargs)

    @cached(cache=TTLCache(ttl=600, maxsize=1))
    def jwks_data(self) -> dict[str, Any]:
        try:
            logger.debug("Fetching JWKS from %s", self.jwks_config.url)
            jwks_response = self.client.get(self.jwks_config.url)
            jwks_response.raise_for_status()
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail="Invalid JWKS URI") from e
        jwks: dict[str, Any] = jwks_response.json()
        if "keys" not in jwks:
            raise HTTPException(status_code=503, detail="Invalid JWKS")
        return jwks

    @staticmethod
    def __extract_algorithms(jwks_response: dict[str, Any]) -> list[str]:
        if "keys" not in jwks_response:
            raise ValueError("JWKS response does not contain keys")
        keys = jwks_response["keys"]
        return [key["alg"] for key in keys]

    @cached_property
    def __is_generic_passed(self):
        if getattr(self, "__orig_class__", None) is None:  # type: ignore
            return False
        return True

    def validate_token(self, token: str) -> DataT:
        if not self.__is_generic_passed:
            raise ValueError(
                "Validator needs a model as generic value to decode payload"
            )

        public_key = None
        try:
            header = jwt.get_unverified_header(token)
            kid = header["kid"]
            jwks_data = self.jwks_data()
            if header["alg"] not in self.__extract_algorithms(jwks_data):
                raise HTTPException(status_code=401, detail="Invalid token")
            for key in jwks_data["keys"]:
                if key["kid"] == kid:
                    public_key = algorithms.get_default_algorithms()[
                        header["alg"]
                    ].from_jwk(key)
                    break
            if public_key is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return self.__orig_class__.__args__[0].model_validate(  # type: ignore
                # This line gets the generic value in runtime to transform it to the correct pydantic model
                jwt.decode(
                    token,
                    key=public_key,
                    **self.decode_config.model_dump(),
                    algorithms=[header["alg"]],
                )
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired") from None
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token") from None

import logging
from typing import Annotated

from fastapi import Depends, Header, HTTPException
from jwt import PyJWTError

from app.services.auth_service import get_user_info_from_token

logger = logging.getLogger(__name__)


def current_user(authorization: str = Header()):
    scheme, token = authorization.split()
    if scheme.lower() != "bearer":
        logger.error(f"Invalid authorization scheme: {scheme}")
        raise HTTPException(401)

    try:
        return get_user_info_from_token(token)
    except PyJWTError as e:
        logger.error(f"JWT error: {e}")
        raise HTTPException(status_code=401)


CurrentUser = Annotated[dict, Depends(current_user)]

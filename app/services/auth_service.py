import os

import jwt

OIDC_ISSUER = os.environ.get("OIDC_ISSUER", "")
OIDC_AUDIENCE = os.environ.get("OIDC_AUDIENCE", "")

jwks_client = jwt.PyJWKClient(f"{OIDC_ISSUER}/protocol/openid-connect/certs")


def get_user_info_from_token(token: str) -> dict:
    signing_key = jwks_client.get_signing_key_from_jwt(token)

    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        issuer=OIDC_ISSUER,
        audience=OIDC_AUDIENCE,
    )

    return payload

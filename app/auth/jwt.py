from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.config import settings


def _create_token(
    subject: UUID,
    token_type: str,
    expires_delta: timedelta,
) -> str:
    now = datetime.now(UTC)

    payload = {
        "sub": str(subject),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def create_access_token(user_id: UUID) -> str:
    return _create_token(
        subject=user_id,
        token_type="access",
        expires_delta=timedelta(
            minutes=settings.access_token_expire_minutes
        ),
    )


def create_refresh_token(user_id: UUID) -> str:
    return _create_token(
        subject=user_id,
        token_type="refresh",
        expires_delta=timedelta(
            days=settings.refresh_token_expire_days
        ),
    )


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
from fastapi import HTTPException, Header


async def get_token_authorization(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    return authorization

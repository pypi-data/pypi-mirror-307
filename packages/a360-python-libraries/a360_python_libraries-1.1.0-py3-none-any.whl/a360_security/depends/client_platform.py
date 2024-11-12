from fastapi import Request, HTTPException

from a360_security import enums


def require_client_platform(request: Request) -> enums.ClientPlatform:
    user_agent = request.headers.get('User-Agent', '').lower()

    if user_agent == '':
        raise HTTPException(status_code=400,
                            detail="User-Agent header is required")

    if any(
        platform in user_agent for platform in [
            'a360-ios',
            'a360-android']):
        return enums.ClientPlatform.MOBILE
    elif any(platform in user_agent for platform in ['a360-windows', 'a360-mac', 'a360-unix']):
        return enums.ClientPlatform.DESKTOP
    else:
        return enums.ClientPlatform.WEB

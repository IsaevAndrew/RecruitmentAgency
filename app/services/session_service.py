from fastapi import Request, HTTPException


def get_current_user(request: Request):
    """
    Получает текущего авторизованного пользователя из сессии.
    """
    user_id = request.session.get("user_id")
    role = request.session.get("role")
    if not user_id or not role:
        raise HTTPException(status_code=401,
                            detail="Пользователь не авторизован")
    return {"user_id": user_id, "role": role}


from fastapi import Request, HTTPException, status

async def allow_get_only(request: Request):
    if request.method != "GET":
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Only GET requests allowed")

    return

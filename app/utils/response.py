from fastapi.responses import JSONResponse
from datetime import datetime

def format_response(data=None, message: str = "Something went wrong...", code: int = 400):
    return JSONResponse(
        content={
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "code": code,
            "data": data if data is not None else [],
        },
        status_code=code,
    ) 
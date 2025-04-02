from datetime import datetime
from fastapi.responses import JSONResponse

def format_response(data=None, message="Something went wrong...", code=400):
    return JSONResponse(
        content={
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "code": code,
            "data": data if data is not None else [],
        },
        status_code=code,
    )

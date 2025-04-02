from fastapi import Request, FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from data.response import format_response
from main import app

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return format_response(message="Internal Server Error", code=500)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return format_response(message="Validation Error", code=400)

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return format_response(message="Database Error", code=500)

from fastapi import APIRouter
import app.routes.v1 as v1_router

routes = APIRouter()

routes.include_router(v1_router.router, prefix="/v1")

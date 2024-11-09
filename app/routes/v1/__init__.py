from fastapi import APIRouter
import app.routes.v1.task as task_router

router = APIRouter()

router.include_router(task_router.router, prefix="/task")

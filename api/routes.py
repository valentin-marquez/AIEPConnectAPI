from fastapi import APIRouter
from api import ExternalApi
from api.models import CourseDataModel
from pydantic.error_wrappers import ValidationError

router = APIRouter(
    prefix="/v1",
    tags=["AIEP"],
    responses={404: {"description": "Not found"}},
)

def get_external_api(email: str, password: str):
    return ExternalApi(email, password)

async def get_user_info(aiep: ExternalApi):
    return await aiep.get_user_info()

@router.get("/userInfo")
async def get_user(email: str, password: str):
    aiep = get_external_api(email, password)
    return await get_user_info(aiep)
    
@router.get("/userInfo/token")
async def get_user_info_token(email: str, password: str):
    aiep = get_external_api(email, password)
    return await aiep.get_token()

@router.get("/schedule")
async def get_schedule(email: str, password: str):
    aiep = get_external_api(email, password)
    user_info = await get_user_info(aiep)
    if user_info:
        return await aiep.get_schedule(user_info)
    else:
        return {"message": "Error al obtener el horario del usuario"}

@router.get("/courses")
async def get_courses(email: str, password: str):
    aiep = get_external_api(email, password)
    user_info = await get_user_info(aiep)
    if user_info:
        return await aiep.get_courses(user_info)
    else:
        return {"message": "Error al obtener los cursos del usuario"}

@router.post("/grades")
async def get_grades(email, password, course_data: CourseDataModel):
    aiep = get_external_api(email, password)
    user_info = await get_user_info(aiep)
    if user_info:
        try:
            return await aiep.get_grades(user_info, course_data)
        except ValidationError as e:
            return {"message": "Error de validación", "details": e.errors()}
    else:
        return {"message": "Error al obtener las calificaciones del usuario"}

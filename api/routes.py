from fastapi import APIRouter, HTTPException
from pydantic.error_wrappers import ValidationError

from api import ExternalApi
from api.models import CourseDataModel
from api.schemas import Calendar, CourseList, GradesResponse, User
from api.utils import Token

router = APIRouter(
    prefix="/v1",
    tags=["AIEP"],
    responses={404: {"description": "Not found"}},
)


def get_external_api(email: str = None, password: str = None) -> ExternalApi:
    return ExternalApi(email, password)

async def get_user_info(aiep: ExternalApi):
    return await aiep.get_user_info()

@router.get("/auth")
async def get_auth(email: str, password: str):
    try:
        aiep = get_external_api(email, password)
        return await get_user_info(aiep)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Error de validación")

@router.get("/schedule", response_model=Calendar)
async def get_schedule(userId:str, careerId:str, token:str):
    try:
        username = Token.get_username_from_token(token)
        aiep = get_external_api()
        user = User(userId=userId, userNC=username, careersList=[careerId], token=token)
        return Calendar.parse_obj(await aiep.get_schedule(user))
    
    except ValidationError:
        raise HTTPException(status_code=400, detail="Error de validación")
    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener el horario")

@router.get("/courses", response_model=CourseList)
async def get_courses(userId:str, careerId:str, token:str):
    try:
        username = Token.get_username_from_token(token)
        aiep = get_external_api()
        user = User(userId=userId, userNC=username, careersList=[careerId], token=token)
        return CourseList.parse_obj(await aiep.get_courses(user))
    except ValidationError:
        raise HTTPException(status_code=400, detail="Error de validación")
    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener los cursos")

@router.post("/grades")
async def get_grades(userId:str, careerId:str,course_data: CourseDataModel, token:str):
    try:
        username = Token.get_username_from_token(token)
        aiep = get_external_api()
        user = User(userId=userId, userNC=username, careersList=[careerId], token=token)
        return GradesResponse.parse_obj(await aiep.get_grades(user, course_data))

    except ValidationError:
        raise HTTPException(status_code=400, detail="Error de validación")
    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener las notas")
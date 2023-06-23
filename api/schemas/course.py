from typing import List
from pydantic import BaseModel


class Professor(BaseModel):
    professorEmail: str
    professorName: str

class CourseData(BaseModel):
    courseType: str
    campus: str
    tipo_curso: str
    empty: str
    courseId: str
    professor_code: str
    type: str
    section: str
    school_code: str
    courseIdBB: str

class Course(BaseModel):
    typeId: str
    courseNC: str
    courseCodeDisplay: str
    showPresentialIcons: str
    activePeriodId: str
    courseName: str
    type: str
    courseIdLMS: str
    professorList: List[Professor]
    courseData: CourseData

class CourseListResponse(BaseModel):
    courseList: List[Course]
    status: str

class Response(BaseModel):
    courseListResponse: CourseListResponse

class CourseList(BaseModel):
    response: Response

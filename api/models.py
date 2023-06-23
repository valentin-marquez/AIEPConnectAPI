from pydantic import BaseModel

class CourseDataModel(BaseModel):
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

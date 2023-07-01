from typing import List

from pydantic import BaseModel


class GradeItem(BaseModel):
    gradeStyle: str
    idIncrementalUnidadTematica: str
    cellId: str
    gradeName: str
    gradeColor: str = None
    grade: str = None
    courseId: str = None


class GradeListByCourseResponse(BaseModel):
    pendingEvaluation: str
    status: str
    blockEvaluation: str
    message: str
    list: List[GradeItem]
    moofwdVersionMashup: str


class GradesResponse(BaseModel):
    response: dict

from typing import List

from pydantic import BaseModel


class Day(BaseModel):
    name: str
    cellId: str

class Module(BaseModel):
    name: str
    cellId: str

class ListEntry(BaseModel):
    professor: str
    moduleId: str
    cellId: str
    sCourseCode: str
    startTime: str
    campus: str
    startDate: str
    classroom: str
    sortKey: str
    column: str
    endDate: str
    endTime: str
    EXAMPLE: str
    courseName: str
    courseCode: str
    day: str
    row: str

class ScheduleResponse(BaseModel):
    status: str
    modules: List[Module]
    confirm: str
    list: List[ListEntry]
    days: List[Day]

class Response(BaseModel):
    scheduleResponse: ScheduleResponse

class Calendar(BaseModel):
    response: Response

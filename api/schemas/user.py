from typing import List
from pydantic import BaseModel
from api.utils import ZubronHelper


class User(BaseModel):
    userId: str
    userNC: str
    careersList: List[str]
    sede: str
    name: str

    def to_params(self):
        return {    
            "roleId": "student",
            "userNC": self.userNC,
            "userId": self.userId,
            "lang": "es",
            "careerId": self.careersList[0],
            "userData": {
                "userBB": self.userNC,
            }
        }

    def __str__(self) -> str:
        return f"User: {self.name} ({self.userId})"

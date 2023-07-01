from typing import List

from pydantic import BaseModel, Field

from api.utils import ZubronHelper


class User(BaseModel):
    userId: str = Field(alias="userId", default=None)
    userNC: str = Field(alias="userNC", default=None)
    careersList: List[str] = Field(alias="careersList", default=None)
    campus: str = Field(alias="campus", default=None)
    name: str = Field(alias="name", default=None)
    token: str = Field(alias="token", default=None)

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
    
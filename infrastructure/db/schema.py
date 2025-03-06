from pydantic import BaseModel, HttpUrl
from .models import Difficulty


class LeetcodeTaskSchema(BaseModel):
    title: str
    difficulty: Difficulty
    link: HttpUrl

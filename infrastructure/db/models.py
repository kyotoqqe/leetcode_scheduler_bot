from .connection import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
import enum


class Difficulty(enum.Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"


class LeetcodeTask(Base):
    __tablename__ = "leetcodetasks"
    task_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    difficulty: Mapped[Difficulty]
    link: Mapped[str] = mapped_column(String(512))
    user_id: Mapped[int]

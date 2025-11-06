from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True, default=None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

 
        
    
    def to_dict(self):
        result = {
            "id": self.id, 
            "title": self.title, 
            "description": self.description,
            "is_complete": self.completed_at is not None
        }

        if self.goal_id:
            result.update({
                "goal_id": self.goal.id
            })

        return result






    @classmethod
    def from_dict(cls, task_data):

        goal_id = task_data.get("goal_id")

        new_task = cls(
            title=task_data["title"],
            description=task_data["description"],
            goal_id=goal_id
        )

        return new_task

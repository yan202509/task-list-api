from flask import Blueprint, abort, request, Response
from app.models.task import Task
from .route_utilities import create_model
from ..db import db


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# @tasks_bp.post("")
# def create_task():
#     request_body = request.get_json()
#     title = request_body["title"]
#     description = request_body["description"]
#     is_complete = False

#     new_task= Task(title=title, description=description)
#     db.session.add(new_task)
#     db.session.commit()

#     response = {
#         "id": new_task.id,
#         "title": new_task.title,
#         "description": new_task.description,
#         "is_complete": False
# }
#     return response, 201

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)



from flask import Blueprint, abort, request, Response
from app.models.task import Task
from .route_utilities import create_model, validate_model, get_models_with_filters
from ..db import db


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)


@tasks_bp.get("")
def get_task():
    return get_models_with_filters(Task, request.args)

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json") # 204 means No Content

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

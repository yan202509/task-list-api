from flask import Blueprint, abort, request, Response
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import create_model, validate_model, get_models_with_filters
from ..db import db
from datetime import datetime
import os
import requests

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    # called the function inside route_utilities
    return create_model(Goal, request_body)

@bp.get("")
def get_goal():
    return get_models_with_filters(Goal, request.args)

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.to_dict()

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json") # 204 means No Content

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# called the function inside route_utilities
# the create_author function called route_utilities

#wave 6
@bp.post("/<goal_id>/tasks")
def post_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])

    # use query to get all the tasks that is related to this one goal
    # this is also use later, can make it into a helpfer function later
    tasks_assign_to_goal = Task.query.filter_by(goal_id=goal.id).all()

    # setting the goal_id to none
    # so now the goal does not have the task(s) 
    for task in tasks_assign_to_goal:
        task.goal_id = None

    # use of foreign key to connecting the two
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id   
    
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids,
        }, 200



@bp.get("/<goal_id>/tasks")
def get_tasks_for_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_assign_to_goal = Task.query.filter_by(goal_id=goal.id).all()

    # return as a dict
    # all tha tasks inside goal
    tasks_list = [task.to_dict() for task in tasks_assign_to_goal]

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_list
    }, 200



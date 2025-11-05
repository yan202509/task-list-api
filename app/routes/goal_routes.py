from flask import Blueprint, abort, request, Response
from app.models.goal import Goal
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
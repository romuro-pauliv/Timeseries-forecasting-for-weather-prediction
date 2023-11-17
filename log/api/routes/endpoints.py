# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                            api.routes.endpoints.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import Blueprint, request
from api.queue.queue import Queue
# |--------------------------------------------------------------------------------------------------------------------|

bp = Blueprint("logs", __name__)

@bp.route("/debug", methods=["POST"])
def debug_post() -> tuple[str, int]:
    
    Queue.receiver_in_queue(request.json)
    
    return "Created", 201


@bp.route("/info", methods=["POST"])
def info_post() -> tuple[str, int]:
    
    Queue.receiver_in_queue(request.json)
    
    return "Created", 201


@bp.route("/warning", methods=["POST"])
def warning_post() -> tuple[str, int]:
    
    Queue.receiver_in_queue(request.json)
    
    return "Created", 201


@bp.route("/error", methods=["POST"])
def error_post() -> tuple[str, int]:
    
    Queue.receiver_in_queue(request.json)
    
    return "Created", 201


@bp.route("/critical", methods=["POST"])
def critical_post() -> tuple[str, int]:
    
    Queue.receiver_in_queue(request.json)
    
    return "Created", 201
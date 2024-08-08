
from flask import request, jsonify, abort, make_response
from functools import wraps
from app.common.base_filter import filter


def filters(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if request.args:
            request_args = request.args
            if "page" in request_args:
                filter.page = request_args["page"]
            if "per_page" in request_args:
                filter.per_page = request_args["per_page"]
            if "sort" in request_args:
                filter.sort = request_args["sort"]
            if "sort_order" in request_args:
                filter.sort_order = request_args["sort_order"]
            if "queries" in request_args:
                filter.page = request_args["queries"]
        
        return f(filter, *args, **kwargs)
    return decorator
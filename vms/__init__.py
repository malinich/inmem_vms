from flask import Blueprint

blueprint = Blueprint("vms", __name__)


def create_module():
    from vms.urls import urls
    for u in urls:
        view_func = u['view'].as_view(u['name'])
        blueprint.add_url_rule(u['path'], view_func=view_func)
    return blueprint

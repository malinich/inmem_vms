from flask import Flask


def create_app():
    app = Flask(__name__,)
    from vms import create_module as vms_create_module
    vms_blueprint = vms_create_module()

    app.register_blueprint(vms_blueprint, url_prefix="/")

    return app

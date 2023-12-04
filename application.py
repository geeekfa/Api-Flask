from flask import Flask, jsonify, redirect
from flask_restful import Api, MethodNotAllowed, NotFound
from flask_cors import CORS
from util.common import prefix, secret, build_swagger_config_json
from resources.bookResource import BooksGETResource, BookGETResource, BookPOSTResource, BookPUTResource, BookDELETEResource
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended.exceptions import NoAuthorizationError

# ============================================
# Main
# ============================================
application = Flask(__name__)
app = application
app.config["JWT_SECRET_KEY"] = secret
app.config['PROPAGATE_EXCEPTIONS'] = True
CORS(app)
api = Api(app, prefix=prefix, catch_all_404s=True)

# ============================================
# Swagger
# ============================================
build_swagger_config_json()
swaggerui_blueprint = get_swaggerui_blueprint(
    prefix,
    '/static/swagger/config.json',
    config={
        'app_name': "Flask API",
        "layout": "BaseLayout",
        "docExpansion": "none"
    },
)
app.register_blueprint(swaggerui_blueprint)

# ============================================
# Error Handler
# ============================================


@app.errorhandler(NoAuthorizationError)
def handle_no_auth_error(e):
    response = jsonify({"message": str(e)})
    response.status_code = 401
    return response


@app.errorhandler(NotFound)
def handle_method_not_found(e):
    response = jsonify({"message": str(e)})
    response.status_code = 404
    return response


@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed_error(e):
    response = jsonify({"message": str(e)})
    response.status_code = 405
    return response


@app.route('/')
def redirect_to_python_agm():
    if prefix != '':
        return redirect(prefix)


# ============================================
# Add Resource
# ============================================
# GET books
api.add_resource(BooksGETResource, '/books')
api.add_resource(BookGETResource, '/books/<int:id>')
# POST book
api.add_resource(BookPOSTResource, '/books')
# PUT book
api.add_resource(BookPUTResource, '/books/<int:id>')
# DELETE book
api.add_resource(BookDELETEResource, '/books/<int:id>')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=False, port=5000)
    app.run(debug=True)

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources.bookResource import BooksGETResource, BookGETResource, BookPOSTResource, BookPUTResource, BookDELETEResource

# ============================================
# Main
# ============================================
application = Flask(__name__)
app = application
CORS(app)
api = Api(app)

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
    app.run(debug=False)
    # app.run(host='0.0.0.0', debug=False, port=80)

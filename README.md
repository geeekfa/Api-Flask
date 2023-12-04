# **Python REST APIs**

[Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) is an effective Flask extension that simplifies the process of developing REST APIs. It offers a minimalistic layer of abstraction that effortlessly blends with your current ORM or libraries. Flask-RESTful promotes the implementation of industry best practices while maintaining a straightforward setup. If you have prior experience with Flask, you'll discover that Flask-RESTful is straightforward to grasp.
***

### Features
- **List Books**: Retrieve a list of all available books.
- **Get Book**: Retrieve details of a specific book by its ID.
- **Add Book**: Add a new book to the collection.
- **Update Book**: Modify the details of an existing book.
- **Delete Book**: Remove a book from the collection.

## 

> Create project
```shell
# Create a new folder named "python_flask_restful"
mkdir python_flask_restful

# Navigate to the newly created folder
cd python_flask_restful

# Create a python environment
python3 -m venv .venv

# Activate the environment
source .venv/bin/activate

# Update the python package manager
pip3 install --upgrade pip

# Install the required libraries
pip3 install Flask
pip3 install Flask-Cors
pip3 install Flask-RESTful
```
## 

> Open the project on VS Code

<small>After opening the project in VS Code, your project structure should be like this:</small>
```plaintext
python_flask_restful/
│
└── .venv/
```
## 

> Let's create: 
> 1. `application.py` 
> 2. `resources/`
> 3. `.vscode/launch.json`

<small>After creating them, your project structure should be like this:</small>
```plaintext
python_flask_restful/
│
├── .venv/
├── .vscode/
│    └── launch.json
├── resources/
└── application.py
```

## 

> Add the following content to `.vscode/launch.json` to configure the debugger in VS Code
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Run",
            "type": "python",
            "request": "launch",
            "program": "application.py",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

## 

> Create `resources/bookResource.py`

```python
from flask_restful import Resource
from flask import request
import json

books = [{"id": 1, "title": "Java book"},
         {"id": 2, "title": "Python book"}]


class BooksGETResource(Resource):
    def get(self):
        return books

class BookGETResource(Resource):
    def get(self, id):
        for book in books:
            if book["id"] == id:
                return book
        return None


class BookPOSTResource(Resource):
    def post(self):
        book = json.loads(request.data)
        new_id = max(book["id"] for book in books) + 1
        book["id"] = new_id
        books.append(book)
        return book


class BookPUTResource(Resource):
    def put(self, id):
        book = json.loads(request.data)
        for _book in books:
            if _book["id"] == id:
                _book.update(book)
                return _book


class BookDELETEResource(Resource):
    def delete(self, id):
        global books
        books = [book for book in books if book["id"] != id]
```

## 

> Add the following content to the  `application.py`

```python
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
```

## 

> Run

<small>To run the application in Visual Studio Code, you can click the Run button and select the `Python: Run` launch configuration.</small>

## 

> Call APIs

```shell
curl --location 'http://127.0.0.1:5000/books'
curl --location 'http://127.0.0.1:5000/books/1'

curl --location --request POST 'http://127.0.0.1:5000/books' \
--header 'Content-Type: application/json' \
--data '{
    "title": "AI"
}'

curl --location --request PUT 'http://127.0.0.1:5000/books/3' \
--header 'Content-Type: text/plain' \
--data '{
    "title": "SQL"
}'

curl --location --request DELETE 'http://127.0.0.1:5000/books/3'
```

## 

> Deploy

<small>To deploy the app to a server, create a `requirements.txt` like this:</small>

```shell
pip3 freeze > requirements.txt
```

<small>After deploying app to the server, open a terminal in the server and install the libraries by the following command:</small>

```shell
pip3 install -r requirements.txt
```
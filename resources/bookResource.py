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
        return "", 204

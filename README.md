# Building a RESTful API with Python Flask and Swagger: A Comprehensive Guide
<img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" height="50"/> <img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg" alt="Flask" height="50"/> <img src="https://upload.wikimedia.org/wikipedia/commons/a/ab/Swagger-logo.png" alt="Swagger" height="50"/>

Set up your Flask app to seamlessly integrating Swagger for documentation and API testing, this guide provides a step-by-step walkthrough. Learn best practices for structuring your API, documenting endpoints with Swagger annotations, and leveraging the power of Flask to create a scalable and maintainable application. Whether you're a seasoned developer or just getting started with APIs, this article will equip you with the knowledge to build, document, and run APIs with confidence using Flask and Swagger.

---

### Features
- **List Books**: Retrieve a list of all available books.
- **Get Book**: Retrieve details of a specific book by its ID.
- **Add Book**: Add a new book to the collection.
- **Update Book**: Modify the details of an existing book.
- **Delete Book**: Remove a book from the collection.

---

1.  Create project
    ```shell
    # Create a new folder named "Api-Flask"
    mkdir Api-Flask

    # Navigate to the newly created folder
    cd Api-Flask

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
    pip3 install flask-swagger-ui
    pip3 install gunicorn
    pip3 install python-dotenv
    ```

2. Open the project on VS Code

    After opening the project in VS Code, your project structure should be like this:
    ```plaintext
    Api-Flask/
    │
    └── .venv/
    ```

3. Let's create: 
   - `.vscode/launch.json`
   - `resources/`
   - `static/`
     - `swagger/`
       - `config.json`
   -  `util/`
   -  `.env`
   -  `application.py`
   
    After creating them, your project structure should be like this:
    ```plaintext
    Api-Flask/
    │
    ├── .venv/
    ├── .vscode/
    │    └── launch.json
    ├── resources/
    ├── static/
    │    └── swagger/
    │           └── config.json
    ├── util/
    ├── .env
    └── application.py
    ```

4. Add the following content to `.vscode/launch.json` to configure the debugger in VS Code
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

5. Create `resources/bookResource.py`

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
            return "", 204
    ```

6. Create `resources/swaggerConfig.py` to get swagger `config.json`
    ```python
    from flask_restful import Resource
    from flask import jsonify
    import json


    class SwaggerConfig(Resource):
        def get(self):
            with open('static/swagger/config.json', 'r') as config_file:
                config_data = json.load(config_file)
            return jsonify(config_data)
    ```

7. Add the following content to `static/swagger/config.json` to configure the swagger
   ```json
    {
        "openapi": "3.0.3",
        "info": {
            "title": "Flask API",
            "version": "1.0.0"
        },
        "servers": [
            { "url": "http://localhost:5000" },
            { "url": "http://example.com:5000" }
        ],
        "tags": [
            { "name": "book", "description": "CRUD Operations" }
        ],
        "paths": {
            "/books": {
                "get": {
                    "tags": ["book"],
                    "summary": "Retrieve all books",
                    "responses": {
                        "200": {
                            "description": "Successful",
                            "content": {
                                "application/json": {
                                    "schema": { "$ref": "#/components/schemas/Book" }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["book"],
                    "summary": "Create a book",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "title": { "type": "string", "example": "Nuxt" }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Created successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": { "token": { "type": "string" } }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/books/{id}": {
                "get": {
                    "tags": ["book"],
                    "summary": "Retrieve specific book",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": true,
                            "schema": { "type": "string" }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful",
                            "content": {
                                "application/json": {
                                    "schema": { "$ref": "#/components/schemas/Book" }
                                }
                            }
                        },
                        "404": { "description": "Not found" }
                    },
                    "security": [{ "bearerAuth": [] }]
                },
                "put": {
                    "tags": ["book"],
                    "summary": "Update a book",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": true,
                            "schema": { "type": "integer", "format": "int32" },
                            "description": "ID of the book to be updated"
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "title": { "type": "string", "example": "SQL" }
                                    },
                                    "required": ["title"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Updated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": { "token": { "type": "string" } }
                                    }
                                }
                            }
                        },
                        "404": { "description": "Book not found" }
                    }
                },
                "delete": {
                    "tags": ["book"],
                    "summary": "Delete a book",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": true,
                            "schema": { "type": "integer", "format": "int32" },
                            "description": "ID of the book to be deleted"
                        }
                    ],
                    "responses": {
                        "204": { "description": "Deleted successfully" },
                        "404": { "description": "Book not found" }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "Book": {
                    "type": "object",
                    "properties": {
                        "id": { "type": "integer", "format": "int64", "example": 1 },
                        "title": { "type": "string", "example": "Java" }
                    }
                }
            }
        }
    }
   ```

8. Create `util/common.py` to setup the common configuration.
   ```python
    import dotenv
    import os
    import json


    class ENVIRONMENT:
        def __init__(self):
            project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
            dotenv_path = os.path.join(project_dir, '.env')
            dotenv.load_dotenv(dotenv_path)
            self.domain = os.getenv("DOMAIN")
            self.port = os.getenv("PORT")
            self.prefix = os.getenv("PREFIX")

        def get_instance(self):
            if not hasattr(self, "_instance"):
                self._instance = ENVIRONMENT()
            return self._instance

        def getDomain(self):
            return self.domain

        def getPort(self):
            return self.port

        def getPrefix(self):
            return self.prefix


    domain = ENVIRONMENT().get_instance().getDomain()
    port = ENVIRONMENT().get_instance().getPort()
    prefix = ENVIRONMENT().get_instance().getPrefix()


    def build_swagger_config_json():
        config_file_path = 'static/swagger/config.json'

        with open(config_file_path, 'r') as file:
            config_data = json.load(file)

        config_data['servers'] = [
            {"url": f"http://localhost:{port}{prefix}"},
            {"url": f"http://{domain}:{port}{prefix}"}
        ]

        new_config_file_path = 'static/swagger/config.json'

        with open(new_config_file_path, 'w') as new_file:
            json.dump(config_data, new_file, indent=2)
   ```


9. Define the environment valiables in the `.env` file.
    ```yaml
    DOMAIN=localhost
    PORT=5000
    PREFIX=
    ```

10. Add the following content to the  `application.py`

    ```python
        from flask import Flask, jsonify, redirect
        from flask_restful import Api, MethodNotAllowed, NotFound
        from flask_cors import CORS
        from util.common import domain, port, prefix, build_swagger_config_json
        from resources.swaggerConfig import SwaggerConfig
        from resources.bookResource import BooksGETResource, BookGETResource, BookPOSTResource, BookPUTResource, BookDELETEResource
        from flask_swagger_ui import get_swaggerui_blueprint

        # ============================================
        # Main
        # ============================================
        application = Flask(__name__)
        app = application
        app.config['PROPAGATE_EXCEPTIONS'] = True
        CORS(app)
        api = Api(app, prefix=prefix, catch_all_404s=True)

        # ============================================
        # Swagger
        # ============================================
        build_swagger_config_json()
        swaggerui_blueprint = get_swaggerui_blueprint(
            prefix,
            f'http://{domain}:{port}{prefix}/swagger-config',
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
        def redirect_to_prefix():
            if prefix != '':
                return redirect(prefix)


        # ============================================
        # Add Resource
        # ============================================
        # GET swagger config
        api.add_resource(SwaggerConfig, '/swagger-config')
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
            app.run(debug=True)
    ```

11. Run

- `Visual Studio Code:` run the application in Visual Studio Code, you can click the Run button and select the `Python: Run` launch configuration.
  
  OR

- `gunicorn:` run the application by using the following command in the terminal.
    ```shell
    gunicorn application:app -b 0.0.0.0:5000
    ```

12.  Open your browser and navigate to http://localhost:5000. You should see the Swagger page and be able to interact with the APIs.


13. Deploy

    To deploy the app to a server, create a `requirements.txt` like this:

    ```shell
    pip3 freeze > requirements.txt
    ```

    After deploying app to the server, open a terminal in the server and install the libraries by the following command:</small>

    ```shell
    pip3 install -r requirements.txt
    ```

[<img src="https://upload.wikimedia.org/wikipedia/commons/c/c2/GitHub_Invertocat_Logo.svg" alt="Github" height="30"/> https://github.com/geeekfa/Api-Flask ](https://github.com/geeekfa/Api-Flask)
---
# Dockerizing a Python Flask App: A Step-by-Step Guide to Containerizing Your Web Application
<img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" height="50"/> <img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Flask_logo.svg" alt="Flask" height="50"/> <img src="https://upload.wikimedia.org/wikipedia/en/f/f4/Docker_logo.svg" alt="Docker" height="50"/>

Discover the essentials of containerizing your Python Flask app with Docker. This guide covers creating Dockerfiles, optimizing builds, and using Docker Compose for deployment. Follow step-by-step instructions to encapsulate your app, manage dependencies, and ensure consistency. Whether you're new to Docker or enhancing your skills, unlock containerization's power and elevate your development workflow.

---

1.  Install Docker
    - Refer to this like [https://www.docker.com/get-started/](https://www.docker.com/get-started/) to install Docker on your machine.
2.  Create a Python Flask project
    
    To create a Python Flask, refer to the medium.com article or clone the prepared project from the Github repository.

    - [Building a RESTful API with Python Flask and Swagger: A Comprehensive Guide](https://medium.com/@geeekfa/building-a-restful-api-with-python-flask-and-swagger-a-comprehensive-guide-e9c9c92853e6)
    - [Github Repository](https://github.com/geeekfa/Api-Flask)
  
3. Create `Dockerfile` in the root of the project.
   ```Makefile
    # Use the official Python 3.8 slim image as the base image
    FROM python:3.8-slim

    # Set the working directory within the container
    WORKDIR /api-flask

    # Copy the necessary files and directories into the container
    COPY resources/ static/ util/ .env application.py requirements.txt /api-flask/
    COPY resources/ /api-flask/resources/
    COPY static/ /api-flask/static/
    COPY util/ /api-flask/util/
    COPY .env application.py requirements.txt  /api-flask/

    # Upgrade pip and install Python dependencies
    RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

    # Expose port 5000 for the Flask application
    EXPOSE 5000

    # Define the command to run the Flask application using Gunicorn
    CMD ["gunicorn", "application:app", "-b", "0.0.0.0:5000", "-w", "4"]
   ```

4. Build a `Docker Image`
   ```bash
   sudo docker build -t api-flask .
   ```
   If you run the following command, you will see the created `Docker Image`.
   ```bash
   docker images
   ```
   ```
    REPOSITORY                   TAG               IMAGE ID       CREATED          SIZE
    api-flask                    latest            161bac35dd39   11 seconds ago   183MB
   ```
   *Some values may be different.*

5. Create a `Volume` directory
   - Create a folder in your machine. (*e.g. ~/Documents/temp/api-flask*)
   - Create `.env` file and add the following content to it.
        ```
        DOMAIN=localhost
        PORT=8080
        PREFIX=
        ```
6. Start a `Docker container`
   - Open a terminal in the created folder and run the following command.
     * `--rm`: Automatically remove the container when it exits.
     * `--it`: Allocate a pseudo-TTY and keep STDIN open, allowing you to interact with the container.
     * `-p 8080:5000`: Publish container's port 5000 to the host machine's port 8080.
     * `--name api-flask-container`: Assign a name to the running container.
     * `api-flask`: The name of the Docker image to be used for creating the container.
   ```bash
   sudo docker run --rm -it -p 8080:5000 -v ./.env:/api-flask/.env --name api-flask-container api-flask
   ```
   - As you see, the container is running and `gunicorn` is listening at `http://0.0.0.0:5000`
    ```bash
    [2023-12-12 06:40:07 +0000] [1] [INFO] Starting gunicorn 21.2.0
    [2023-12-12 06:40:07 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
    [2023-12-12 06:40:07 +0000] [1] [INFO] Using worker: sync
    [2023-12-12 06:40:07 +0000] [8] [INFO] Booting worker with pid: 8
    [2023-12-12 06:40:07 +0000] [9] [INFO] Booting worker with pid: 9
    [2023-12-12 06:40:07 +0000] [10] [INFO] Booting worker with pid: 10
    [2023-12-12 06:40:07 +0000] [11] [INFO] Booting worker with pid: 11
    ```

7. Open your browser and navigate to http://localhost:8080. You should see the Swagger page and be able to interact with the APIs.
   
8. Open a new terminal and run the following command, you will see the created `Docker Container`.
   ```bash
    docker ps
   ```
   ```
    CONTAINER ID   IMAGE                             COMMAND                  CREATED              STATUS              PORTS                    NAMES
    4d355b2637dd   api-flask                         "gunicorn applicatio…"   About a minute ago   Up About a minute   0.0.0.0:8080->5000/tcp   api-flask-container
   ```
   *Some values may be different.*

   ---

   ## Tips
   1. If you close the running terminal, the container doesn't run anymore. To run the container in detached mode, use `-d`.
        ```bash
        sudo docker run --rm -d -it -p 8080:5000 -v ./.env:/api-flask/.env --name api-flask-container api-flask
        ```
   2. To interact with the container:
        ```bash
        docker exec -it api-flask-container sh
        ``` 
        Now you can run the commands inside the container. For example, by running the following command, you will be informed about the Linux release.
        ```bash
        cat /etc/os-release
        ```
        ```bash
        PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
        NAME="Debian GNU/Linux"
        VERSION_ID="12"
        VERSION="12 (bookworm)"
        VERSION_CODENAME=bookworm
        ID=debian
        HOME_URL="https://www.debian.org/"
        SUPPORT_URL="https://www.debian.org/support"
        BUG_REPORT_URL="https://bugs.debian.org/"
        ```
   
    3. To remove a Docker image:
        ```bash
        docker rmi <image_name_or_id>
        ```
    4. To remove all the Docker images:
        ```bash
        sudo docker rmi $(docker images -q)
        ```
    5. To stop a Docker container:
        ```bash
        docker stop <container_name_or_id>
        ```
    6. To remove a Docker container:
        ```bash
        docker rm <container_name_or_id>
        ```
    7. To remove all the stopped Docker containers:
        ```bash
        docker container prune
        ```
    8. To remove all the Docker containers:
        ```bash
        sudo docker rm $(docker ps -a -q)
        ```
    9. To save a Docker image in your machine:
        ```bash
        docker save -o api-flask.tar api-flask
        ```
    10. To load a Docker image:
        ```bash
        docker load -i api-flask.tar
        ```
    11. To push a Docker image to the Docker Hub:
        ```bash
        docker login

        # amd64
        docker buildx build --platform linux/amd64 -t <your_docker_hub_username>/api-flask:latest-amd64 --push .
        
        # arm64
        docker buildx build --platform linux/arm64 -t <your_docker_hub_username>/api-flask:latest-arm64 --push .
        ```


#!/usr/bin/env python3
import os
from flask import Flask, request, current_app, g, make_response

app = Flask(__name__)

@app.before_request
def set_app_path():
    # Path on the SERVER where this app lives
    g.path = os.path.abspath(current_app.root_path)

@app.route('/')
def index():
    host = request.host
    appname = current_app.name

    response_body = (
        f"<h1>The host for the page is {host}</h1>"
        f"<h2>The name of this application is {appname}</h2>"
        f"<h3>The path of the application on the server is {g.path}</h3>"
    )

    headers = {"Content-Type": "text/html; charset=utf-8"}
    return make_response(response_body, 200, headers)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

# The Request-Response Cycle

Web browsers cannot execute Python code. To make our views show up in the browser, Flask needs to translate HTTP requests into Python objects and new Python objects into HTTP responses. There are plenty of strategies to do this by hand, but Flask makes our lives easier with Werkzeug- you'll find that Flask generates WSGI maps for your application with little to no manual configuration on your part.
<br /><br />
Let's take a look under the hood at the request-response cycle in Flask applications.

## The Scenario

You are working to build a simple request response trigger for a newly built server. Your goal is to build a single route that takes the hosts information and displays it with the proper codes.

## Tools & Resources

- [GitHub Repo](https://github.com/learn-co-curriculum/flask-request-response-cycle-technical-lesson)
- [Flask: QuickStart](https://flask.palletsprojects.com/en/stable/quickstart)
- [API - Pallets Projects](https://flask.palletsprojects.com/en/2.2.x/api/)
- [HTTP request methods - Mozilla](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [HTTP response status codes - Mozilla](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [Response Objects - Pallets Projects](https://flask.palletsprojects.com/en/2.2.x/api/#response-objects)

## Instructions

### Set Up

Before we begin coding, let's complete the initial setup for this lesson: 

* Fork and Clone
 * Go to the provided GitHub repository link.
 * Fork the repository to your GitHub account.
 * Clone the forked repository to your local machine.
* Open and Run File
 * Open the project in VSCode.
 * Run pipenv install to install all necessary dependencies.
 * Run pipenv shell to open instance of python shell

### Task 1: Define the Problem

You are working to build a simple request response trigger for a newly built server. 
Your goal is to build a single route that takes the hosts information and displays it with the proper codes.

### Task 2: Determine the Design

Determine Routes and responses

* ```/```
 * HTML elements, 200

### Task 3: Develop, Test, and Refine the Code 

#### Step 1: Create a Feature Branch

```bash
git checkout -b request_response
```

#### Step 2: HTTP request

* When a Flask application gets a request from the browser, it has to pass some specific objects to the view function that will respond to that request. One example is the request object itself, which contains the HTTP request from the browser.
* View functions do not take request objects as arguments. Since every view function needs access to a request object- among other things- Flask manages requests through contexts.

***All code changes will happen in server/app.py***

```python
# server/app.py

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    host = request.headers.get('Host')
    return f'<h1>The host for this page is {host}</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
```

* Our application will be handling many requests, a common problem is overlapping with one another while multiple users are visiting our website. To make this functional we did an import request, we didn't assign it any attributes that would tell it about the activity on our server. It almost seems like a global variable- one that is set outside of our application instances and views that provides an unchanging set of information. That wouldn't make much sense as an implementation, though: 
* Flask generates a context for requests after receiving a request and before our application runs. When request is called, we have access to all of that request data without having to do any configuration or include a request argument to our view. 

#### Step 3: Accessing Application Context

* Flask also has an application context. This works very much the same way as a request context: when a request is received, Flask generates the application context.
* When the application instance is accessed, the application context becomes available to our app and views.
* This provides information on the application we're working on and is accessible through the ```flask.current_app``` object.

```python
# server/app.py

from flask import Flask, request, current_app

app = Flask(__name__)

@app.route('/')
def index():
    host = request.headers.get('Host')
    appname = current_app.name
    return f'''<h1>The host for this page is {host}</h1>
               <h2>The name of this application is {appname}</h2>'''

if __name__ == '__main__':
    app.run(port=5555, debug=True)
```

* Flask also provides us two unique objects that allow us to manipulate request data more effectively:
 * ```g``` is an object that can be used to store anything that you want to store globally for the lifetime of a request. It is reset with each new request.
 * ```session``` is a dictionary object that can be used to hold onto values between multiple requests

#### Step 4: Trigger Request Hooks

* As you build out a variety of Flask web applications, you will notice that there are many tasks that you want to carry out before or after most of your view functions. This could be as simple as generating a reminder message or as complex as multi-factor authentication- either way, you'll want to handle these with hooks

```python
# server/app.py
import os
from flask import Flask, request, current_app, g

app = Flask(__name__)

@app.before_request
def app_path():
    g.path = os.path.abspath(os.getcwd())

@app.route('/')
def index():
    host = request.headers.get('Host')
    appname = current_app.name
    return f'''<h1>The host for this page is {host}</h1>
            <h2>The name of this application is {appname}</h2>
            <h3>The path of this application on the user's device is {g.path}</h3>'''

if __name__ == '__main__':
    app.run(port=5555, debug=True)
```

* We are using the following hook: ```@app.before_request```: runs a function before each request
* We are setting up a hook so that our views all know where our application files are located

#### Step 5: Creating Response

* An important part of any response is the HTTP status code. Flask sets this to 200 by default, which indicates that the request successfully reached the specified resource and an appropriate response was generated.
* When we need to send a different status code, we can simply add this as a second return value after the response body

```python
# server/app.py
import os
from flask import Flask, request, current_app, g

app = Flask(__name__)

@app.before_request
def app_path():
    g.path = os.path.abspath(os.getcwd())

@app.route('/')
def index():
    host = request.headers.get('Host')
    appname = current_app.name
    return f'''<h1>The host for this page is {host}</h1>
            <h2>The name of this application is {appname}</h2>
            <h3>The path of this application on the user's device is {g.path}</h3>'''

if __name__ == '__main__':
    app.run(port=5555, debug=True)
```

* 202 is the "Accepted" status code. This signifies that a request has been received by the server, but that the server has not done anything about it yet. We could also return 204 if there was no content on the page, or 404 if the URL was not found.

#### Step 6: Response Object

* For a more object-oriented approach to responses, you can use Flask's ```make_response()``` function. This takes 1-3 arguments in the same format as our earlier response: a body string, a status code, and a headers dictionary, respectively.

```python
#!/usr/bin/env python3
import os
from flask import Flask, request, current_app, g, make_response

app = Flask(__name__)
@app.before_request
def app_path():
    g.path = os.path.abspath(os.getcwd())

@app.route('/')
def index():
    host = request.headers.get('Host')
    appname = current_app.name
    response_body = f'''
        <h1>The host for this page is {host}</h1>
        <h2>The name of this application is {appname}</h2>
        <h3>The path of this application on the user's device is {g.path}</h3>
    '''
    status_code = 200
    headers = {}
    return make_response(response_body, status_code, headers)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
```

* While this will not change the response from the browser this is best practice and will make your code cleaner and easier to understand! In addition while not often, the use of headers is necessary for more complex responses.
* Once you have verified that our routes work, commit changes:

```bash
git commit -am "Finish / route"
```

#### Step 7: Push and Merge

* Push the branch to GitHub:

```bash
git push origin request_response
```

* Create a Pull Request (PR) on GitHub.

* Merge the PR into main after review.

* Pull the new merged main branch locally and delete merged feature branch (optional): 

```bash
git checkout main
git pull origin main

git branch -d request_response
```

* If the last command doesn’t delete the branch, it’s likely git is not recognizing the branch as having been merged.

* Verify you do have the merged code in your main branch, then you can run the same command but with a capital D to ignore the warning and delete the branch anyway.

```bash
git branch -D request_response
```

### Task 4: Document and Maintain

Best practices documentation steps:

* Add comments to code to explain purpose and logic, clarifying intent/functionality of code to other developers.
* Update README text to reflect the functionality of the application following: https://makeareadme.com.
 * Add screenshot of completed work included in README markdown.
* Delete any stale branches on GitHub
* Remove unnecessary/commented out code
* If needed, update git ignore to remove sensitive data

## Considerations

* Status Codes
  * There are a whole bunch of common status codes! Visit this [Mozilla: Redirect Status](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status) to see other common codes
* Redirect
  * There are specific cases where your response is meant to do something other than display an HTML body in the browser, the redirect.
  * The ```redirect()``` function is usually delivered with a "301: Moved Permanently" or "302: Found" status code. These signify that the URL for the resource on our server has been changed.
  * We can redirect the user to the current URL for the resource. ```redirect()``` takes one argument, the URL for the relocated resource

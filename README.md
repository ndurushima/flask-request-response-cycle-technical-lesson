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

## Considerations

* Status Codes
  * There are a whole bunch of common status codes! Visit this Mozilla: Redirect StatusLinks to an external site. to see other common codes
* Redirect
  * There are specific cases where your response is meant to do something other than display an HTML body in the browser, the redirect.
  * The redirect() function is usually delivered with a "301: Moved Permanently" or "302: Found" status code. These signify that the URL for the resource on our server has been changed.
  * We can redirect the user to the current URL for the resource. Redirect() takes one argument, the URL for the relocated resource

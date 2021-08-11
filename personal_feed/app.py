import aiohttp_jinja2
import jinja2
from aiohttp import web

from settings import *
from db import UserDoesntExists
from async_logic import person_feed

http_error_message_header='''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User input error</title>
</head>
<body>
<h1>'''

routes = web.RouteTableDef()

@aiohttp_jinja2.template('index.html')
async def feed(request):
    user_id = request.rel_url.query.get('user_id')
    if not isinstance(user_id, int):
        if user_id is None or not user_id.isdigit():
           raise web.HTTPBadRequest(headers = {'Content-Type': 'text/html '},
                    text = http_error_message_header+
                    'Wrong User id</h1>'+
                    'User ID should be integer. Please try again.'+
                    '</body>')
    try:
        feed = await person_feed(int(user_id))
        return feed
    except UserDoesntExists:
        raise web.HTTPBadRequest(headers = {'Content-Type': 'text/html '},
                    text = http_error_message_header+
                    'User does not exist</h1>'+
                    'Sorry, we could not find the user with ID'+
                     f'= {user_id}. Please try again.'+
                    '</body>')
    

# RUN async application 
if __name__ == "__main__":
    app = web.Application()
    app.add_routes([web.get('/', feed)])
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(TEMPLATE_PATH)
    )
    web.run_app(app, port=5000, host='127.0.0.1')

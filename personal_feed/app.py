import aiohttp_jinja2
import jinja2
from aiohttp import web

from personal_feed.settings import *
from personal_feed.db import UserDoesntExists
from personal_feed.async_logic import person_feed

routes = web.RouteTableDef()

@aiohttp_jinja2.template('index.html')
async def feed(request):
    user_id = request.rel_url.query.get('user_id')
    if not isinstance(user_id, int):
        if user_id is None or not user_id.isdigit():
           raise web.HTTPBadRequest(headers = {'Content-Type': 'text/html '}, text =
'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User input error</title>
</head>
<body>
<h1>Wrong User id</h1>
User ID should be integer. Please try again.
</body>''')

    try:
        feed = await person_feed(int(user_id))
        return feed
    except UserDoesntExists:
        raise web.HTTPBadRequest(headers = {'Content-Type': 'text/html '}, text =
f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User input error</title>
</head>
<body>
<h1>User does not exist</h1>
Sorry, we could not find the user with ID = {user_id}. Please try again.
</body>''')
    

# RUN async application
app = web.Application()
app.add_routes([web.get('/', feed)])
aiohttp_jinja2.setup(
    app,
    loader=jinja2.FileSystemLoader(TEMPLATE_PATH)
)
web.run_app(app, port=5000, host='127.0.0.1')

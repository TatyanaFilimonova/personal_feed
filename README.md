# personal_feed
Original "personal feed" was refactored using aiohttp, jinja2, asyncio, asyncfile

app.py - http server refactored with aiohttp and jinja2

async_logic.py - requesting and parsing data from the web APIs using aiohttp and asyncio

db.py - DB interaction using asyncio and aiofiles

DISCLAIMER: I only tested the vitality of code, didn't compare the efficiency with original "personal feed".
I couldn't measure it cause internet connection here, on the island in Adriatic sea, is very unstaible and slooooooow. I will be appretiate if you would do test and share the results. Thanks!

QUESTION/PROBLEM: 
There were the problems with local modules import when running the app under the flask.
I used package.module import * to avoid an error. When you pull the repository from GIT - do not rename the folder. 
So, could you advise more elegant way to solve this problem?

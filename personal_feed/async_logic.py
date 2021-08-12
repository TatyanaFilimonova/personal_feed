import aiohttp
import asyncio
import time
from db import *

async def _get_response(url_type, url, session, timeout=None):
    if timeout is None:
        timeout = 5.0
    try:
        async with session.get(url, timeout = timeout) as response:
            response = await session.get(url, timeout=timeout)
            res = await response.json()
    except TimeoutError:
        return None
    return url_type, res


async def get_content(urls: dict):
    res = {}
    task_lst = []
    result_lst = []
    async with aiohttp.ClientSession() as session:
        location = asyncio.create_task(_get_response('location_url', urls['location_url'],  session,timeout=None))        
        location = await asyncio.gather(location , loop=None, return_exceptions=False)
        urls.pop('location_url')
        for url_type in urls:
            if url_type == 'weather_url':
                urls['weather_url'] = urls['weather_url']+ str(location[0][1][0]['woeid'])
            task_lst.append(asyncio.create_task(_get_response(url_type, urls[url_type],  session,timeout=None)))
        result_lst = await asyncio.gather(*task_lst, loop=None, return_exceptions=False)
        for r in result_lst:
            res[r[0]] = r[1]
        return res

    
def _get_urls_dict(user: User):
    city = user.city
    urls = {}
    _type = user.user_type
    if _type == 'cat':
       urls['picture_url']  = 'https://thatcopy.pw/catapi/rest/'
       urls['fact_url']     = 'https://catfact.ninja/fact?max_length=140'
    elif _type == 'dog':
        urls['picture_url'] = 'https://dog.ceo/api/breeds/image/random'
        urls['fact_url']    = 'https://dog-facts-api.herokuapp.com/api/v1/resources/dogs?number=1'
    else:
        raise RuntimeError(f'Unknown user type {user.user_type }')
    urls['location_url']    = f'https://www.metaweather.com/api/location/search/?query={city}'
    urls['weather_url']      = f'https://www.metaweather.com/api/location/'
    return urls


def _get_weather_feed_user(weather): 
    dates_weather = weather
    if dates_weather is None:
        return
    response = []
    for date in dates_weather['consolidated_weather']:
        response.append(
            dict(
                state=date['weather_state_name'],
                temp=round(float(date['the_temp']), 2),
                date=date['applicable_date'],
                humidity=date['humidity'],
                visibility=round(float(date['visibility']), 2),
            )
        )
    return response


async def _get_feed(user: User):
    data_dict  = await get_content(_get_urls_dict(user=user))
    feed = dict(user=user)
    if user.user_type == 'dog':
        feed['image'] = data_dict['picture_url']['message']
        feed['fact'] = data_dict['fact_url'][0]['fact']
    else:
        feed['image'] = data_dict['picture_url']['url']
        feed['fact'] = data_dict['fact_url']['fact']
        feed['weather'] = _get_weather_feed_user(data_dict['weather_url'])
    return feed


async def person_feed(user_id):
    user = await get_user_sync(user_id)
    return await _get_feed(user)    

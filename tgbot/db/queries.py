import logging

import aiohttp
from aiohttp import ClientSession, ClientResponseError, ClientError


class Database:
    class NotFoundException(Exception):
        ...

    class BadRequestError(Exception):
        ...

    class ChannelAlreadyExists(Exception):
        ...

    def __init__(self, base_url):
        self.base_url = base_url

    async def make_request(self, method, endpoint, data=None):
        url = self.base_url + endpoint

        async with (ClientSession(headers={'Referer': 'http://django:8000/'}, timeout=aiohttp.ClientTimeout(total=10))
                    as session):
            async with session.request(method, url, json=data) as resp:
                if resp.status in [200, 201]:
                    return await resp.json()
                elif resp.status == 400:
                    r = await resp.json()
                    logging.info(r)
                    if r == ['Channel with this ID exists.']:
                        raise self.ChannelAlreadyExists
                    raise ClientError()
                elif resp.status in [401, 403, 404]:
                    raise ClientError()
                else:
                    raise ClientResponseError(resp.request_info,
                                              resp.history,
                                              status=resp.status,
                                              message=resp.reason)

    async def send_token_to_server(self, user_id, token):
        return await self.make_request("POST", "/create-chat/",
                                       {'token': token, 'chat_id': user_id})

    async def create_channel(self, guid: str, channel_id: str, name: str, link: str):
        return await self.make_request("POST", "/channels/create/",
                                       {'guid': guid,
                                        'channel_id': channel_id,
                                        "name": name,
                                        "is_active": True,
                                        "link": link
                                        })

    async def get_poll(self, pk):
        return await self.make_request("GET", f"/polls/{pk}/")


    async def get_poll_owner_channels(self, pk):
        return await self.make_request("GET", f"/polls/channel/list/{pk}/")

    async def vote(self, user_id, poll_id, choice):
        url = self.base_url + "/polls/votes/create/"
        data = {'poll': poll_id,
                'user_id': user_id,
                "choice": choice}
        async with ClientSession() as session:
            async with session.request("POST", url, json=data) as resp:
                c = await resp.json()
                logging.info(c)
                if resp.status in [200, 201]:
                    response = await resp.json(), True
                    return response
                elif resp.status == 400:
                    response = await resp.json(), False
                    return response
                else:
                    raise ClientError()

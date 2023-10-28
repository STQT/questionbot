import logging

from aiohttp import ClientSession, ClientResponseError, ClientError


class Database:
    # DELIVERY_COST = "10000"

    def __init__(self, base_url):
        self.base_url = base_url

    async def make_request(self, method, endpoint, data=None):
        url = self.base_url + endpoint

        async with ClientSession() as session:
            async with session.request(method, url, json=data) as resp:
                logging.info(resp.status)
                logging.info(resp.text)
                if resp.status in [200, 201]:
                    return await resp.json()
                elif resp.status in [400, 401, 403, 404]:
                    raise ClientError()
                else:
                    raise ClientResponseError(resp.request_info,
                                              resp.history,
                                              status=resp.status,
                                              message=resp.reason)
    async def send_token_to_server(self, user_id, token):
        return await self.make_request("POST", "/create-chat/",
                                       {'token': token, 'chat_id': user_id})

    async def create_channel(self, guid: str, channel_id: str, name: str):
        return await self.make_request("POST", "/channels/create/",
                                       {'guid': guid,
                                        'channel_id': channel_id,
                                        "name": name,
                                        "is_active": True
                                        })

    async def get_poll(self, pk):
        return await self.make_request("GET", f"/polls/{pk}/")


    async def get_poll_owner_channels(self, pk):
        return await self.make_request("GET", f"/polls/channel/list/{pk}/")

from aiohttp import ClientSession
from fastapi import HTTPException
from starlette import status


async def _make_request(session: ClientSession, method: str, url: str, **kwargs):
    async with session.request(method, url, **kwargs) as resp:
        if resp.status == status.HTTP_200_OK:
            return resp.json()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='no answer from service')


async def make_request(method: str, url: str, **kwargs):
    async with ClientSession() as session:
        return await _make_request(session, method, url, **kwargs)

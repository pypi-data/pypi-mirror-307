from .common import Response


async def fetch(url: str):
    from niquests import AsyncSession

    async with AsyncSession(happy_eyeballs=True) as session:
        res = await session.get(url)

        assert res.status_code is not None, res
        assert res.text is not None, res

        return Response(res.ok, res.status_code, res.headers, res.text)

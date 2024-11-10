from sys import argv

from . import Response, fetch


def get_loop():
    from asyncio import get_running_loop, new_event_loop

    try:
        return get_running_loop()
    except RuntimeError:
        return new_event_loop()


def print_response(res: Response):
    for k, v in res.headers.items():
        print(f"{k}: {v}")
    print()
    print(res.text)


async def run():
    try:
        res = await fetch(*argv[1:])
        print_response(res)
    except KeyboardInterrupt:
        print(" Interrupted")


def main():
    get_loop().run_until_complete(run())

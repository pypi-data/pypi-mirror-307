from aiohttp.formdata import FormData


async def read_body(receive) -> bytes:
    body = b''
    more_body = True

    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    return body


async def answer(send, form: FormData):
    data = form()
    body = data.decode().encode(encoding='utf-8')
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            (b'content-type', data.content_type.encode()),
            (b'content-length', str(data.size or len(body)).encode())
        ]
    })
    await send({
        'type': 'http.response.body',
        'body': body,
    })

async def _send_code(send, code: int) -> None:
    await send({
        'type': 'http.response.start',
        'status': code,
        'headers': [
            (b'content-length', b"0")
        ]
    })
    await send({
        'type': 'http.response.body',
        'body': b"",
    })

async def ok(send):
    await _send_code(send, 200)

async def error(send):
    await _send_code(send, 500)

def parce_path(path: str) -> tuple[str, slice, str]:
    start_token = path.index("{bot_token}")
    if start_token + 11 == len(path):
        end_token = None
        path_postfix = ""
    else:
        end_token = start_token + 11 - len(path)
        path_postfix = path[end_token:]
    return path[:start_token], slice(start_token, end_token), path_postfix

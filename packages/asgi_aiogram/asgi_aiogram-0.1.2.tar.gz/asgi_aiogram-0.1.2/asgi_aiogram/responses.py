from aiohttp.formdata import FormData

async def answer(send, form: FormData) -> None:
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

async def ok(send) -> None:
    await _send_code(send, 200)

async def error(send) -> None:
    await _send_code(send, 500)
